# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# It is difficult to test the actual logic with the micro:bit hardware in the loop,
# thus this testing is mostly a smoke test to make sure the names of methods,
# and the number and types of parameters are correct.

# No testing framework is used, since the debug version of the serial link uses the
# console, which makes unit test frameworks unhappy.

from microbit import *

def check(test, message):
    if not(test):
        print('FAILED: ' + message)

set_trace_serial(True)
