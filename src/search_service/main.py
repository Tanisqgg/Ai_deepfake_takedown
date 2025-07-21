from fastapi import FastAPI, Query
from serpapi_client import search_web, search_youtube
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