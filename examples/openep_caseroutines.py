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

import sys
sys.path.append("..") 

import numpy as np
import matplotlib.pyplot as plt
import openep 
from openep._datasets.openep_datasets import DATASET_2

case = openep.load_openep_mat(DATASET_2)
print("##################################")
print("case: ", case)
mesh = case.create_mesh()

# determine the window of interest for each point
woi = openep.case.case_routines._get_window_of_interest(case)
print("woi1: ", np.shape(woi))
reference_time = openep.case.case_routines._get_reference_annotation(case)
print("reference_time: ", np.shape(reference_time))
woi += reference_time[:, np.newaxis]
print("woi2: ", np.shape(woi))

# Get mapping points within WOI
mapping_points = openep.case.get_mapping_points_within_woi(case, indices=np.arange(10))
print("mapping_points: ", mapping_points)
# Get electrograms for specific points
electrograms, names, local_activation_times = openep.case.get_electrograms_at_points(
    case,
    egm_type="reference",
    indices=[1, 10, 100],
    return_names=True,
    return_lat=True,
)

print("local_activation_times: ", local_activation_times)

# Plot the electrogram traces
# Array of times that are within the window of interest:
times = openep.case.get_woi_times(case)
print("times: ", times)
fig, axis = openep.draw.plot_electrograms(
    times=times,
    electrograms=electrograms[:, times],  # only show the electrograms within the woi
    names=names,
    woi=woi[0]
)
plt.show()

# Plot Carto bipolar voltages
plotter = openep.draw.draw_map(
    mesh=mesh,
    field=case.fields.bipolar_voltage,
)
plotter.background_color = "white"
# plotter.show()

# Interpolate bipolar voltage onto surface from raw electrograms
interpolated_voltages = openep.case.interpolate_voltage_onto_surface(case, max_distance=15, bipolar=False)
plotter = openep.draw.draw_map(
    mesh=mesh,
    field=interpolated_voltages,
    add_mesh_kws={"clim": (0, 5)}
)
plotter.background_color = "white"
# plotter.show()
