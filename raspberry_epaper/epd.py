import logging
import time

import epaper

from raspberry_epaper.epd_core import EPDCore


class EPD:
    @staticmethod
    def modules():
        return epaper.modules()

    def __init__(self, device):
        logging.debug("Initialize:{}".format(device))
        self.device = device
        self.epdLib = epaper.epaper(device)
        self.epd_core = EPDCore(self.device, self.epdLib)

    def clear(self):
        logging.debug("Clear")
        self.epd_core.init()
        self.epd_core.Clear()
        time.sleep(1)

    def display(self, image1, image2=None):
        logging.debug("Display")
        self.epd_core.display(image1, image2)

    def sleep(self):
        logging.debug("Sleep")
        self.epd_core.sleep()

    def exit(self):
        logging.debug("Exit")
        self.epdLib.epdconfig.module_exit()

    @property
    def width(self):
        return self.epd_core.width

    @property
    def height(self):
        return self.epd_core.height
