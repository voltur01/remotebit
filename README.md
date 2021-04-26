# `remote:bit`
`remote:bit` is a remote Python execution library for [BBC micro:bit](https://microbit.org/).

`remote:bit` allows developing MicroPython code on your host computer using your
favorite Python IDE, running and debugging the code on the host computer 
while the micro:bit attached to USB executes all the commands.

Moreover, the resulting Python code can be copied to micro:bit and run there without modifications.

# Why `remote:bit`

The default [Python editor](https://python.microbit.org/v/2) for micro:bit:
- Is rather limited and unlike modern Python IDEs.
- Does not support code completion or debugging.
- Requires very slow workflow: edit in the browser -> download file -> copy it to the micro:bit -> potentially see a syntax error message and start from the beginning.

[Mu](https://codewith.mu/) editor is slightly better, but still it does not support debugging, thus does not eliminate the need to copy the file to the micro:bit after every change.

`remote:bit` is an attempt to bring proper Python environment and workflow to micro:bit to actually teach kids real world Python programming techniques.

# How `remote:bit` works

`remote:bit` has two components:
1. MicroPython application that runs on a micro:bit and accepts commands from the host computer via the USB.
1. Normal Python3 library for the host computer that closely follows the [MicroPython API](https://microbit-micropython.readthedocs.io/en/v2-docs/microbit_micropython_api.html) and translates it to commands to send to the micro:bit via the USB.

As the result it is possible to write and debug the MicroPython-like code on the host computer using any Python IDE, while controlling the micro:bit functions in real time. For example, a code running on the host computer that sets `pin0` to `1` would send the command to the micro:bit and the micro:bit would actually set it to `1`, thus e.g. light a connected LED right away.

It is possible to use `remote:bit` to simply control the micro:bit remotely for projects that expect the micro:bit to be connected to the computer via USB as well as develop the code on the computer then copy the same code to the micro:bit and disconnect it from the computer to run the same application on a battery.

# Requirements

1. A Linux host computer, e.g. Ubuntu or Raspberry Pi OS.
	
	_Note: It might work on Windows with few tweaks (see below), however it was not tested on Windows._
1. Python 3.6 or higher (needs f-Strings support).
1. pySerial Python package installed.
	
	`python3 -m pip install pyserial`

1. A Python IDE, e.g. Visual Studio Code with the Python extension.
1. BBC micro:bit v2 (there is a limited support for micro:bit v1, see below).
1. Python environment is configured by running the `configure.sh` script.

# Known limitations

* micro:bit UART is used for the communication between the host computer and the micro:bit, thus not available for applications running on the micro:bit.
* Some methods are not implemented, because they are not practical or seemed to be rarely used. Not complete list:
	* `neopixel`
	* All `microphone` methods except `sound_level`
	* All `os` methods except `uname`
	* `radio.config`, `radio.receive_bytes_into`, `radio.receive_full`
	* `SPI.write_readinto`
* Some methods are implemented on the host computer, thus may yield slightly different results.
* Because of the memory limitations, micro:bit v1 only supports the following: pins, buttons, display, music (short melodies, longer may result in memory allocation errors).


# How to

## Create and run a simple project

* Make sure you have all the requirements listed above met
* Connect the micro:bit
* Copy the `microbit_app/microbit_app.py` to the micro:bit using one of
	* [Python editor](https://python.microbit.org/v/2)
	* [Mu](https://codewith.mu/) editor
* Create a Python script in your IDE
* Run or debug the script in the IDE - micro:bit will execute the commands
* When you are happy with your script you may copy it to the micro:bit as usual

## Use micro:bit v1

* Install `uflash` Python package `python3 -m pip install uflash`
* Connect the micro:bit
* Goto the `microbit_app` folder in a terminal
* Run `./flash_to_mb_v1.sh`

	This will create a new `microbit_v1_app.py` file that is the v1 subset of `microbit_app.py`
	Then copy the file to the attached micro:bit using the `uflash` utility.

_Note: You can use [Python editor](https://python.microbit.org/v/2) or [Mu](https://codewith.mu/) editor to copy the `microbit_v1_app.py` as well._

## Distinguish host vs micro:bit

Use `os.uname()` to check the name of the system:
```
from microbit import *
import os

if os.uname().sysname == 'microbit':
	# micro:bit specific code
else:
	# host specific code, os.uname().sysname is 'remotebit'
```

## Connect multiple micro:bit's to the same computer

The script that needs to run on the micro:bit that is connected to the 2nd, 3rd, ... serial port needs to initialize the serial link at the top of the script by calling `init_mb_link(serial_name_str)`.

_Note: The call to `init_mb_link` is not portable, thus will not work on the micro:bit._

## Use on Windows

The `PYTHONPATH` user environment variable needs to be set to point to the `remotebit\remotebit` folder where `microbit.py` is located. See e.g. [this tutorial](https://www.tenforums.com/tutorials/121855-edit-user-system-environment-variables-windows.html).

Use of micro:bit v1 needs `microbit_v1_app.py` file to be generated using the `sed` utility which is not available on Windows. It can be created manually from the `microbit_app.py` by removing the lines between 

	# mbv2_begin

and

	# mbv2_end

lines.

The code assumes that micro:bit is connected to `COM7` serial port. If this is not the case,
the serial link needs to be initialized at the top of your script by calling `init_mb_link(serial_name_str)`.

_Note: The call to `init_mb_link` is not portable, thus will not work on the micro:bit._

## Troubleshoot

1. Sometimes the host computer reports that micro:bit is not connected or access permission denied, refreshing MICROBIT volume in the file manager usually helps.

1. If the micro:bit runs into an exception and goes into the Python prompt, pressing the micro:bit reset button usually helps.

1. Use `set_trace_serial(True)` to enable tracing of the messages to and from micro:bit to the console.

1. Use `set_raise(True)` to enable raising exceptions in case of a communication error so that your code can handle it instead of the program terminating right away.

1. You may need to run your editor or IDE from the terminal to make sure it inherits the PYTHONPATH environment variable to be able to support code completion for `remote:bit` modules, e.g. `code . &` to run Visual Studio Code in the current folder without blocking the terminal.

## Report issues

I use `remote:bit` with my son for tinkering and learning Python, so this is pretty much "works on my computer" level of quality now. Please report any issues in [Github](https://github.com/voltur01/remotebit/issues) if you are interested in `remote:bit` too so that we can make it better together.

# FAQ

## Why `remote:bit` is not a Python package?

A Python package introduces its own namespace, e.g. `import remotebit.microbit`, which makes it impossible to have the same Python code run on both the host computer and micro:bit. 

The ability to run MicroPython examples unchanged as well as deploy the resulting code to the micro:bit was one of the key design goals of `remote:bit`.

## What is the protocol used to communicate with the micro:bit?

The protocol is a custom very simple text based one, which makes it possible to see and understand the request-response series as well as debug using a terminal. Example:

```
-> display.set_pixel 2 2 5
<- ok
-> display.get_pixel 2 2
<- 5
```

`display.set_pixel` is the command name, `2 2 5` the list of parameters (x, y, brightness).

`ok` is the response for commands that do not return any value, `5` is an example of the result response (brightness).

Use `set_trace_serial(True)` to see all the messages sent to and from micro:bit in the console.
