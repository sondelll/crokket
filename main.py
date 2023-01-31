from os import mkdir
from os.path import isdir
import sys

from src.transcription.recognize import CrokketRecognition
from src.transcription.io import TextOut, filename_cleanup

from time import perf_counter


def ensure_data_folder():
    basedir = "./data"
    if not isdir(basedir):
        mkdir("./data")


def main():
    start_time = perf_counter()
    try:
        filename=sys.argv[1]
    except:
        filename = "audio.wav"
    cr = CrokketRecognition(filename)
    tscript = cr.transcript()
    
    clean_name = filename_cleanup(filename)
    out = TextOut(clean_name, tscript)
    out.write()
    
    finished_time = perf_counter()
    seconds = finished_time-start_time
    (time, unit) = (seconds/60, "minutes") if seconds > 60 else (seconds, "seconds")
    print(f"Full transcribe run took {time} {unit}")
    

if __name__ == '__main__':
    ensure_data_folder()
    main()
