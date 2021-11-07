from enum import Enum

from raspberry_epaper.epd import EPD


class Order(str, Enum):
    asc = "asc"
    desc = "desc"
    random = "random"


devices = {_: _ for _ in EPD.modules()}
Device = Enum("Device", devices)
