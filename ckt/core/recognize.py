from .audio import AudioData
from .trpipe import TPipeline


class CrokketRecognition:
    def __init__(self, filepath: str, model_override:str = None) -> None:
        self.audio = AudioData(filepath)
        self.pipe = TPipeline(model_override)

    def transcript(self) -> str:
        return self.pipe(self.audio.audio)["text"]
