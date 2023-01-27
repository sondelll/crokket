import numpy as np
from scipy.io import wavfile

from .fubar import UnchunkedException


class TextOut:
    def __init__(self, name:str, text:str, out_dir:str = "data/transcript") -> None:
        self.name = name
        self.text = text
        if not out_dir.endswith("/"):
            out_dir = out_dir + "/"
        self.out_dir = out_dir
        
    def write(self):
        with open(f"{self.out_dir}{self.name}.txt", 'w', encoding="utf-8") as file:
            file.write(self.text)
            file.flush()
            file.close()


def adaptive_open_audio(path:str):
    import matplotlib.pyplot as plt
    input_file = wavfile.read(path)
    print("Avg: ", np.average(input_file[1]))
    print("Max: ", np.max(input_file[1]))
    print("Min: ", np.min(input_file[1]))
    plt.plot(input_file[1])
    plt.show()

def chunks_to_disk(source_filename:str, chunks:list, sample_rate:int, out_dir:str):
    if len(chunks) < 1:
        raise UnchunkedException()
    
    _paths = []
    if not out_dir.endswith("/"):
        out_dir = f"{out_dir}/"
        
    for n, chunk in enumerate(chunks):
        pathname = _generate_chunkname(n, source_filename)
        full_path = f"{out_dir}{pathname}"
        wavfile.write(full_path, sample_rate, chunk)
        #print(f"Writing to {full_path}")
        _paths.append(full_path)
    return _paths

def _generate_chunkname(n:int, file_basename:str = "audio_chunk", extension:str = "wav"):
    file_basename = filename_cleanup(file_basename)
    return f"{file_basename}_{n}.{extension}"

def filename_cleanup(name:str):
    if name.startswith("."):
        name = name[1:]
    if "." in name: # Has extension
        name = name.split(".")[0]
    if "/" in name: # Has multi-level path
        name = name.split("/")[-1]
    return name
