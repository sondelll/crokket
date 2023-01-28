from time import perf_counter

from .audio import AudioData
from .trpipe import TPipeline


class CrokketRecognition:
    def __init__(self, filepath:str) -> None:
        self.audio = AudioData(filepath)
        self.pipe = TPipeline()

    def transcript(self) -> str:
        return self.pipe(self.audio.audio)["text"]
    
    