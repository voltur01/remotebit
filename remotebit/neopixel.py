# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# remote:bit is a remote Python execution library for BBC micro:bit
# https://github.com/voltur01/remotebit

from microbit import *

class NeoPixel:
    def __init__(self, pin: Pin, n: int) -> NeoPixel:
        # TODO: handle remote stateful class
        raise RemotebitException('remote-bit: NeoPixel() is not implemented.') 
