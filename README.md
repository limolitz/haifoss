# Haifoss

A project written to draw a specially compressed file from a network source on the Inkplate 10.

## Overview

The project is split up into two main parts. The client, written in Micropython, running on the Inkplate, and a tool which runs on a server, written in Python, and compresses files into a special format and writes that to a text file. This file then needs to be delivered by any regular webserver.

Since drawing every pixel is incredibly slow, the image is read line by line and coverted into line drawing operations, which are way faster. On the device, we then loop through every row and draw all lines in this column. Note that empty lines carry meaning in this file format (that there is no black pixel in this line).

## Snippets

Copy a file

```Bash
python3 pyboard.py --device /dev/ttyUSB0 -f cp ../haifoss/config.json :
```

Manually run the tool:

```Bash
python3 pyboard.py --device /dev/ttyUSB0 ../haifoss/main.py
```

