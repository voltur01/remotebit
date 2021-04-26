#!/bin/bash

# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Volodymyr Turanskyy

# PYTHONPATH allows importing modules directly without the package name.
# If a package was created, say 'remotebit', then the import statement
# would have been:
#   from remotebit.microbit import *
# i.e. different on the host and the micro:bit native.
# The goal of the project is to make the same code runnable on both.

CFG_FILE=~/.bashrc
MB_LIB_DIR=`pwd`'/remotebit'

if grep PYTHONPATH $CFG_FILE > /dev/null;
then
    sed -i 's|export PYTHONPATH=.*|export PYTHONPATH='"$MB_LIB_DIR"':$PYTHONPATH|' $CFG_FILE
else
    echo 'export PYTHONPATH='"$MB_LIB_DIR"':$PYTHONPATH' >> $CFG_FILE
fi
