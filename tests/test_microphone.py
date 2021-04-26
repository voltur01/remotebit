# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

level = microphone.sound_level()
check(isinstance(level, int), 'sound_level must be int')
