from transformers import pipeline
from .acceleration import get_acceleration_device
from ..cfg import model_str

class TPipeline:
    def __init__(self) -> None:
        _device = get_acceleration_device()
        _model = model_str()
        self.pipe = pipeline(
        "automatic-speech-recognition", model=_model,
        chunk_length_s=30, device=_device, max_new_tokens=320
        )
        
    def __call__(self, long_audio) -> str:
        return self.pipe(long_audio)

