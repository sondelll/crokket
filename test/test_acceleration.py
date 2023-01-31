import os
import sys
sys.path.insert(0, os.curdir)

import torch
from src.transcription.acceleration import get_acceleration_device

def test_acc_device_fetch():
    a_device = get_acceleration_device()
    assert isinstance(a_device, str)