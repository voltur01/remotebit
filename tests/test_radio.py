# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *
import radio

radio.on()
radio.reset()
radio.send('hello')
rs = radio.receive()
radio.off()
