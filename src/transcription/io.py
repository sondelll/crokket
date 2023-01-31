class TextOut:
    def __init__(self, name:str, text:str, out_dir:str = "data/") -> None:
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


def filename_cleanup(name:str):
    if name.startswith("."):
        name = name[1:]
    if "." in name: # Has extension
        name = name.split(".")[0]
    if "/" in name: # Has multi-level path
        name = name.split("/")[-1]
    return name
