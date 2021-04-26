# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# remote:bit is a remote Python execution library for BBC micro:bit
# https://github.com/voltur01/remotebit

from microbit import *

def translate(words: str) -> None:
    return mb_unescape(get_mb_link().send_receive(f'speech.translate {mb_escape(words)}'))

def pronounce(phonemes: str, *, \
        pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128) -> None:
    get_mb_link().send(f'speech.pronounce {mb_escape(phonemes)} {pitch} {speed} {mouth} {throat}')

def say(words: str, *, \
        pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128) -> None:
    get_mb_link().send(f'speech.say {mb_escape(words)} {pitch} {speed} {mouth} {throat}')

def sing(phonemes: str, *, \
        pitch: int = 64, speed: int = 72, mouth: int = 128, throat: int = 128) -> None:
    get_mb_link().send(f'speech.sing {mb_escape(phonemes)} {pitch} {speed} {mouth} {throat}')
