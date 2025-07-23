import uvicorn
from fastapi import FastAPI, UploadFile, File
from .fingerprint import extract_face_embedding, extract_voice_embedding

app = FastAPI(title="Identity Fingerprint Service")

@app.post("/face/")
async def face_fingerprint(file: UploadFile = File(...)):
    # save upload
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    emb = extract_face_embedding(path)
    return {"embedding": emb.tolist()}

@app.post("/voice/")
async def voice_fingerprint(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    emb = extract_voice_embedding(path)
    return {"embedding": emb.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
