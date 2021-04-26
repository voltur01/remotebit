# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

compass.calibrate()
t = compass.is_calibrated()
compass.clear_calibration()
x = compass.get_x()
y = compass.get_y()
z = compass.get_z()
h = compass.heading()
s = compass.get_field_strength()
