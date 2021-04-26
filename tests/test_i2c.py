# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

i2c.init()
ps = i2c.scan()
b = i2c.read(ps[0], 1)
# i2c.write(b)  # fails since there is no actual device there
