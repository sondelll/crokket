from torch import cuda, device
from torch.backends import mps


def get_acceleration_device():
    if cuda.is_available():
        d_str = "cuda:0"
        print(f"Using device: {d_str}")
        return device(d_str)
    if mps.is_available():
        d_str = "mps"
        print(f"Using device: {d_str}")
        return device(d_str)
    d_str = "cpu"
    print(f"Using device: {d_str}")
    return device(d_str)
