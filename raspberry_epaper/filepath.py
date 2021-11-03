import glob
import logging
import mimetypes
import os
import random
import sys

from raspberry_epaper.valid_types import VALID_FILE_TYPES


def get_path_type(path):
    if not os.path.exists(path):
        return "not_found"
    if os.path.isdir(path):
        return "directory"

    t = mimetypes.guess_type(path)[0]
    if t in VALID_FILE_TYPES:
        return "valid"

    return "invalid"


def get_filepath(path):
    exts = ["jpg", "jpeg", "png", "txt"]
    filepaths = []
    for ext in exts:
        filepaths += glob.glob("{}/*.{}".format(path, ext))
    logging.debug("Number of files:{}".format(len(filepaths)))
    random.shuffle(filepaths)
    return filepaths[0]


def get_filepath_and_mimetype(path):
    path_type = get_path_type(path)
    logging.debug("Path type:{}".format(path_type))

    if path_type == "not_found":
        logging.error("Path dose not exist")
        sys.exit(1)

    if path_type == "invalid":
        logging.error("Path is invalid")
        sys.exit(1)

    if path_type == "directory":
        filepath = get_filepath(path)
    else:
        filepath = path
    logging.info("File path:{}".format(filepath))

    mimetype = mimetypes.guess_type(filepath)[0]
    logging.info("Mimetype:{}".format(mimetype))
    if mimetype not in VALID_FILE_TYPES:
        logging.error("Internal error")
        sys.exit(1)

    return (filepath, mimetype)
