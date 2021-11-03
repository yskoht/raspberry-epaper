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
from raspberry_epaper.combine import combine
from raspberry_epaper.get_background_color import get_background_color

logging.basicConfig(level=logging.DEBUG)

VALID_IMAGE_TYPES = [
    'image/png',
    'image/jpeg',
]

VALID_TEXT_TYPES = [
    'text/plain',
]

VALID_TYPES = VALID_IMAGE_TYPES + VALID_TEXT_TYPES

def get_filepath(path):
    exts = ['jpg', 'jpeg', 'png', 'txt']
    filepaths = []
    for ext in exts:
        filepaths += glob.glob('{}/*.{}'.format(path, ext))
    random.shuffle(filepaths)
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
    if t in VALID_TYPES:
        return 'valid'

    return 'invalid'


def build_image(epd, image_filepath):
    foreImage = Image.open(image_filepath)
    backColor = get_background_color(foreImage)
    backImage = Image.new('1', (epd.width(), epd.height()), backColor)
    image = combine(foreImage, backImage)
    return image


def build_text_image(epd, text_filepath):
    font12 = ImageFont.truetype('./Font.ttc', 12)
    image = Image.new('1', (epd.width(), epd.height()), 255)
    text = ''
    with open(text_filepath) as f:
        text = f.read()
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font12, fill=0)
    return image


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
    if mimetype not in VALID_TYPES:
        print('Error: internal error', file=sys.stderr)
        sys.exit(1)

    try:
        epd = EPD(arg.device)
        epd.clear()

        if mimetype in VALID_IMAGE_TYPES:
            image = build_image(epd, filepath)
        elif mimetype in VALID_TEXT_TYPES:
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
