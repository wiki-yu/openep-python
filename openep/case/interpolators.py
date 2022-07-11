# OpenEP
# Copyright (c) 2021 OpenEP Collaborators
#
# This file is part of OpenEP.
#
# OpenEP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenEP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program (LICENSE.txt).  If not, see <http://www.gnu.org/licenses/>

"""
Interpolators - :mod:`openep.case.interpolators`
================================================

This module provides classes for performing interpolation.
"""

from attr import attrs

import numpy as np
import numba
from .case_routines import calculate_distance

__all__ = [
    'LocalSmoothingInterpolator',
]


@attrs(auto_attribs=True, auto_detect=True)
class LocalSMoothingInterpolator:
    """Interpolator for performing local  smoothing.

    Args:
        points (np.ndarray): Data point coordinates.
        field (np.ndarray): Scalar values for each point.
        smoothing_length (int): Cutoff distance between `points` and coordinates
            at which the interpolant is evaluated. Typically, values in the range
            5-10 are reasonable. Defaults to 5.
        fill_value (float): Value used to assign to the field at coordinates that
            fall outside the query radius.
    """

    points: np.ndarray
    field: np.ndarray
    smoothing_length: int = 5
    fill_value: float = np.NaN

    def __call__(self, new_points):
        """Evaluate the interpolant.

        Args:
            new_points (np.ndarray): Coordinates at which to evaluate the interpolant.

        Returns:
            y (np.ndarray): Interpolated field at `new_points`.
        """

        n_points = len(new_points)
        new_field = np.full(n_points, fill_value=self.fill_value, dtype=float)

        distances = calculate_distance(
            origin=new_points,
            destination=self.points,
        )

        new_field = _local_smoothing(
            field=self.field,
            smoothing_length=self.smoothing_length,
            distances=distances,
            out=new_field,
        )

        return new_field


@numba.jit(nopython=True, cache=True, fastmath=True)
def _local_smoothing(field, smoothing_length, distances, out):

    within_cutoff = distances < smoothing_length

    for index in range(out.shape[0]):

        if not np.any(within_cutoff[index]):
            continue

        # Calculate field at new points
        distance = distances[index]
        exponent = distance[distance < smoothing_length] / smoothing_length
        weights = np.exp(-exponent**2)
        normalised_weights = weights / weights.sum()

        field_value = sum(field[distance < smoothing_length] * normalised_weights)
        out[index] = field_value

    return out
