# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *
from utime import *

t1 = ticks_ms()
sleep_ms(1000)
t2 = ticks_ms()
check(ticks_diff(t2, t1) - 1000 < 10, 'sleep_ms deviation should be small')
