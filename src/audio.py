import numpy as np

def standard_audio_preprocess(audio:np.ndarray):
    audio = audio.astype(np.float32)
    try:
        audio = np.average(audio, 1)
    except Exception as e:
        print(e)
    audio_max = max(audio.min(), audio.max())
    audio = np.multiply(audio, 0.5/np.abs(audio_max))
    
    return audio