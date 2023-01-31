import yaml



def model_str() -> str:
    cfg = parse_yaml("./config/crokket.yml")
    _size = cfg["model_size"]
    return f"openai/whisper-{_size}"
    



def parse_yaml(path:str):
    with open(path) as file:
        return yaml.load(file, yaml.FullLoader)