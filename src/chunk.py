import numpy as np
import torch

from src.fubar import UnchunkedException

def to_chunks(indices:list[int], audio_content:np.ndarray, sample_rate:int = 48000):
    if len(indices) < 1:
        raise UnchunkedException()
    chunks = []
    progress = 0
    
    for split_point in indices:
        if split_point - progress < 0.75 * sample_rate:
            continue
        
        print(f"Creating chunk between sample {progress} and {split_point}")
        chunk = audio_content[progress:split_point]
        if len(chunk) > 0 and np.max(chunk) > 0.0:
            chunks.append(chunk)
        progress = split_point

    print(f"Creating final chunk between sample {indices[-1]} and {len(audio_content)}")
    final_chunk = audio_content[indices[-1]:]
    chunks.append(final_chunk)
    
    return chunks
    
    