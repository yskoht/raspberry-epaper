from enum import Enum


class Order(str, Enum):
    asc = "asc"
    desc = "desc"
    random = "random"
