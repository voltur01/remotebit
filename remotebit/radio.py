# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# remote:bit is a remote Python execution library for BBC micro:bit
# https://github.com/voltur01/remotebit

from microbit import *
from typing import Tuple

def on() -> None:
    get_mb_link().send('radio.on')

def off() -> None:
    get_mb_link().send('radio.off')

def config(**kwargs) -> None:
    # TODO: too advanced?
    raise RemotebitException('remote-bit: radio.config is not implemented.')

def reset():
    get_mb_link().send('radio.reset')

def send_bytes(message: bytes) -> None:
    get_mb_link().send(f'radio.send_bytes {mb_from_bytes(message)}')

def receive_bytes() -> bytes:
    msg = get_mb_link().send_receive('radio.receive_bytes')
    return mb_to_bytes(msg) if msg else None

def receive_bytes_into(buffer: bytes) -> None:
    # TODO: handle buffers
    raise RemotebitException('remote-bit: radio.receive_bytes_into is not implemented.')

#TODO: b'\x01\x00\x01' prepended to the front???
def send(message: str) -> None:
    send_bytes(bytes(message, 'utf8'))

def receive() -> str:
    bts = receive_bytes()
    return str(bts, 'utf8') if bts else None

def receive_full() -> Tuple[bytes, int, int]:
    # TODO: too advanced?
    raise RemotebitException('remote-bit: radio.receive_full is not implemented.')
