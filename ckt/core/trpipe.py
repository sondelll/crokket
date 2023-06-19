from transformers import pipeline
from torch import cuda
from torch.backends import mps
from ..cfg import model_str


USE_MPS = False

def get_acceleration_device():
    if cuda.is_available():
        d_str = "cuda:0"
        print(f"Using device: {d_str}")
        return d_str
    if USE_MPS and mps.is_available() and mps.is_built():
        d_str = "mps"
        print(f"Using device: {d_str}")
        return d_str
    d_str = "cpu"
    print(f"Using device: {d_str}")
    return d_str


class TPipeline:
    def __init__(self, model_override:str = None) -> None:
        _device = get_acceleration_device()
        _model = model_str() if model_override is None else model_override
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=_model,
            chunk_length_s=30,
            device=_device,
            max_new_tokens=320,
        )

    def __call__(self, long_audio) -> str:
        return self.pipe(long_audio)
