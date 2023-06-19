import os
from pathlib import Path


def is_usable_audio_path(p:str) -> bool:
    path = Path(p)
    if path.suffix == ".wav" and path.is_file():
        return True
    else:
        return False
