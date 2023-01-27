from scipy.io.wavfile import read
import scipy.signal as sg
import numpy as np
from time import perf_counter

import torch

from .audio import standard_audio_preprocess
from .splits import SplitTimes
from .chunk import to_chunks
from .io import chunks_to_disk
from .ml import load_model

WHISPER_SAMPLE_RATE = 16000


class CrokketRecognition:
    def __init__(self, threshold:float = 0.066) -> None:
        self.threshold = threshold
        self.model = load_model("openai/whisper-small")

    def __call__(self, filename:str, disk_copy:bool = False) -> str:
        start_time = perf_counter()
        audio_file = read(filename)

        sa = SplitTimes(audio_file, threshold=self.threshold)
        split_list = sa.get_splits()
        
        raw_audio = audio_file[1]
        
        audio_content = standard_audio_preprocess(raw_audio)
        
        chunks = to_chunks(split_list, audio_content)
        if disk_copy:
            chunks_to_disk(filename, chunks, sa._sample_rate, out_dir="./data/temp")
        
        chunked_time = perf_counter()
        print(f"Took {round(chunked_time-start_time, 3)}s to load, analyze and chunk audio.")
        
        sample_rate = audio_file[0]
        downsample_factor = self.calculate_downsampling(sample_rate)
        chunks = [sg.decimate(x=cnk, q=downsample_factor, ftype='fir') for cnk in chunks]
        
        transcribed = self.transcribe_multi(chunks)
        
        return transcribed
    
    def transcribe_multi(self, chunks:list) -> str:
        outputs = []
        for _n, chunk in enumerate(chunks):
            try:
                output = self.model.transcribe(chunk, "sv", "transcribe")
                outputs.append(output['text'])
                print(f"Processed chunk {_n} of {len(chunks)}")
            except Exception as e:
                print("Transcription exception,\n", e)
        
        str_out = self.join_to_str(outputs)
        return str_out

    def calculate_downsampling(self, sample_rate:int) -> int:
        if sample_rate % WHISPER_SAMPLE_RATE != 0:
            raise ValueError("Float resampling not enabled.")
        return int(sample_rate/WHISPER_SAMPLE_RATE)
    
    def join_to_str(self, items:list[str]) -> str:
        output = ""
        for text in items:
            output = f"{output}{text}\n"
        return output
        
    