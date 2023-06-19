import yaml


def model_str() -> str:
    cfg = parse_yaml("./config/crokket.yml")
    if cfg['model'] == "w2v":
        return "facebook/wav2vec2-large-960h-lv60-self"
    elif cfg['model'] == "whisper":
        _model = "openai/whisper-"
        _size = cfg['model_size']
        return f"{_model}{_size}"
    

def parse_yaml(path:str):
    with open(path) as file:
        return yaml.load(file, yaml.FullLoader)