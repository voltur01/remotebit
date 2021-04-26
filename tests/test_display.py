# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

intensity = 5
display.set_pixel(2, 2, intensity)
p = display.get_pixel(2, 2)
check(p == intensity, 'get_pixel value != set_pixel')

display.clear()
p = display.get_pixel(1, 1)
check(p == 0, 'get_pixel != 0 for clear screen')
p = display.get_pixel(2, 2)
check(p == 0, 'get_pixel != 0 for clear screen')

display.on()
check (display.is_on(), 'should be on')
display.off()
check (not(display.is_on()), 'should be off')
display.on()
l = display.read_light_level()
check (l > 0, 'shoudl be some light')

display.show(Image.HEART)
sleep(500)
display.show(Image.HEART_SMALL)
sleep(500)
display.show(Image.HAPPY)
sleep(500)
display.show(Image( '90000:'
                    '09000:'
                    '00900:'
                    '00090:'
                    '00009'))
sleep(500)
display.show(123)
display.show(4.5)
display.show("hi")
display.show(Image.ALL_CLOCKS)
