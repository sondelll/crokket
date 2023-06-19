from ...versioning import get_version_str

def startup_msg() -> str:
    bar = "|-----------------|"
    msg = f"{bar}\nCrokket\n{get_version_str()}\n{bar}\n"
    return msg

def path_selection() -> str:
    user_input = input("Enter path to wav file:\n")
    return user_input.strip()

def tabbed(s:str, level:int = 1):
    padding = ""
    for l in range(level):
        padding = padding + "  "
    return padding + s
