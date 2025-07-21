import numpy as np
from pathlib import Path
from src.identity_service.fingerprint import extract_face_embedding, extract_voice_embedding

# base directory of this test file
BASE = Path(__file__).parent

def test_face_embedding_shape():
    img_path = BASE / "sample_face.jpg"
    assert img_path.exists(), f"Missing test image: {img_path}"
    emb = extract_face_embedding(str(img_path))
    assert isinstance(emb, np.ndarray)
    assert emb.shape[0] == 128

def test_voice_embedding_shape():
    wav_path = BASE / "sample_voice.wav"
    assert wav_path.exists(), f"Missing test audio: {wav_path}"
    emb = extract_voice_embedding(str(wav_path))
    assert isinstance(emb, np.ndarray)
    # adjust this if your encoder returns a different size
    assert emb.shape[0] == 256