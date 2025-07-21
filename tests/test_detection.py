import os
from src.detection_service.face_match import match_faces, cosine_similarity
from src.detection_service.voice_match import match_voices

def test_cosine_similarity_perfect():
    import numpy as np
    a = np.array([1,0,0])
    b = np.array([1,0,0])
    assert cosine_similarity(a,b) == 1.0

def test_match_faces_identical(tmp_path):
    # Copy your sample image into tmp_path as client.jpg & suspect.jpg
    # e.g. shutil.copy("tests/sample_face.jpg", tmp_path/"client.jpg")
    client = tmp_path/"client.jpg"
    suspect = tmp_path/"client.jpg"
    with open(client, "wb") as f: f.write(b"")  # replace with real image in your env
    matched, sim = match_faces(str(client), str(suspect), threshold=0.99)
    assert isinstance(matched, bool)
    assert 0.0 <= sim <= 1.0

def test_match_voices_shape(tmp_path):
    # Similar idea for audio files
    pass  # fill in when you have sample .wav files