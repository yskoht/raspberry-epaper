import glob
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
    random.shuffle(filepaths)
    return filepaths[0]


def get_filepath_and_mimetype(path):
    path_type = get_path_type(path)

    if path_type == "not_found":
        print("Error: path dose not exist", file=sys.stderr)
        sys.exit(1)

    if path_type == "invalid":
        print("Error: path is invalid", file=sys.stderr)
        sys.exit(1)

    if path_type == "directory":
        filepath = get_filepath(path)
    else:
        filepath = arg.path

    mimetype = mimetypes.guess_type(filepath)[0]
    if mimetype not in VALID_FILE_TYPES:
        print("Error: internal error", file=sys.stderr)
        sys.exit(1)

    return (filepath, mimetype)
