from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from detection_service.main import app as detection_app
from identity_service.main import app as identity_app
from search_service.main import app as search_app

app = FastAPI(title="AI Deepfake Takedown")

# mount sub applications
app.mount("/detect", detection_app)
app.mount("/fingerprint", identity_app)
app.mount("/search", search_app)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("WebUI.html", {"request": request})
