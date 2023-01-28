from os import listdir, mkdir
from os.path import isdir


def required_standard_folders():
    basedir = listdir("./data")
    if not isdir(basedir):
        mkdir("./data")