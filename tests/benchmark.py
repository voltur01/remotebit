# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# test the speed difference

# remote:bit -> ~140 reads/sec
# real micro:bit native -> ~3600 read/sec, i.e. 25 faster

# pylint: disable=unused-wildcard-import
from microbit import * 
from utime import *

iterations = 1000

t_begin = ticks_ms()
for i in range(iterations):
    v = pin0.read_analog()
t_end = ticks_ms()

diff_ms = ticks_diff(t_end, t_begin)

print('ms: ' + str(diff_ms))
print('ops / sec: ' + str(iterations / diff_ms * 1000))
