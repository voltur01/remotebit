# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy
# https://github.com/voltur01/remotebit

from microbit import *
import music
# mbv2_begin
import gc
import radio
import speech
# mbv2_end

def escape(s: str) -> str:
    return s.replace('%', '%%').replace(' ', '%20').replace('\r', '%10').replace('\n', '%13')
def unescape(s: str) -> str:
    return s.replace('\n', '%13').replace('\r', '%10').replace('%20', ' ').replace('%%', '%')
# mbv2_begin
def to_bytes(msg: str) -> bytes:
    return bytes([int (b) for b in unescape(msg).split()])
def from_bytes(bts: bytes) -> str:
    return escape(' '.join([str(b) for b in bts]))
# mbv2_end
def confirm():
    print('ok')

buttons = { 'A': button_a, 'B': button_b }
pins = [pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10,
        pin11, pin12, pin13, pin14, pin15, pin16, None, None, pin19, pin20]
while True:
    try:
        request = input()
        params = request.split(' ')
        cmd = params[0]
        if cmd == 'pin.read_digital':
            print(pins[int(params[1])].read_digital())
        elif cmd == 'pin.write_digital':
            pins[int(params[1])].write_digital(int(params[2]))
            confirm()
        elif cmd == 'pin.read_analog':
            print(pins[int(params[1])].read_analog())
        elif cmd == 'pin.write_analog':
            pins[int(params[1])].write_analog(int(params[2]))
            confirm()
        elif cmd == 'pin.set_analog_period':
            pins[int(params[1])].set_analog_period(int(params[2]))
            confirm()
        elif cmd == 'pin.set_analog_period_microseconds':
            pins[int(params[1])].set_analog_period_microseconds(int(params[2]))
            confirm()
        elif cmd == 'pin.is_touched':
            print(pins[int(params[1])].is_touched())
        elif cmd == 'button.is_pressed':
            print(buttons[params[1]].is_pressed())
        elif cmd == 'button.was_pressed':
            print(buttons[params[1]].was_pressed())
        elif cmd == 'button.get_presses':
            print(buttons[params[1]].get_presses())
        elif cmd == 'display.clear':
            display.clear()
            confirm()
        elif cmd == 'display.set_pixel':
            display.set_pixel(int(params[1]), int(params[2]), int(params[3]))
            confirm()
        elif cmd == 'display.get_pixel':
            print(display.get_pixel(int(params[1]), int(params[2])))
        elif cmd == 'display.show':
            value_type = params[1]
            value = unescape(params[2])
            delay = int(params[3])
            wait = params[4] == True
            loop = params[5] == True
            clear = params[6] == True
            if value_type == 'img':
                display.show(Image(value))
            elif value_type == 'int':
                display.show(int(value), delay, wait = wait, loop = loop, clear = clear)
            elif value_type == 'fp':
                display.show(float(value), delay, wait = wait, loop = loop, clear = clear)
            elif value_type == 'str':
                display.show(value, delay, wait = wait, loop = loop, clear = clear)
            confirm()
        elif cmd == 'display.scroll':
            display.scroll(params[1])
            confirm()
        elif cmd == 'display.on':
            display.on()
            confirm()
        elif cmd == 'display.off':
            display.off()
            confirm()
        elif cmd == 'display.is_on':
            print(display.is_on())
        elif cmd == 'display.read_light_level':
            print(display.read_light_level())
        elif cmd == 'running_time':
            print(running_time())
        elif cmd == 'temperature':
            print(temperature())
        elif cmd == 'music.set_tempo':
            music.set_tempo(ticks = int(params[1]), bpm = int(params[2]))
            confirm()
        elif cmd == 'music.get_tempo':
            ticks, bpm = music.get_tempo()
            print(str(ticks) + ' ' + str(bpm))
        elif cmd == 'music.play':
            music.play(unescape(params[1]).split(), pins[int(params[2])], params[3] == 'True', params[4] == 'True')
            confirm()
        elif cmd == 'music.pitch':
            music.pitch(int(params[1]), int(params[2]), pins[int(params[3])], params[4] == 'True')
            confirm()
        elif cmd == 'music.stop':
            music.stop(pins[int(params[1])])
            confirm()
        elif cmd == 'music.reset':
            music.reset()
            confirm()
# mbv2_begin
        elif cmd == 'a.get_x':
            print(accelerometer.get_x())
        elif cmd == 'a.get_y':
            print(accelerometer.get_y())
        elif cmd == 'a.get_z':
            print(accelerometer.get_z())
        elif cmd == 'a.get_values':
            x, y, z = accelerometer.get_values()
            print(str(x) + ' ' + str(y) + ' ' + str(z))
        elif cmd == 'a.current_gesture':
            print(accelerometer.current_gesture())
        elif cmd == 'a.is_gesture':
            print(accelerometer.is_gesture(params[1]))
        elif cmd == 'a.was_gesture':
            print(accelerometer.was_gesture(params[1]))
        elif cmd == 'a.get_gestures':
            print(' '.join(accelerometer.get_gestures()))
        elif cmd == 'compass.calibrate':
            compass.calibrate()
            confirm()
        elif cmd == 'compass.is_calibrated':
            print(compass.is_calibrated())
        elif cmd == 'compass.clear_calibration':
            compass.clear_calibration()
            confirm()
        elif cmd == 'compass.get_x':
            print(compass.get_x())
        elif cmd == 'compass.get_y':
            print(compass.get_y())
        elif cmd == 'compass.get_z':
            print(compass.get_z())
        elif cmd == 'compass.heading':
            print(compass.heading())
        elif cmd == 'compass.get_field_strength':
            print(compass.get_field_strength())
        elif cmd == 'i2c.init':
            i2c.init(int(params[1]), pins[int(params[2])], pins[int(params[3])])
            confirm()
        elif cmd == 'i2c.scan':
            print(' '.join([str(a) for a in i2c.scan()]))
        elif cmd == 'i2c.read':
            print(i2c.read(int(params[1]), int(params[2]), params[3] == 'True').hex())
        elif cmd == 'i2c.write':
            i2c.write(bytes.fromhex(params[1]), params[2] == 'True')
            confirm()
        elif cmd == 'radio.on':
            radio.on()
            confirm()
        elif cmd == 'radio.off':
            radio.off()
            confirm()
        elif cmd == 'radio.reset':
            radio.reset()
            confirm()
        elif cmd == 'radio.send_bytes':
            radio.send_bytes(to_bytes(params[1]))
            confirm()
        elif cmd == 'radio.receive_bytes':
            msg = radio.receive_bytes()
            print(from_bytes(msg) if msg else '')
        elif cmd == 'speech.translate':
            print(escape(speech.translate(unescape(params[1]))))
        elif cmd == 'speech.pronounce':
            speech.pronounce(unescape(params[1]), \
                    pitch=int(params[2]), speed=int(params[3]), \
                    mouth=int(params[4]), throat=int(params[5]))
            confirm()
        elif cmd == 'speech.say':
            gc.collect()
            speech.say(unescape(params[1]), \
                    pitch=int(params[2]), speed=int(params[3]), \
                    mouth=int(params[4]), throat=int(params[5]))
            confirm()
        elif cmd == 'speech.sing':
            speech.sing(unescape(params[1]), \
                    pitch=int(params[2]), speed=int(params[3]), \
                    mouth=int(params[4]), throat=int(params[5]))
            confirm()
        elif cmd == 'speaker.on':
            speaker.on()
            confirm()
        elif cmd == 'speaker.off':
            speaker.off()
            confirm()
        elif cmd == 'microphone.sound_level':
            print(microphone.sound_level())
# mbv2_end
        else:
            print('ERROR: Unknown command.')
    except Exception as e:
        print('EXCEPTION: ' + str(e))
