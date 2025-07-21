import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path

from .face_match import cosine_similarity

def match_voices(wav1: str, wav2: str, threshold: float = 0.75):
    """
    Returns (is_match: bool, similarity: float).
    """
    wav1_proc = preprocess_wav(Path(wav1))
    wav2_proc = preprocess_wav(Path(wav2))
    encoder = VoiceEncoder()
    emb1 = encoder.embed_utterance(wav1_proc)
    emb2 = encoder.embed_utterance(wav2_proc)
    sim = cosine_similarity(emb1, emb2)
    return (sim >= threshold, sim)