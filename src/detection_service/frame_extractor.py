import cv2
import tempfile
from pytube import YouTube
from typing import List

def download_video(url: str) -> str:
    """Download a YouTube URL to a temp .mp4 file."""
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        out_path = tmp.name
    stream.download(filename=out_path)
    return out_path

def extract_frames(video_path: str, interval_s: float = 1.0) -> List[str]:
    """
    Extract frames every `interval_s` seconds.
    Returns list of file-paths to the JPEG frames.
    """
    vid = cv2.VideoCapture(video_path)
    fps = vid.get(cv2.CAP_PROP_FPS)
    step = int(fps * interval_s)
    frames = []
    idx = 0
    success, img = vid.read()
    while success:
        if idx % step == 0:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                frame_path = tmp.name
            cv2.imwrite(frame_path, img)
            frames.append(frame_path)
        success, img = vid.read()
        idx += 1
    vid.release()
    return frames