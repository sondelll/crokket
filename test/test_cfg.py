import os
import sys
sys.path.insert(0, os.curdir)

from src.cfg import model_str

def test_model_string():
    m_s = model_str()
    assert isinstance(m_s, str)
    assert "whisper" in m_s or "wav2vec" in m_s
