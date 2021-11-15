import bisect
import glob
import logging
import mimetypes
import os
import random
import sys

from raspberry_epaper.type import Order
from raspberry_epaper.valid_types import VALID_FILE_TYPES

PREV_FILE = ".prev"


def get_path_type(path):
    if not os.path.exists(path):
        return "not_found"
    if os.path.isdir(path):
        return "directory"

    t = mimetypes.guess_type(path)[0]
    if t in VALID_FILE_TYPES:
        return "valid"

    return "invalid"


def readline(file):
    with open(file) as f:
        line = f.readline()
    return line.rstrip()


def write(file, s):
    with open(file, mode="w") as f:
        f.write(s)


def get_next_filepath(filepaths, prev, order):
    N = len(filepaths)
    i = bisect.bisect(filepaths, prev)
    if order == Order.desc:
        i = (i + N - 2) % N
    else:
        i = i % N
    return filepaths[i]


def get_filepath(path, order):
    exts = ["jpg", "jpeg", "png", "txt", "JPG", "JPEG", "PNG", "TXT"]
    filepaths = []
    for ext in exts:
        filepaths += glob.glob("{}/*.{}".format(path, ext))

    filepaths.sort()
    filepaths_len = len(filepaths)
    logging.debug("Number of files:{}".format(filepaths_len))

    logging.debug("Order:{}".format(order))
    if order == Order.random:
        random.shuffle(filepaths)
        return filepaths[0]

    prev_file = "{}/{}".format(path, PREV_FILE)
    logging.debug("Prev file:{}".format(prev_file))
    if not os.path.exists(prev_file):
        logging.debug("Prev file not found")
        filepath = filepaths[0]
    else:
        prev = readline(prev_file)
        logging.debug("Prev:{}".format(prev))
        filepath = get_next_filepath(filepaths, prev, order)

    write(prev_file, filepath)
    return filepath


def get_filepath_and_mimetype(path, order):
    path_type = get_path_type(path)
    logging.debug("Path type:{}".format(path_type))

    if path_type == "not_found":
        logging.error("Path dose not exist")
        sys.exit(1)

    if path_type == "invalid":
        logging.error("Path is invalid")
        sys.exit(1)

    if path_type == "directory":
        filepath = get_filepath(path, order)
    else:
        filepath = path
    logging.info("File path:{}".format(filepath))

    mimetype = mimetypes.guess_type(filepath)[0]
    logging.info("Mimetype:{}".format(mimetype))
    if mimetype not in VALID_FILE_TYPES:
        logging.error("Internal error")
        sys.exit(1)

    return (filepath, mimetype)
