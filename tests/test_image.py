# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

from testing_utils import *

from microbit import *

#TODO: add actual checks as this is implemented on the host

im = Image.HEART.copy()
w = im.width()
h = im.height()
im2 = im.shift_left(1)
im3 = im.shift_right(1)
im4 = im.shift_up(1)
im5 = im.shift_down(1)
im6 = im.crop(1, 1, 2, 3)
im7 = im.invert()
im.fill(5)
im = Image.HEART.copy()
im8 = Image(5, 5)
im8.blit(im, 2, 2, 5, 5)

im_a = Image(5, 5)
im_a.fill(5)
im_b = Image(5, 5)
im_b.fill(3)

im = im_a + im_b
im = im_a + im_a
im = im_b * 2
