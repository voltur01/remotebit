#!/bin/bash

# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

echo 'generating microbit_v1_app.py'
sed '/mbv2_begin/,/mbv2_end/d' microbit_app.py > microbit_v1_app.py
uflash microbit_v1_app.py