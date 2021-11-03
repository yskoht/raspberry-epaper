import logging
import sys
import traceback

import qrcode
from PIL import Image, ImageDraw, ImageFont

from raspberry_epaper.combine import combine
from raspberry_epaper.epd import EPD
from raspberry_epaper.filepath import get_filepath_and_mimetype
from raspberry_epaper.get_background_color import get_background_color
from raspberry_epaper.valid_types import VALID_IMAGE_TYPES, VALID_TEXT_TYPES


def build_image(epd, image_filepath):
    foreImage = Image.open(image_filepath)
    backColor = get_background_color(foreImage)
    backImage = Image.new("1", (epd.width(), epd.height()), backColor)
    image = combine(foreImage, backImage)
    return image


def build_text_image(epd, text_filepath, font, font_size):
    logging.debug("Font:{}".format(font))
    logging.debug("Font size:{}".format(font_size))

    font = ImageFont.truetype(font, font_size)
    image = Image.new("1", (epd.width(), epd.height()), 255)
    text = ""
    with open(text_filepath) as f:
        text = f.read()
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=0)
    return image


def overlay_qr_code(image, qr):
    _qr_image = qrcode.make(qr)
    qr_image = _qr_image.resize((60, 60))
    _, height = image.size
    image.paste(qr_image, (5, height - 60 - 5))
    return image


def process(arg):
    logging.debug("Arguments:{}".format(arg))
    filepath, mimetype = get_filepath_and_mimetype(arg.path)

    try:
        epd = EPD(arg.device)
        epd.clear()

        if mimetype in VALID_IMAGE_TYPES:
            image = build_image(epd, filepath)
        elif mimetype in VALID_TEXT_TYPES:
            image = build_text_image(epd, filepath, arg.font, arg.font_size)

        if arg.qr is not None:
            image = overlay_qr_code(image, arg.qr)

        epd.display(image)
        epd.sleep()

    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        epd.exit()
        sys.exit(1)
