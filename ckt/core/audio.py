import numpy as np
import torchaudio
import torch
import os
from pathlib import Path


class AudioData:
    def __init__(self, audio_path) -> None:
        self.metadata = torchaudio.info(audio_path)
        
        joined_path = Path(audio_path).resolve()
        
        file_load:tuple[torch.Tensor, int] = torchaudio.load(joined_path)
        audio = file_load[0]
        sample_freq = file_load[1]
        audio = torchaudio.functional.resample(audio, sample_freq, 16000)
        self.audio = np.average(audio.numpy(), 0)
        