from torch import cuda
from torch.backends import mps

USE_MPS = False


def get_acceleration_device():
    if cuda.is_available():
        d_str = "cuda:0"
        print(f"Using device: {d_str}")
        return d_str
    if USE_MPS and mps.is_available() and mps.is_built():
        d_str = "mps"
        print(f"Using device: {d_str}")
        return d_str
    d_str = "cpu"
    print(f"Using device: {d_str}")
    return d_str
