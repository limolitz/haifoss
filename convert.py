#!/usr/bin/env python3

import sys
import argparse

from PIL import Image
from io import IOBase


def convert(input_file: IOBase, output_file: IOBase) -> None:
    image = Image.open(input_file)

    # TODO: check image size

    # convert to monochrome
    monochrome = image.convert('1')

    line_running = False
    line_start = 0

    output = []
    # loop through image
    for y in range(monochrome.height):
        line_output = ""
        for x in range(monochrome.width):
            # for the given pixel at w,h, lets check its value against the threshold
            pixel = monochrome.getpixel((x, y))
            if line_running:
                if pixel == 0:
                    pass
                elif pixel == 255:
                    print(f"{y}: Line started at {line_start}, stopped at {x}.")
                    line_running = False
                    line_output += f"{line_start}-{x},"
                else:
                    print(f"Unexpected pixel value {pixel}.")
                    return
            else:
                if pixel == 0:
                    print(f"{y}: Line started at {x}")
                    line_start = x
                    line_running = True
                elif pixel == 255:
                    pass
                else:
                    print(f"Unexpected pixel value {pixel}.", file=sys.stderr)
                    return

        if len(line_output) == 0:
            print(f"No black pixel in line {y}.")
        else:
            print(f"Line {y}: {line_output}")
            # cut off trailing comma
            line_output = line_output[:-1]
        output.append(line_output)

    for line in output:
        output_file.write(line)
        output_file.write('\n')


def main(input_file: IOBase, output_file: IOBase) -> None:
    convert(input_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert images into file format for Haifoss')
    parser.add_argument(
        'input', default="tab1.bmp", nargs='?', type=argparse.FileType('rb'),
        help='Path to the image file, default is "tab1.bmp"'
    )
    parser.add_argument(
        'output', default="tab1.txt", nargs='?', type=argparse.FileType('w'),
        help='Path to the output file, default is "tab1.txt"'
    )
    args = parser.parse_args()
    main(args.input, args.output)
