from os import mkdir
from os.path import isdir
import sys


def ensure_data_folder():
    """Always run before doing ANYTHING so we don't do work for nothing
    """
    basedir = "./data"
    if not isdir(basedir):
        mkdir("./data")