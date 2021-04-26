# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# remote:bit is a remote Python execution library for BBC micro:bit
# https://github.com/voltur01/remotebit

# MicroPython API reference:
# https://microbit-micropython.readthedocs.io/en/v2-docs/microbit_micropython_api.html

from typing import List, Tuple, Union
import platform
import sys
import serial

class RemotebitException(Exception):
    pass


# Global data

_mb_link = None
_mb_trace_serial = False
_mb_raise = False

if platform.system() == 'Windows':
    _mb_default_serial_name = 'COM7'
elif platform.system() == 'Darwin':
    _mb_default_serial_name = '/dev/tty.usbmodem102'
else:
    _mb_default_serial_name = '/dev/ttyACM0'

# micro:bit serial link


def set_trace_serial(on: bool) -> None:
    global _mb_trace_serial
    _mb_trace_serial = on


def set_raise(on: bool) -> None:
    global _mb_raise
    _mb_raise = on


def _report_error(msg: str) -> None:
    if _mb_raise:
        raise RemotebitException(msg)
    else:
        print('ERROR: micro:bit response: ' + msg)
        sys.exit(1)

def _trace(msg: str) -> None:
    if _mb_trace_serial:
        print('TRACE: ' + msg)


class SerialLink:
    def __init__(self, path):
        self.port = serial.Serial(path, '115200')

    def send(self, request: str, confirm: bool = True) -> None:
        request += '\r\n'

        self.port.write(request.encode())
        echo = self.port.readline().decode()

        _trace('request ' + repr(request))
        _trace('echo ' + repr(echo))

        if echo != request:
            while self.port.in_waiting:
                echo += self.port.readline().decode()
            _report_error(f'{repr(echo)} for reqest {repr(request)}')
        if confirm:
            confirmation = self.port.readline().decode().strip()
            if confirmation != 'ok':
                _report_error(f'{repr(confirmation)} for request {repr(request)}')

    def send_receive(self, request: str) -> str:
        self.send(request, confirm=False)
        response = self.port.readline().decode()
        
        _trace('response ' + repr(response))

        if response.startswith('EXCEPTION:'):
            _report_error(f'{repr(response)} for request {repr(request)}')
        
        return response.strip()


class DebugLink:
    def __init__(self, path):
        pass

    def send(self, request: str) -> None:
        print(request)

    def send_receive(self, request: str) -> str:
        self.send(request)
        return input()


def init_mb_link(path: str) -> None:
    global _mb_link
    try:
        _mb_link = SerialLink(path)
    except Exception as e:
        _mb_link = DebugLink('dummy')
        print(f'ERROR: Cannot connect to micro:bit ({str(e)}), '
                'using debug link to the console.')


init_mb_link(_mb_default_serial_name)


def get_mb_link() -> Union[SerialLink, DebugLink]:
    return _mb_link


# General utilities


def mb_escape(s: str) -> str:
    return s.replace('%', '%%').replace(' ', '%20').replace('\r', '%10')\
            .replace('\n', '%13')


def mb_unescape(s: str) -> str:
    return s.replace('\n', '%13').replace('\r', '%10').replace('%20', ' ')\
            .replace('%%', '%')


def mb_to_bytes(msg: str) -> bytes:
    return bytes([int(b) for b in mb_unescape(msg).split()])


def mb_from_bytes(bts: bytes) -> str:
    return mb_escape(' '.join([str(b) for b in bts]))


# micro:bit classes and functions


def sleep(ms: int) -> None:
    import time
    time.sleep(ms / 1000)


def running_time() -> int:
    return int(_mb_link.send_receive('running_time'))


def temperature() -> int:
    return int(_mb_link.send_receive('temperature'))


class Accelerometer:
    def get_x(self) -> int:
        return int(_mb_link.send_receive('a.get_x'))

    def get_y(self) -> int:
        return int(_mb_link.send_receive('a.get_y'))

    def get_z(self) -> int:
        return int(_mb_link.send_receive('a.get_z'))

    def get_values(self) -> (int, int, int):
        v_strs = _mb_link.send_receive('a.get_values').split(' ')
        return (int(v_strs[0]), int(v_strs[1]), int(v_strs[2]))

    def current_gesture(self) -> str:
        """
        up, down, left, right, face up, face down, freefall, 3g, 6g, 8g, shake
        """
        return _mb_link.send_receive('a.current_gesture')

    def is_gesture(self, gesture: str) -> bool:
        return _mb_link.send_receive(f'a.is_gesture {mb_escape(gesture)}') == 'True'

    def was_gesture(self, gesture: str) -> bool:
        return _mb_link.send_receive(f'a.was_gesture {mb_escape(gesture)}') == 'True'

    def get_gestures(self):
        return tuple(_mb_link.send_receive('a.get_gestures').split(' '))


accelerometer = Accelerometer()


class Compass:
    def calibrate(self) -> None:
        _mb_link.send('compass.calibrate')

    def is_calibrated(self) -> bool:
        return _mb_link.send_receive('compass.is_calibrated') == True

    def clear_calibration(self) -> None:
        _mb_link.send('compass.clear_calibration')

    def get_x(self) -> int:
        return int(_mb_link.send_receive('compass.get_x'))

    def get_y(self) -> int:
        return int(_mb_link.send_receive('compass.get_y'))

    def get_z(self) -> int:
        return int(_mb_link.send_receive('compass.get_z'))

    def heading(self) -> int:
        return int(_mb_link.send_receive('compass.heading'))

    def get_field_strength(self) -> int:
        return int(_mb_link.send_receive('compass.get_field_strength'))


compass = Compass()


class Image:
    def _pack(self, pixels):
        return ':'.join([''.join(line) for line in pixels])
    
    def _unpack(self, string):
        if '\n' in string:
            separator = '\n'
        else:
            separator = ':'
        return [list(line) for line in string.split(separator)]

    def __init__(self, *args):
        """
        Image() - Create a blank 5x5 image
        Image(string) - Create an image by parsing the string, a single character returns that glyph
        Image(width, height) - Create a blank image of given size
        Image(width, height, buffer) - Create an image from the given buffer
        """
        if len(args) == 0:
            self.pixels_str = ':'.join(['0' * 5] * 5)
        elif len(args) == 1 and isinstance(args[0], str):
            self.pixels_str = args[0]
        elif len(args) == 2:
            self.pixels_str = ':'.join(['0' * args[0]] * args[1])
        elif len(args) == 3:
            width = args[0]
            pixels = ''.join([chr(b + ord('0')) for b in args[2]])
            self.pixels_str = ':'.join([pixels[i:i + width] for i in range(0, len(args[2]), width)])
        else:
            raise RemotebitException('remote-bit: Image: Incorrect number or type of arguments.')

    @classmethod
    def _to_image(cls, string):
        return cls(string)

    def width(self) -> int:
        im = self._unpack(self.pixels_str)
        return len(im[0])

    def height(self) -> int:
        im = self._unpack(self.pixels_str)
        return len(im)

    def set_pixel(self, x: int, y: int, value: int) -> None:
        im = self._unpack(self.pixels_str)
        im[y][x] = str(value)
        self.pixels_str = self._pack(im)

    def get_pixel(self, x: int, y: int) -> int:
        im = self._unpack(self.pixels_str)
        return int(im[y][x])

    def shift_left(self, n: int):
        if n < 0:
            self.shift_right(-n)
        else:
            im = self._unpack(self.pixels_str)
            new_im = [line[n:] + ['0'] * n for line in im]
            return self._to_image(self._pack(new_im))

    def shift_right(self, n: int):
        if n < 0:
            self.shift_left(-n)
        else:
            im = self._unpack(self.pixels_str)
            new_im = [['0'] * n + line[:-n] for line in im]
            return self._to_image(self._pack(new_im))

    def shift_up(self, n: int):
        if n < 0:
            self.shift_down(-n)
        else:
            im = self._unpack(self.pixels_str)
            new_im = im[n:] + [['0'] * len(im[0])] * n
            return self._to_image(self._pack(new_im))

    def shift_down(self, n: int):
        if n < 0:
            self.shift_up(-n)
        else:
            im = self._unpack(self.pixels_str)
            new_im = [['0'] * len(im[0])] * n + im[:-n]
            return self._to_image(self._pack(new_im))

    def crop(self, x: int, y: int, w: int, h: int):
        im = self._unpack(self.pixels_str)
        new_im = [line[x:x+w] for line in im[y:y+h]]
        return self._to_image(self._pack(new_im))

    def copy(self):
        return self._to_image(self.pixels_str)

    def invert(self):
        im = self._unpack(self.pixels_str)
        o0 = ord('0')
        invert = lambda line: [chr(abs(ord(p)-o0-9) + o0) for p in line]
        new_im = [invert(line) for line in im]
        return self._to_image(self._pack(new_im))

    def fill(self, n: int) -> None:
        w = self.width()
        h = self.height()
        im = [[chr(ord('0')+n)]*w for line in range(h)]
        self.pixels_str = self._pack(im)

    def blit(self, src, x: int, y: int, w: int, h: int,
            xdest: int = 0, ydest: int = 0) -> None:
        src_im = self._unpack(src.pixels_str)
        src_w = src.width()
        src_h = src.height()
        im = self._unpack(self.pixels_str)
        for ix in range(w):
            for iy in range(h):
                if x + ix < src_w and y + iy < src_h:
                    im[ydest + iy][xdest + ix] = src_im[y + iy][x + ix]
                else:
                    im[ydest + iy][xdest + ix] = '0'
        self.pixels_str = self._pack(im)

    def _add_mul_saturated(self, pc1: chr, pc2: chr, n: int = 1) -> chr:
        pi = (ord(pc1) + ord(pc2) - 2 * ord('0')) * n
        if pi <= 9:
            return chr(pi + ord('0'))
        else:
            return '9'

    def __add__(self, src):
        src_im = self._unpack(src.pixels_str)
        src_w = src.width()
        src_h = src.height()
        im = self._unpack(self.pixels_str)
        for ix in range(self.width()):
            for iy in range(self.height()):
                if ix < src_w and iy < src_h:
                    im[iy][ix] = self._add_mul_saturated(im[iy][ix], src_im[iy][ix])
        return self._to_image(self._pack(im))

    def __mul__(self, n):
        im = self._unpack(self.pixels_str)
        for ix in range(self.width()):
            for iy in range(self.height()):
                im[iy][ix] = self._add_mul_saturated(im[iy][ix], '0', n)
        return self._to_image(self._pack(im))


# These are the default icons as provided by MicroPython,
# refer to the MicroPython docs for the details and copyrights
Image.HEART = Image(
    '09090:'
    '99999:'
    '99999:'
    '09990:'
    '00900'
)

Image.HEART_SMALL = Image(
    '00000:'
    '09090:'
    '09990:'
    '00900:'
    '00000'
)

Image.HAPPY = Image(
    '00000:'
    '09090:'
    '00000:'
    '90009:'
    '09990'
)

Image.SMILE = Image(
    '00000:'
    '00000:'
    '00000:'
    '90009:'
    '09990'
)

Image.SAD = Image(
    '00000:'
    '09090:'
    '00000:'
    '09990:'
    '90009'
)

Image.CONFUSED = Image(
    '00000:'
    '09090:'
    '00000:'
    '09090:'
    '90909'
)

Image.ANGRY = Image(
    '90009:'
    '09090:'
    '00000:'
    '99999:'
    '90909'
)

Image.ASLEEP = Image(
    '00000:'
    '99099:'
    '00000:'
    '09990:'
    '00000'
)

Image.SURPRISED = Image(
    '09090:'
    '00000:'
    '00900:'
    '09090:'
    '00900'
)

Image.SILLY = Image(
    '90009:'
    '00000:'
    '99999:'
    '00909:'
    '00999'
)

Image.FABULOUS = Image(
    '99999:'
    '99099:'
    '00000:'
    '09090:'
    '09990'
)

Image.MEH = Image(
    '09090:'
    '00000:'
    '00090:'
    '00900:'
    '09000'
)

Image.YES = Image(
    '00000:'
    '00009:'
    '00090:'
    '90900:'
    '09000'
)

Image.NO = Image(
    '90009:'
    '09090:'
    '00900:'
    '09090:'
    '90009'
)

Image.CLOCK12 = Image(
    '00900:'
    '00900:'
    '00900:'
    '00000:'
    '00000'
)

Image.CLOCK1 = Image(
    '00090:'
    '00090:'
    '00900:'
    '00000:'
    '00000'
)

Image.CLOCK2 = Image(
    '00000:'
    '00099:'
    '00900:'
    '00000:'
    '00000'
)

Image.CLOCK3 = Image(
    '00000:'
    '00000:'
    '00999:'
    '00000:'
    '00000'
)

Image.CLOCK4 = Image(
    '00000:'
    '00000:'
    '00900:'
    '00099:'
    '00000'
)

Image.CLOCK5 = Image(
    '00000:'
    '00000:'
    '00900:'
    '00090:'
    '00090'
)

Image.CLOCK6 = Image(
    '00000:'
    '00000:'
    '00900:'
    '00900:'
    '00900'
)

Image.CLOCK7 = Image(
    '00000:'
    '00000:'
    '00900:'
    '09000:'
    '09000'
)

Image.CLOCK8 = Image(
    '00000:'
    '00000:'
    '00900:'
    '99000:'
    '00000'
)

Image.CLOCK9 = Image(
    '00000:'
    '00000:'
    '99900:'
    '00000:'
    '00000'
)

Image.CLOCK10 = Image(
    '00000:'
    '99000:'
    '00900:'
    '00000:'
    '00000'
)

Image.CLOCK11 = Image(
    '09000:'
    '09000:'
    '00900:'
    '00000:'
    '00000'
)

Image.ARROW_N = Image(
    '00900:'
    '09990:'
    '90909:'
    '00900:'
    '00900'
)

Image.ARROW_NE = Image(
    '00999:'
    '00099:'
    '00909:'
    '09000:'
    '90000'
)

Image.ARROW_E = Image(
    '00900:'
    '00090:'
    '99999:'
    '00090:'
    '00900'
)

Image.ARROW_SE = Image(
    '90000:'
    '09000:'
    '00909:'
    '00099:'
    '00999'
)

Image.ARROW_S = Image(
    '00900:'
    '00900:'
    '90909:'
    '09990:'
    '00900'
)

Image.ARROW_SW = Image(
    '00009:'
    '00090:'
    '90900:'
    '99000:'
    '99900'
)

Image.ARROW_W = Image(
    '00900:'
    '09000:'
    '99999:'
    '09000:'
    '00900'
)

Image.ARROW_NW = Image(
    '99900:'
    '99000:'
    '90900:'
    '00090:'
    '00009'
)

Image.TRIANGLE = Image(
    '00000:'
    '00900:'
    '09090:'
    '99999:'
    '00000'
)

Image.TRIANGLE_LEFT = Image(
    '90000:'
    '99000:'
    '90900:'
    '90090:'
    '99999'
)

Image.CHESSBOARD = Image(
    '09090:'
    '90909:'
    '09090:'
    '90909:'
    '09090'
)

Image.DIAMOND = Image(
    '00900:'
    '09090:'
    '90009:'
    '09090:'
    '00900'
)

Image.DIAMOND_SMALL = Image(
    '00000:'
    '00900:'
    '09090:'
    '00900:'
    '00000'
)

Image.SQUARE = Image(
    '99999:'
    '90009:'
    '90009:'
    '90009:'
    '99999'
)

Image.SQUARE_SMALL = Image(
    '00000:'
    '09990:'
    '09090:'
    '09990:'
    '00000'
)

Image.RABBIT = Image(
    '90900:'
    '90900:'
    '99990:'
    '99090:'
    '99990'
)

Image.COW = Image(
    '90009:'
    '90009:'
    '99999:'
    '09990:'
    '00900'
)

Image.MUSIC_CROTCHET = Image(
    '00900:'
    '00900:'
    '00900:'
    '99900:'
    '99900'
)

Image.MUSIC_QUAVER = Image(
    '00900:'
    '00990:'
    '00909:'
    '99900:'
    '99900'
)

Image.MUSIC_QUAVERS = Image(
    '09999:'
    '09009:'
    '09009:'
    '99099:'
    '99099'
)

Image.PITCHFORK = Image(
    '90909:'
    '90909:'
    '99999:'
    '00900:'
    '00900'
)

Image.XMAS = Image(
    '00900:'
    '09990:'
    '00900:'
    '09990:'
    '99999'
)

Image.PACMAN = Image(
    '09999:'
    '99090:'
    '99900:'
    '99990:'
    '09999'
)

Image.TARGET = Image(
    '00900:'
    '09990:'
    '99099:'
    '09990:'
    '00900'
)

Image.TSHIRT = Image(
    '99099:'
    '99999:'
    '09990:'
    '09990:'
    '09990'
)

Image.ROLLERSKATE = Image(
    '00099:'
    '00099:'
    '99999:'
    '99999:'
    '09090'
)

Image.DUCK = Image(
    '09900:'
    '99900:'
    '09999:'
    '09990:'
    '00000'
)

Image.HOUSE = Image(
    '00900:'
    '09990:'
    '99999:'
    '09990:'
    '09090'
)

Image.TORTOISE = Image(
    '00000:'
    '09990:'
    '99999:'
    '09090:'
    '00000'
)

Image.BUTTERFLY = Image(
    '99099:'
    '99999:'
    '00900:'
    '99999:'
    '99099'
)

Image.STICKFIGURE = Image(
    '00900:'
    '99999:'
    '00900:'
    '09090:'
    '90009'
)

Image.GHOST = Image(
    '99999:'
    '90909:'
    '99999:'
    '99999:'
    '90909'
)

Image.SWORD = Image(
    '00900:'
    '00900:'
    '00900:'
    '09990:'
    '00900'
)

Image.GIRAFFE = Image(
    '99000:'
    '09000:'
    '09000:'
    '09990:'
    '09090'
)

Image.SKULL = Image(
    '09990:'
    '90909:'
    '99999:'
    '09990:'
    '09990'
)

Image.UMBRELLA = Image(
    '09990:'
    '99999:'
    '00900:'
    '90900:'
    '09900'
)

Image.SNAKE = Image(
    '99000:'
    '99099:'
    '09090:'
    '09990:'
    '00000'
)

Image.ALL_ARROWS = [Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, 
        Image.ARROW_SE, Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW]
Image.ALL_CLOCKS = [Image.CLOCK12, Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, 
        Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, Image.CLOCK7, Image.CLOCK8, 
        Image.CLOCK9, Image.CLOCK10, Image.CLOCK11]
       

class Display:
    def clear(self) -> None:
        _mb_link.send('display.clear')

    def set_pixel(self, x: int, y: int, b: int) -> None:
        _mb_link.send(f'display.set_pixel {x} {y} {b}')

    def get_pixel(self, x: int, y: int) -> int:
        return int(_mb_link.send_receive(f'display.get_pixel {x} {y}'))

    def show(self, value, delay: int = 400, *,
            wait: bool = True, loop: bool = False, clear: bool = False) -> None:
        value_type = ''
        if isinstance(value, Image):
            value_type = 'img'
            value = value.pixels_str
        elif isinstance(value, str):
            value_type = 'str'
        elif isinstance(value, int):
            value_type = 'int'
        elif isinstance(value, float):
            value_type = 'fp'

        if value_type:
            _mb_link.send(f'display.show {value_type} {value} {delay} {wait} {loop} {clear}')
        else:
            for v in value:
                self.show(v)

    def scroll(self, s: str) -> None:
        _mb_link.send(f'display.scroll {mb_escape(s)}')

    def on(self) -> None:
        _mb_link.send('display.on')

    def off(self) -> None:
        _mb_link.send('display.off')

    def is_on(self) -> bool:
        return _mb_link.send_receive('display.is_on') == 'True'

    def read_light_level(self) -> int:
        return int(_mb_link.send_receive('display.read_light_level'))


display = Display()


class Button:
    def __init__(self, button_name):
        self.button_name = button_name

    def is_pressed(self) -> bool:
        return _mb_link.send_receive(f'button.is_pressed {self.button_name}') == 'True'

    def was_pressed(self) -> bool:
        return _mb_link.send_receive(f'button.was_pressed {self.button_name}') == 'True'

    def get_presses(self) -> int:
        return int(_mb_link.send_receive(f'button.get_presses {self.button_name}'))


button_a = Button('A')
button_b = Button('B')


class AnalogPin:
    def __init__(self, pin):
        self.pin = pin
    
    def read_analog(self) -> int:
        return int(_mb_link.send_receive(f'pin.read_analog {self.pin}'))

    def write_analog(self, value: int) -> None:
        _mb_link.send(f'pin.write_analog {self.pin} {value}')

    def read_digital(self) -> int:
        return int(_mb_link.send_receive(f'pin.read_digital {self.pin}'))

    def write_digital(self, value: int) -> None:
        _mb_link.send(f'pin.write_digital {self.pin} {value}')

    def set_analog_period(self, period: int) -> None:
        _mb_link.send(f'pin.set_analog_period {self.pin} {period}')

    def set_analog_period_microseconds(self, period: int) -> None:
        _mb_link.send(f'pin.set_analog_period_microseconds {self.pin} {period}')

    def is_touched(self) -> bool:
        return _mb_link.send_receive(f'pin.is_touched {self.pin}') == 'True'


class DigitalPin:
    def __init__(self, pin):
        self.pin = pin

    def read_digital(self) -> int:
        return int(_mb_link.send_receive(f'pin.read_digital {self.pin}'))

    def write_digital(self, value: int) -> None:
        _mb_link.send(f'pin.write_digital {self.pin} {value}')


pin0 = AnalogPin(0)     # Pad 0
pin1 = AnalogPin(1)     # Pad 1
pin2 = AnalogPin(2)     # Pad 2
pin3 = AnalogPin(3)     # Column 1
pin4 = AnalogPin(4)     # Column 2
pin5 = DigitalPin(5)    # Button A
pin6 = DigitalPin(6)    # Row 2
pin7 = DigitalPin(7)    # Row 1
pin8 = DigitalPin(8) 	 
pin9 = DigitalPin(9)    # Row 3
pin10 = AnalogPin(10)   # Column 3
pin11 =	DigitalPin(11)  # Button B
pin12 =	DigitalPin(12) 	 
pin13 =	DigitalPin(13)  # SPI MOSI
pin14 =	DigitalPin(14)  # SPI MISO
pin15 =	DigitalPin(15)  # SPI SCK
pin16 =	DigitalPin(16)
pin19 =	DigitalPin(19)  # I2C SCL
pin20 =	DigitalPin(20)  # I2C SDA


Pin = Union[AnalogPin, DigitalPin]


def mb_pin_num(pin: Pin) -> int:
    pins = [pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10,
        pin11, pin12, pin13, pin14, pin15, pin16, None, None, pin19, pin20]
    return pins.index(pin)


class I2C:
    def init(self, freq: int = 100000, sda: Pin = pin20, scl: Pin = pin19) -> None:
        _mb_link.send(f'i2c.init {freq} {mb_pin_num(sda)} {mb_pin_num(scl)}')
        
    def scan(self) -> List[int]:
        return [int(p) for p in _mb_link.send_receive('i2c.scan').split()]

    def read(self, addr: int, n: int, repeat: bool = False) -> bytes:
        return bytes.fromhex(_mb_link.send_receive(f'i2c.read {addr} {n} {repeat}'))

    def write(addr, buf: bytes, repeat: bool = False) -> None:
        _mb_link.send(f'i2c.send {buf.hex()} {repeat}')


i2c = I2C()


class SPI:
    def init(self, baudrate: int = 1000000, bits: int = 8, mode: int = 0, \
            sclk: Pin = pin13, mosi: Pin = pin15, miso: Pin = pin14) -> None:
        _mb_link.send(f'spi.init {baudrate} {bits} {mode} {mb_pin_num(sclk)} {mb_pin_num(mosi)} {mb_pin_num(miso)}')
    def read(self, nbytes: int) -> bytes:
        pass
    def write(self, buffer: bytes) -> None:
        pass
    def write_readinto(self, out_buf: bytes, in_buf: bytes) -> None:
        # TODO: handle the in/out buffers
        # cannot find any example projects with SPI though - does it even make sense?
        raise RemotebitException('remote-bit: spi.write_readinto() is not implemented.')


spi = SPI()


class UART:
    # TODO: the default UART is used by the library for the communication,
    # thus is not available to the user.
    # It can be used with other devices though - to be added on demand.
    pass


# class Random: # - host module should work locally
# TODO: see how to limit the functions to ones available on MB


class Speaker:
    def on(self) -> None:
        _mb_link.send('speaker.on')

    def off(self) -> None:
        _mb_link.send('speaker.off')


speaker = Speaker()


class SoundEvent:
    QUIET = None
    LOUD = None


class Microphone:
    SoundEvent = SoundEvent()

    def current_event(self):
        raise RemotebitException('remote-bit: microphone.current_event is not implemented.')

    def was_event(self, event):
        raise RemotebitException('remote-bit: microphone.was_event is not implemented.')

    def is_event(self, event):
        raise RemotebitException('remote-bit: microphone.is_event is not implemented.')

    def get_events(self):
        raise RemotebitException('remote-bit: microphone.get_events is not implemented.')

    def set_threshold(self, event, value):
        raise RemotebitException('remote-bit: microphone.set_threshold is not implemented.')

    def set_threshold(self, event, value):
        raise RemotebitException('remote-bit: microphone.set_threshold is not implemented.')

    def sound_level(self) -> int:
        return int(_mb_link.send_receive('microphone.sound_level'))


microphone = Microphone()


class _UName:
    def __init__(self, sysname, nodename, release, version, machine):
        self.sysname = sysname
        self.nodename = nodename
        self.release = release
        self.version = version
        self.machine = machine


class OS:
    def uname(self):
        return _UName('remotebit', 'nodename', '0', '0', 'machine')

    def listdir(self):
        raise RemotebitException('remote-bit: os.listdir() is not implemented.')

    def remove(self, filename):
        raise RemotebitException('remote-bit: os.remove() is not implemented.')

    def size(self, filename):
        raise RemotebitException('remote-bit: os.size() is not implemented.')


os = OS()
