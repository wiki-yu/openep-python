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

from dataclasses import field
import sys
sys.path.append("..") 

import openep
import time
import numpy as np
import math
import pyvista as pv



filename = "../openep/_datasets/OpenEP-MATLAB/openep_dataset_2.mat"
case = openep.load_openep_mat(filename)
mesh = case.create_mesh()
print("mesh: ", mesh)
# print("mesh vertices: ", mesh.verts)

# mesh.plot(eye_dome_lighting=True)
# points = pv.wrap(mesh)
# surf = points.reconstruct_surface()
# pl = pv.Plotter(shape=(1, 2))
# pl.add_mesh(mesh)
# pl.add_title('Point Cloud of 3D Surface')
# pl.subplot(0, 1)
# pl.add_mesh(surf, color=True, show_edges=True)
# pl.add_title('Reconstructed Surface')
# pl.show()


print("voltage shape", np.shape(case.fields.bipolar_voltage))
print("voltage: ", case.fields.bipolar_voltage)
voltage = [0 if math.isnan(x) else x for x in case.fields.bipolar_voltage]
vol = np.array(voltage)
voltage = np.repeat(voltage, 4)
voltage = voltage[:46000]
# voltage[:5000] = 0
# voltage[5000:10000] = 4.0
# voltage[10000:] = 1
# voltage_extra = [4] * (16942 - 14383)
# voltage_extra = np.array(voltage_extra)
# voltage = np.concatenate((vol, voltage_extra), axis=0)
print("&&&&&&&&&&&&&&&&& len voltage: ", len(voltage))
print("voltage2: ", voltage)
print("max v: {}, min v: {}".format(np.max(voltage), np.min(voltage)))

# DrawVoltage Map
plotter = openep.draw.draw_map(
    mesh=mesh,
    # field=case.fields.bipolar_voltage,
    field=voltage,
)
plotter.show()
# plotter.show(interactive_update=True)


# # Animation
# for i in range(5, 10000):
#     # Updating our data
#     # Updating scalars
#     # plotter.update_scalars(mesh=mesh, scalars=case.fields.bipolar_voltage)
#     # noise = np.random.rand(np.shape(voltage)[0], 1).flatten()
#     noise = np.random.uniform(low=-0.02, high=0.02, size=(np.shape(voltage)[0], 1)).flatten()
#     noise = np.random.uniform(low=-0.2, high=0.2, size=(np.shape(voltage)[0], 1)).flatten()
#     voltage += noise
#     plotter.update_scalars(mesh=mesh, scalars=voltage)
#     #p.mesh['data'] = data.flatten() # setting data to the specified mesh is also possible
#     # Redrawing
#     plotter.update()
