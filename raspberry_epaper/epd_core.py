INIT_FUNC = {
    "epd1in02": lambda epd: epd.Init(),
    "epd1in54_V2": lambda epd: epd.init(False),
    "epd1in54": lambda epd: epd.init(epd.lut_full_update),
    "epd2in9": lambda epd: epd.init(epd.lut_full_update),
    "epd2in13_V2": lambda epd: epd.init(epd.FULL_UPDATE),
    "epd2in13": lambda epd: epd.init(epd.lut_full_update),
    "epd2in66": lambda epd: epd.init(0),
    "epd3in7": lambda epd: epd.init(0),
}


def clear_with(color):
    return lambda epd: epd.Clear(color)


CLEAR_FUNC = {
    "epd1in54_V2": clear_with(0xFF),
    "epd1in54": clear_with(0xFF),
    "epd2in7": clear_with(0xFF),
    "epd2in7b": clear_with(0x00),
    "epd2in9_V2": clear_with(0xFF),
    "epd2in9d": clear_with(0xFF),
    "epd2in13_V2": clear_with(0xFF),
    "epd2in13": clear_with(0xFF),
    "epd2in13d": clear_with(0xFF),
    "epd3in7": lambda epd: epd.Clear(0xFF, 0),
}


def display1(epd, image1, _):
    epd.display(epd.getbuffer(image1))


def display2(epd, image1, image2):
    epd.display(epd.getbuffer(image1), epd.getbuffer(image2))


DISPLAY_FUNC = {
    "epd1in02": lambda epd, image1, _: epd.Display(epd.getbuffer(image1)),
    "epd1in54": display1,
    "epd1in54_V2": display1,
    "epd1in54b": display2,
    "epd1in54b_V2": display2,
    "epd1in54c": display2,
    "epd2in13": display1,
    "epd2in13_V2": display1,
    "epd2in13b_V3": display2,
    "epd2in13bc": display2,
    "epd2in13d": display1,
    "epd2in66": display1,
    "epd2in66b": display2,
    "epd2in7": display1,
    "epd2in7b": display2,
    "epd2in7b_V2": display2,
    "epd2in9": display1,
    "epd2in9_V2": display1,
    "epd2in9b_V3": display2,
    "epd2in9bc": display2,
    "epd2in9d": display1,
    "epd3in7": lambda epd, image1, _: epd.display_4Gray(epd.getbuffer_4Gray(image1)),
    "epd4in01f": display1,
    "epd4in2": display1,
    "epd4in2b_V2": display2,
    "epd4in2bc": display2,
    "epd5in65f": display1,
    "epd5in83": display1,
    "epd5in83_V2": display1,
    "epd5in83b_V2": display2,
    "epd5in83bc": display2,
    "epd7in5": display1,
    "epd7in5_HD": display1,
    "epd7in5_V2": display1,
    "epd7in5b_HD": display2,
    "epd7in5b_V2": display2,
    "epd7in5bc": display2,
}


class EPDCore:
    def __init__(self, device, epdLib):
        self.device = device
        self.epd = epdLib.EPD()

    def __init(self):
        init = INIT_FUNC.get(self.device, lambda epd: epd.init())
        init(self.epd)

    def __Clear(self):
        clear = CLEAR_FUNC.get(self.device, lambda epd: epd.Clear())
        clear(self.epd)

    def init(self):
        self.__init()

    def Clear(self):
        self.__Clear()

    def display(self, image1, image2=None):
        display = DISPLAY_FUNC.get(self.device, lambda epd: epd.display)

        display(self.epd, image1, image2)

    def sleep(self):
        self.epd.sleep()

    @property
    def width(self):
        return self.epd.width

    @property
    def height(self):
        return self.epd.height
