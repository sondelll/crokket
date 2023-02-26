import sys

from time import perf_counter

from src.core.recognize import CrokketRecognition
from src.core.io import TextOut, filename_cleanup
from .elements import startup_msg, path_selection
from ..runtime_utils import ensure_data_folder
from ..files.checker import is_usable_audio_path
from ..gui.app import CrokketGUIApp

class Interactive:
    def __init__(self) -> None:
        print(startup_msg())
        if self._is_direct_invoked():
            self._invoke()
            return
        if self._should_launch_gui():
            self._launch()
        else:
            self._fileselect()
            self._invoke()
            
    def _is_direct_invoked(self):
        try:
            self.p = sys.argv[1]
        except:
            self.p = ""
        return is_usable_audio_path(self.p)
    
    def _should_launch_gui(self) -> bool:
        user_input = input("Launch GUI?[Y/n]")
        return not "n" in user_input.strip()
    
    def _fileselect(self):
        if not is_usable_audio_path(self.p):
            self.p = path_selection()
        if not is_usable_audio_path(self.p):
            raise ValueError("Invalid path")
    
    def _invoke(self):
        ensure_data_folder()
        start_time = perf_counter()
        cr = CrokketRecognition(self.p)
        print("Transcribing audio, this can take a couple of minutes..\n")
        tscript = cr.transcript()
    
        clean_name = filename_cleanup(self.p)
        out = TextOut(clean_name, tscript)
        out.write()
    
        finished_time = perf_counter()
        seconds = finished_time-start_time
        (time, unit) = (seconds/60, "minutes") if seconds > 60 else (seconds, "seconds")
        print(f"Full transcribe run took {time} {unit}")
        
    def _launch(self):
        app = CrokketGUIApp()
        app.mainloop()
    
def get_app():
    return Interactive()