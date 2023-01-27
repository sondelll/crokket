from time import perf_counter

from src.recognize import CrokketRecognition
from src.io import TextOut, filename_cleanup, adaptive_open_audio


def main():
    start_time = perf_counter()
    filename= "./long_sound.wav"
    recog = CrokketRecognition()
    tscript = recog(filename)
    clean_name = filename_cleanup(filename)
    out = TextOut(clean_name, tscript)
    out.write()
    
    finished_time = perf_counter()
    seconds = finished_time-start_time
    (time, unit) = (seconds/60, "minutes") if seconds > 60 else (seconds, "seconds")
    print(f"Full transcribe run took {time} {unit}")
    # adaptive_open_audio(filename)
    

if __name__ == '__main__':
    main()
