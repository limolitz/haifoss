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

Convert a file (default filename is `tab1.bmp`):
```Bash
./convert.py
```

Configure a webserver (e.g. Nginx, Apache) to deliver it.

Copy the needed files to the Inkplate

```Bash
make copy
```

or

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

## TODO

* Document autostart
