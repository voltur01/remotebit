# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# remote:bit is a remote Python execution library for BBC micro:bit
# https://github.com/voltur01/remotebit

import time

def sleep_ms(ms: int) -> None:
    time.sleep(ms / 1000)

def sleep_us(us: int) -> None:
    time.sleep(us / 1000000)

def ticks_ms() -> int:
    return round(time.time() * 1000)

def ticks_us() -> int:
    return round(time.time() * 1000000)

def ticks_add(ticks: int, delta: int) -> int:
    return ticks + delta

def ticks_diff(ticks1: int, ticks2: int) -> int:
    return ticks1 - ticks2
    