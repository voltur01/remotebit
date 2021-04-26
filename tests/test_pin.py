# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

touch_pins = [pin0, pin1, pin2]

for tpin in touch_pins:
    t = tpin.is_touched()

analog_pins = [pin0, pin1, pin2, pin3, pin4, pin10]

display.off()

for apin in analog_pins:
    apin.write_analog(512)
    v = apin.read_analog()

digital_pins = [pin6, pin7, pin8, pin9, 
        pin12, pin13, pin14, pin15, pin16]
        # pins 5 and 11 are used by buttons
        # pins 19 and 20 are used by I2C

for dpin in digital_pins:
    dpin.write_digital(1)
    v = dpin.read_digital()

pin0.set_analog_period(1)
pin0.set_analog_period_microseconds(2500)

display.on()
