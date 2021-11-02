import random
import glob
import logging
import time
import traceback
import argparse
import os
import mimetypes
import sys
import qrcode

from PIL import Image,ImageDraw,ImageFont

from raspberry_epaper.epd import EPD
from raspberry_epaper.fitting import fitting
from raspberry_epaper.get_background_color import get_background_color

logging.basicConfig(level=logging.DEBUG)

valid_image_types = [
    'image/png',
    'image/jpeg',
]

valid_text_types = [
    'text/plain',
]

valid_types = valid_image_types + valid_text_types

def get_filepath(path):
    exts = ['jpg', 'jpeg', 'png', 'txt']
    filepaths = []
    for ext in exts:
        filepaths += glob.glob('{}/*.{}'.format(path, ext))
    random.shuffle(files)
    return filepaths[0]


def parse_arg():
    description = 'e-paper utility'
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-d',
        '--device',
        type=str,
        metavar='device',
        help='waveshare device'
    )
    parser.add_argument(
        '-q',
        '--qr',
        type=str,
        metavar='qr',
        help='QR code string'
    )
    parser.add_argument(
        'path',
        type=str,
        help='picture, directory or text file'
    )

    arg = parser.parse_args()
    return arg


def get_path_type(path):
    if not os.path.exists(path):
        return 'not_found'
    if os.path.isdir(path):
        return 'directory'

    t = mimetypes.guess_type(path)[0]
    if t in valid_types:
        return 'valid'

    return 'invalid'


def build_image(epd, image_filepath):
    foreImage = Image.open(image_filepath)
    backColor = get_background_color(foreImage)
    backImage = Image.new('1', (epd.width(), epd.height()), backColor)
    image = fitting(foreImage, backImage)
    return image


def build_text_image(epd, text_filepath):
    pass


def overlay_qr_code(image, qr):
    _qr_image = qrcode.make(qr)
    qr_image = _qr_image.resize((60, 60))
    _, height = image.size
    image.paste(qr_image, (5, height - 60 - 5))
    return image


def process():
    arg = parse_arg()
    path_type = get_path_type(arg.path)

    if path_type == 'not_found':
        print('Error: path dose not exist', file=sys.stderr)
        sys.exit(1)

    if path_type == 'invalid':
        print('Error: path is invalid', file=sys.stderr)
        sys.exit(1)

    if path_type == 'directory':
        filepath  = get_filepath(arg.path)
    else:
        filepath = arg.path

    mimetype = mimetypes.guess_type(filepath)[0]
    if mimetype not in valid_types:
        print('Error: internal error', file=sys.stderr)
        sys.exit(1)

    try:
        epd = EPD(arg.device)
        epd.clear()

        if mimetype in valid_image_types:
            image = build_image(epd, filepath)
        elif mimetype in valid_text_types:
            image = build_text_image(epd, filepath)

        if arg.qr is not None:
            image = overlay_qr_code(image, arg.qr)

        epd.display(image)
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.exit()
        exit()


def main():
    process()
