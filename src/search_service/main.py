import os
from fastapi import FastAPI, Query, UploadFile, File
from .serpapi_client import search_web, search_youtube
from .extended_search import search_social_media, search_dark_web
from .image_search import search_by_image
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI(title="Search & Scraping Service")

class SearchResult(BaseModel):
    title: str
    link: str

@app.get("/search/web/", response_model=List[SearchResult])
def web_search(q: str = Query(..., description="Search query"), limit: int = 10):
    results = search_web(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/search/youtube/", response_model=List[SearchResult])
def youtube_search(q: str = Query(..., description="Search query"), limit: int = 5):
    results = search_youtube(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/search/social/", response_model=List[SearchResult])
def social_search(account: str = Query(..., description="Social media handle"), limit: int = 10):
    """Search known social media sites for posts mentioning the account."""
    results = search_social_media(account, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/search/darkweb/", response_model=List[SearchResult])
def darkweb_search(q: str = Query(..., description="Search query"), limit: int = 10):
    """Search Tor-hidden services for the query."""
    results = search_dark_web(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]


@app.post("/search/image/", response_model=List[SearchResult])
async def image_search(file: UploadFile = File(...), limit: int = 5):
    """Search the web for matches to the uploaded image."""
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as fh:
        fh.write(await file.read())
    results = search_by_image(tmp_path, num=limit)
    os.remove(tmp_path)
    return [SearchResult(title=t, link=l) for t, l in results]