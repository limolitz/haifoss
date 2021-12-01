# Haifoss

A project written to draw a specially compressed file from a network source on the Inkplate 10.

## Overview

The project is split up into two main parts. The client, written in Micropython, running on the Inkplate, and a tool which runs on a server, written in Python, and compresses files into a special format and writes that to a text file. This file then needs to be delivered by any regular webserver.

Since drawing every pixel is incredibly slow, the image is read line by line and coverted into line drawing operations, which are way faster. On the device, we then loop through every row and draw all lines in this column. Note that empty lines carry meaning in this file format (that there is no black pixel in this line).

## Installation

Clone the repo, and get the submodule:
```Bash
git clone https://github.com/wasmitnetzen/haifoss.git
git submodule init
git submodule update
```

Make a `venv` and install the requirements:

```Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Convert a file (default filename is `tab1.bmp`). It should be a file with the resolution of 825 x 1136 pixels (or smaller).

```Bash
./convert.py
```

Configure a webserver (e.g. Nginx, Apache) to deliver it.

Adjust the `config.json` from the sample with your Wifi and webserver data.

Copy the needed files to the Inkplate

```Bash
python3 ./Inkplate-micropython/pyboard.py --device /dev/ttyUSB0 -f cp config.json screen.py ./Inkplate-micropython/inkplate10.py :
```

Lauch the client on the Inkplate:

```Bash
make run
```
or

```Bash
python3 ./Inkplate-micropython/pyboard.py --device /dev/ttyUSB0 screen.py
```

If you are happy with the results, you can copy the `boot.py` file to the Inkplate, which will start the script on boot.

```Bash
python3 ./Inkplate-micropython/pyboard.py --device /dev/ttyUSB0 -f cp boot.py :
```

or

```Bash
make copy
```

## Troubleshooting

Reset flash

```Bash
esptool.py -p /dev/ttyUSB0 erase_flash
```

Install new firmware
```Bash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32spiram-20210902-v1.17.bin
```

## Resources

* New firmware: https://micropython.org/download/esp32spiram/
* InkPlate docs: https://inkplate.readthedocs.io/en/latest/get-started.html#micropython
