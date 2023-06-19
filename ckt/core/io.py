from pathlib import Path


class TextOut:
    def __init__(self, fp:str, text:str) -> None:
        self.p = Path(fp).resolve()
        
        self.text = text
        
    def write(self):
        if self.p.is_dir():
            p = self.p.joinpath("ckt_out.txt")
            p.write_text(self.text)
        else:
            self.p.write_text(self.text)


def filename_cleanup(name:str):
    if name.startswith("."):
        name = name[1:]
    if "." in name: # Has extension
        name = name.split(".")[0]
    if "/" in name: # Has multi-level path
        name = name.split("/")[-1]
    return name
