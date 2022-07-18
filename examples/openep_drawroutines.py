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
start_time = time.time()
case = openep.load_openep_mat(filename)
end_time = time.time()
print("time gap: ", end_time - start_time)
mesh = case.create_mesh()
end_time2 = time.time()
print("create mesh time: ", end_time2 - end_time)
print("mesh: ", mesh)

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
voltage = np.array(voltage)
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
#     voltage += noise
#     plotter.update_scalars(mesh=mesh, scalars=voltage)
#     #p.mesh['data'] = data.flatten() # setting data to the specified mesh is also possible
#     # Redrawing
#     plotter.update()
