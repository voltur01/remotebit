# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *
import speech

speech.say('hello world')

p = speech.translate('hello world')
check (p != '', 'wrong pronounce')
speech.pronounce(p)
speech.sing(p)
