import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from detection_service.main import app as detection_app
from identity_service.main import app as identity_app
from search_service.main import app as search_app
from detection_service.face_match import match_faces
from detection_service.voice_match import match_voices

app = FastAPI(title="AI Deepfake Takedown")

# mount sub applications
app.mount("/detect", detection_app)
app.mount("/fingerprint", identity_app)
app.mount("/search", search_app)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("WebUI.html", {"request": request})


@app.post("/upload/face/")
async def upload_face(
    client: UploadFile = File(...),
    suspect: UploadFile = File(...),
    threshold: float = Form(0.7),
):
    """Check two uploaded images for a face match."""
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


@app.post("/upload/voice/")
async def upload_voice(
    client: UploadFile = File(...),
    suspect: UploadFile = File(...),
    threshold: float = Form(0.75),
):
    """Check two uploaded audio clips for a voice match."""
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
