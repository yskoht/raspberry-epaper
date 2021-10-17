import random
import glob
import logging
import time
import traceback

from PIL import Image,ImageDraw,ImageFont

from raspberry_epaper.epd import EPD
from raspberry_epaper.fitting import fitting
from raspberry_epaper.getBackgroundColor import getBackgroundColor

picdir = '/pic'

logging.basicConfig(level=logging.DEBUG)

def getImage():
    exts = ['jpg', 'jpeg', 'png']
    images = []
    for ext in exts:
        images += glob.glob('{}/*.{}'.format(picdir, ext))
    random.shuffle(images)
    return images[0]

def main():
    try:
        epd = EPD('epd7in5')

        logging.info("init and Clear")
        epd.clear()

        img = getImage()
        logging.info(img)

        foreImage = Image.open(img)
        backColor = getBackgroundColor(foreImage)
        backImage = Image.new('1', (epd.width(), epd.height()), backColor)
        blackImage = fitting(foreImage, backImage)

        epd.display(blackImage)

        logging.info("Goto Sleep...")
        epd.sleep()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.exit()
        exit()
