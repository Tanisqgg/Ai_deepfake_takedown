import cv2
import tempfile
from pytube import YouTube
from typing import List
import os

def download_video(url: str) -> str:
    """Download a YouTube URL to a temp .mp4 file."""
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    out_path = tempfile.mktemp(suffix=".mp4")
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
            frame_path = tempfile.mktemp(suffix=".jpg")
            cv2.imwrite(frame_path, img)
            frames.append(frame_path)
        success, img = vid.read()
        idx += 1
    vid.release()
    return frames