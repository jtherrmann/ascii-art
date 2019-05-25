#!/usr/bin/env python3

import argparse
import math
import os
import sys

from PIL import Image


# TODO
# - break into smaller funcs

GRAYSCALE_PATH = 'grayscale.png'


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
    parser.add_argument(
        '-g', '--save-grayscale',
        action='store_true',
        help="save the intermediate grayscale image as '{}'".format(
            GRAYSCALE_PATH
        )
    )
    return parser.parse_args()


def add_default(help_str):
        return help_str + " (default: '%(default)s')"


def check_image_path(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("'{}' is not a file".format(path))
    return path


def resize_image(image, max_width):
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = round(ratio * image.height)
        return image.resize((max_width, new_height))
    return image


def convert_to_grayscale(image, save_grayscale):
    image = image.convert('L')
    if save_grayscale:
        image.save(GRAYSCALE_PATH, 'PNG')
    return image


def image_to_ascii(image, source_str):
    output_rows = (
        row_to_ascii(image, row, source_str) for row in range(image.height)
    )
    return '\n'.join(output_rows) + '\n'


def row_to_ascii(image, row, source_str):
    return ''.join(
        pixel_to_ascii(image.getpixel((col, row)), source_str)
        for col in range(image.width)
    )


def pixel_to_ascii(pixel, source_str):
    assert 0 <= pixel <= 255
    scale_factor = len(source_str) / 256
    scaled_pixel = math.floor(pixel * scale_factor)
    return source_str[scaled_pixel]


if __name__ == '__main__':
    version = sys.version_info
    assert (version.major, version.minor, version.micro) >= (3, 5, 3)

    args = parse_args()

    image = Image.open(args.image_path)
    image = resize_image(image, args.max_width)
    image = convert_to_grayscale(image, args.save_grayscale)

    output = image_to_ascii(image, args.source_str)
    with open(args.output_path, 'w+') as output_file:
        output_file.write(output)
