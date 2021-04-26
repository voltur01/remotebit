# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

x = accelerometer.get_x()
y = accelerometer.get_y()
z = accelerometer.get_z()
x, y, z = accelerometer.get_values()
g = accelerometer.current_gesture()
g = accelerometer.is_gesture('up')
g = accelerometer.was_gesture('left')
gs = accelerometer.get_gestures()
