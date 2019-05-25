#!/usr/bin/env python3

import argparse
import math
import os
import sys
import time
from datetime import datetime

from PIL import Image


# TODO
# - do something with saved resized/grayscale image
# - add test for single-char kirby (chars = ' .')
# - break into smaller funcs


def pixel_to_ascii(pixel, chars):
    assert 0 <= pixel <= 255
    scale_factor = len(chars) / 256
    scaled_pixel = math.floor(pixel * scale_factor)
    return chars[scaled_pixel]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_path', type=check_image_path, help='path to input image'
    )
    parser.add_argument(
        'max_width', type=int, help='maximum width for the output'
    )
    parser.add_argument(
        '-o', '--output-path',
        default='output.txt',
        help=add_default('path to the output file')
    )
    parser.add_argument(
        '-s', '--source-str',
        default=' .:',
        help=add_default(
            'string of chars to use for the output, ordered from darkest to '
            'lightest'
        )
    )
    return parser.parse_args()


def add_default(help_str):
        return help_str + " (default: '%(default)s')"


def check_image_path(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("'{}' is not a file".format(path))
    return path


if __name__ == '__main__':
    version = sys.version_info
    assert (version.major, version.minor, version.micro) >= (3, 5, 3)

    args = parse_args()

    image = Image.open(args.image_path)
    if image.width > args.max_width:
        ratio = args.max_width / image.width
        new_height = round(ratio * image.height)
        image = image.resize((args.max_width, new_height))

    image = image.convert('L')  # convert to grayscale
    grayscale_path = os.path.join(
        os.path.dirname(args.image_path), 'grayscale.png'
    )
    image.save(grayscale_path, 'PNG')  # save for debugging

    print('start: {}'.format(datetime.now().strftime('%H:%M:%S')))
    t1 = time.time()

    output_rows = []
    for y in range(image.height):
        output_row = ''
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            output_row += pixel_to_ascii(pixel, args.source_str)
        output_rows.append(output_row)
    output = '\n'.join(output_rows) + '\n'

    t2 = time.time()
    print('end: {}\n'.format(datetime.now().strftime('%H:%M:%S')))
    total_time = round((t2 - t1) * 1000)
    print('time: {} ms'.format(total_time))

    with open(args.output_path, 'w+') as output_file:
        output_file.write(output)
