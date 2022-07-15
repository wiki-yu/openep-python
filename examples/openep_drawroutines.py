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


# filename = "./data/openep_dataset_2.mat"
filename = "../openep/_datasets/OpenEP-MATLAB/openep_dataset_2.mat"
case = openep.load_openep_mat(filename)
mesh = case.create_mesh()
print("mesh: ", mesh)


print("shape!!!!!!!!", np.shape(case.fields.bipolar_voltage))
print("v1: ", case.fields.bipolar_voltage)
voltage = [0 if math.isnan(x) else x for x in case.fields.bipolar_voltage]
voltage = np.array(voltage)
print("v2: ", voltage)
print("max v: ", np.max(voltage))
print("min v: ", np.min(voltage))

# DrawVoltage Map
# start_time = time.time()
plotter = openep.draw.draw_map(
    mesh=mesh,
    # field=case.fields.bipolar_voltage,
    field=voltage,
)


# plotter.show()
plotter.show(interactive_update=True)
# end_time = time.time()
# print("time gap: ", end_time - start_time)

# Animation
for i in range(5, 10000):
    # Updating our data
    # Updating scalars
    # plotter.update_scalars(mesh=mesh, scalars=case.fields.bipolar_voltage)
    # noise = np.random.rand(np.shape(voltage)[0], 1).flatten()
    noise = np.random.uniform(low=-0.02, high=0.02, size=(np.shape(voltage)[0], 1)).flatten()
    voltage += noise
    plotter.update_scalars(mesh=mesh, scalars=voltage)
    #p.mesh['data'] = data.flatten() # setting data to the specified mesh is also possible
    # Redrawing
    plotter.update()
