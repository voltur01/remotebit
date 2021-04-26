# simple demo with display and bottons

# pylint: disable=unused-wildcard-import
from microbit import *

while True:
    if button_a.was_pressed():
        display.clear()
        display.set_pixel(0, 1, 9)

    if button_b.was_pressed():
        display.clear()
        display.set_pixel(4, 1, 9)

    sleep(100)
    