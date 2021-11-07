import logging
import time

import epaper


class EPD:
    @staticmethod
    def modules():
        return epaper.modules()

    def __init__(self, device):
        logging.debug("Initialize:{}".format(device))
        self.epdLib = epaper.epaper(device)
        self.epd = self.epdLib.EPD()

    def clear(self):
        logging.debug("Clear")
        self.epd.init()
        self.epd.Clear()
        time.sleep(1)

    def display(self, blackImage, colorImage=None):
        logging.debug("Display")
        if colorImage:
            self.epd.display(
                self.epd.getbuffer(blackImage), self.epd.getbuffer(colorImage)
            )
        else:
            self.epd.display(self.epd.getbuffer(blackImage))

    def sleep(self):
        logging.debug("Sleep")
        self.epd.sleep()

    def exit(self):
        logging.debug("Exit")
        self.epdLib.epdconfig.module_exit()

    def width(self):
        return self.epd.width

    def height(self):
        return self.epd.height
