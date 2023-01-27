# MIT License

# Copyright (c) 2022 Chidi Williams

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# NOTE:
# This code has been modified yes, but still very much based on CW's work. 
# The original implementation, in "Buzz", can be found at https://github.com/chidiwilliams/buzz,
# it's worth a look, and probably a star as well.

from transformers import WhisperProcessor, WhisperForConditionalGeneration
from typing import Optional, Union

import torch
import numpy as np
import whisper

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def load_model(model_id: str):
    processor = WhisperProcessor.from_pretrained(model_id)
    model = WhisperForConditionalGeneration.from_pretrained(model_id)

    return CoreTranscriber(processor, model)


class CoreTranscriber:
    SAMPLE_RATE = whisper.audio.SAMPLE_RATE
    N_SAMPLES_IN_CHUNK = whisper.audio.N_SAMPLES

    def __init__(self, processor: WhisperProcessor, model: WhisperForConditionalGeneration):
        self.processor = processor

        self.model = model
        self.model.to(device)

    def transcribe(self, audio: Union[str, np.ndarray], language: str, task: str, verbose: Optional[bool] = None):
        audio = torch.Tensor(audio).cuda(device)
        self.model.config.forced_decoder_ids = self.processor.get_decoder_prompt_ids(task=task, language=language)

        segments = []
        all_predicted_ids = []

        num_samples = audio.shape[0]
        seek = 0
        while seek < num_samples:
            chunk = torch.as_tensor(audio[seek: seek + self.N_SAMPLES_IN_CHUNK]).to("cpu")
            
            input_features:torch.Tensor = self.processor(audio=chunk, return_tensors="pt",
                                            sampling_rate=self.SAMPLE_RATE).input_features
            input_features = input_features.cuda(device)
            
            predicted_ids = self.model.generate(input_features, max_new_tokens=256).to("cpu")
            all_predicted_ids.extend(predicted_ids)

            text: str = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            if text.strip() != '':
                segments.append({
                    'start': seek / self.SAMPLE_RATE,
                    'end': min(seek + self.N_SAMPLES_IN_CHUNK, num_samples) / self.SAMPLE_RATE,
                    'text': text
                })

            seek += self.N_SAMPLES_IN_CHUNK
        
        t = self.processor.batch_decode(all_predicted_ids, skip_special_tokens=True)[0]
            
        return {
            'text': t,
            'segments': segments
        }
