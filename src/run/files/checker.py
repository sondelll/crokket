import os

def is_usable_audio_path(p:str) -> bool:
    if p.endswith(".wav") and os.path.exists(p):
        return True
    else:
        return False
