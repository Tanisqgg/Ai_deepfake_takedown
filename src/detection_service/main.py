import os
from fastapi import FastAPI, UploadFile, File, Form
from detection_service.face_match import match_faces
from detection_service.voice_match import match_voices
from detection_service.frame_extractor import download_video, extract_frames

app = FastAPI(title="Detection Service")

@app.post("/face/")
async def detect_face(
    client: UploadFile = File(...),
    suspect: UploadFile = File(...),
    threshold: float = Form(0.7),
):
    # save uploads
    tmp1 = f"/tmp/{client.filename}"
    tmp2 = f"/tmp/{suspect.filename}"
    with open(tmp1, "wb") as f:
        f.write(await client.read())
    with open(tmp2, "wb") as f:
        f.write(await suspect.read())

    matched, score = match_faces(tmp1, tmp2, threshold)

    os.remove(tmp1)
    os.remove(tmp2)
    return {"matched": matched, "similarity": score}

@app.post("/voice/")
async def detect_voice(
    client: UploadFile = File(...),
    suspect: UploadFile = File(...),
    threshold: float = Form(0.75),
):
    tmp1 = f"/tmp/{client.filename}"
    tmp2 = f"/tmp/{suspect.filename}"
    with open(tmp1, "wb") as f:
        f.write(await client.read())
    with open(tmp2, "wb") as f:
        f.write(await suspect.read())

    matched, score = match_voices(tmp1, tmp2, threshold)

    os.remove(tmp1)
    os.remove(tmp2)
    return {"matched": matched, "similarity": score}

@app.post("/video/")
async def detect_video(
    client: UploadFile = File(...),
    video_url: str = Form(...),
    threshold: float = Form(0.7),
    interval_s: float = Form(1.0),
):
    # save client image
    client_path = f"/tmp/{client.filename}"
    with open(client_path, "wb") as f:
        f.write(await client.read())

    # download & split video
    vid_path = download_video(video_url)
    frames = extract_frames(vid_path, interval_s)

    matches = []
    for idx, frame_path in enumerate(frames):
        matched, score = match_faces(client_path, frame_path, threshold)
        if matched:
            matches.append({"frame_index": idx, "similarity": score})
    os.remove(client_path)
    os.remove(vid_path)
    for fp in frames:
        os.remove(fp)
    return {"matches": matches}
