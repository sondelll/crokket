import sys
from time import perf_counter

from src.transcription.recognize import CrokketRecognition
from src.transcription.io import TextOut, filename_cleanup



def main():
    start_time = perf_counter()
    filename=sys.argv[1]
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
    main()
