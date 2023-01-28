import torch
from transformers import pipeline


class TPipeline:
    def __init__(self) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline(
        "automatic-speech-recognition", model="openai/whisper-large",
        chunk_length_s=30, device=device, max_new_tokens=320
        )
        
    def __call__(self, long_audio) -> str:
        return self.pipe(long_audio)

