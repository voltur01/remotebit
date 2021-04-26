#!/bin/bash

# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

for TEST_FILE in test_*.py;
do
    echo '------- '$TEST_FILE' -------'
    python3 $TEST_FILE
done
