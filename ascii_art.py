#!/usr/bin/env python3

import math
import os
import sys
import time
from datetime import datetime

from PIL import Image


# started with example string from
# https://robertheaton.com/2018/06/12/programming-projects-for-advanced-beginners-ascii-art/
#
# CHARS = ' `^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

# complete printable ascii:
#
#  !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~

# experimenting:
CHARS = ' .,:;/(@$#'

SCALE_FACTOR = len(CHARS) / 256


def pixel_to_ascii(pixel):
    assert 0 <= pixel <= 255
    scaled_pixel = math.floor(pixel * SCALE_FACTOR)

    return CHARS[scaled_pixel]


if __name__ == '__main__':
    version = sys.version_info
    assert (version.major, version.minor, version.micro) >= (3, 5, 3)

    assert os.path.isfile(sys.argv[1])
    path = sys.argv[1]
    max_width = int(sys.argv[2])

    image = Image.open(path)

    if image.width > max_width:
        ratio = max_width / image.width
        new_height = round(ratio * image.height)
        image = image.resize((max_width, new_height))

    image = image.convert('L')  # convert to grayscale
    grayscale_path = os.path.join(os.path.dirname(path), 'grayscale.png')
    image.save(grayscale_path, 'PNG')  # save for debugging

    print('start: {}'.format(datetime.now().strftime('%H:%M:%S')))
    t1 = time.time()

    output_rows = []
    for y in range(image.height):
        output_row = ''
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            output_row += pixel_to_ascii(pixel)
        output_rows.append(output_row)
    output = '\n'.join(output_rows) + '\n'

    t2 = time.time()
    print('end: {}\n'.format(datetime.now().strftime('%H:%M:%S')))
    total_time = round((t2 - t1) * 1000)
    print('time: {} ms'.format(total_time))

    with open('output.txt', 'w+') as output_file:
        output_file.write(output)
