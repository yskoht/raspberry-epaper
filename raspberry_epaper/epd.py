import epaper
import time

class EPD:
    def __init__(self, device):
        self.epdLib = epaper.epaper(device)
        self.epd = self.epdLib.EPD()

    def clear(self):
        self.epd.init()
        self.epd.Clear()
        time.sleep(1)

    def display(self, blackImage, colorImage=None):
        if colorImage:
            self.epd.display(
                self.epd.getbuffer(blackImage),
                self.epd.getbuffer(colorImage)
            )
        else:
            self.epd.display(
                self.epd.getbuffer(blackImage)
            )

    def sleep(self):
        self.epd.sleep()

    def exit(self):
        self.epdLib.epdconfig.module_exit()

    def width(self):
        return self.epd.width

    def height(self):
        return self.epd.height
