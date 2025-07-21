import numpy as np
from deepface import DeepFace

def match_faces(
    img1_path: str,
    img2_path: str,
    threshold: float = 0.7,
    enforce_detection: bool = False,            # <— allow skipping
) -> tuple[bool, float]:
    """
    Compare two face images. Returns (matched, similarity).
    If a face can’t be detected, returns (False, 0.0).
    """
    try:
        emb1 = np.array(
            DeepFace.represent(
                img1_path,
                model_name="Facenet",
                enforce_detection=enforce_detection
            )[0]["embedding"]
        )
        emb2 = np.array(
            DeepFace.represent(
                img2_path,
                model_name="Facenet",
                enforce_detection=enforce_detection
            )[0]["embedding"]
        )
    except ValueError:
        # no face found → treat as non-match
        return False, 0.0

    sim = float(emb1.dot(emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
    return sim >= threshold, sim