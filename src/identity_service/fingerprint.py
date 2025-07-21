from deepface import DeepFace
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

def extract_face_embedding(image_path: str) -> np.ndarray:
    """
    Given a face image, return a 512-dim embedding.
    """
    embedding = DeepFace.represent(img_path=image_path, model_name='Facenet')[0]['embedding']
    return np.array(embedding)

def extract_voice_embedding(audio_path: str) -> np.ndarray:
    """
    Given a WAV file, return a voice embedding.
    """
    wav = preprocess_wav(Path(audio_path))
    encoder = VoiceEncoder()
    embedding = encoder.embed_utterance(wav)
    return np.array(embedding)