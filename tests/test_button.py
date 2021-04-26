# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

check(button_a.is_pressed() == False, 'button A should not be pressed')
check(button_a.was_pressed() == False, 'button A was not be pressed')
check(button_a.get_presses() == 0, 'button A presses should be 0')

check(button_b.is_pressed() == False, 'button B should not be pressed')
check(button_b.was_pressed() == False, 'button B was not be pressed')
check(button_b.get_presses() == 0, 'button B presses should be 0')
