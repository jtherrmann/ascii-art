#!/usr/bin/env python3

import argparse
import math
import os
import sys

from PIL import Image


GRAYSCALE_PATH = 'grayscale.png'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_path', type=check_image_path, help='path to input image'
    )
    parser.add_argument(
        'max_width', type=int, help='maximum width for the output'
    )
    parser.add_argument('-o', '--output-path', help='path to the output file')
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


def get_image(image_path, max_width):
    image = Image.open(args.image_path)

    if image.width > max_width:
        ratio = max_width / image.width
        new_height = round(ratio * image.height)
        image = image.resize((max_width, new_height))

    return image.convert('L')  # convert to grayscale


def image_to_ascii(image):
    output_rows = (row_to_ascii(image, row) for row in range(image.height))
    return '\n'.join(output_rows) + '\n'


def row_to_ascii(image, row):
    return ''.join(
        pixel_to_ascii(image.getpixel((col, row)))
        for col in range(image.width)
    )


def pixel_to_ascii_func(source_str):
    scale_factor = len(source_str) / 256

    def func(pixel):
        assert 0 <= pixel <= 255
        scaled_pixel = math.floor(pixel * scale_factor)
        return source_str[scaled_pixel]

    return func


if __name__ == '__main__':
    version = sys.version_info
    assert (version.major, version.minor, version.micro) >= (3, 5, 3)

    args = parse_args()

    global pixel_to_ascii
    pixel_to_ascii = pixel_to_ascii_func(args.source_str)

    image = get_image(args.image_path, args.max_width)
    if args.save_grayscale:
        image.save(GRAYSCALE_PATH, 'PNG')

    output = image_to_ascii(image)

    output_path = (
        os.path.splitext(os.path.basename(args.image_path))[0] + '.txt'
    ) if args.output_path is None else args.output_path

    with open(output_path, 'w+') as output_file:
        output_file.write(output)

    metadata_path = os.path.splitext(output_path)[0] + '.metadata'
    with open(metadata_path, 'w+') as metadata_file:
        metadata_file.write('')
