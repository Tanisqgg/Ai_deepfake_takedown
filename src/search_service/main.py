from fastapi import FastAPI, Query
from .serpapi_client import search_web, search_youtube
from .extended_search import search_social_media, search_dark_web
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI(title="Search & Scraping Service")

class SearchResult(BaseModel):
    title: str
    link: str

@app.get("/web/", response_model=List[SearchResult])
def web_search(q: str = Query(..., description="Search query"), limit: int = 10):
    results = search_web(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/youtube/", response_model=List[SearchResult])
def youtube_search(q: str = Query(..., description="Search query"), limit: int = 5):
    results = search_youtube(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/social/", response_model=List[SearchResult])
def social_search(account: str = Query(..., description="Social media handle"), limit: int = 10):
    """Search known social media sites for posts mentioning the account."""
    results = search_social_media(account, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]

@app.get("/darkweb/", response_model=List[SearchResult])
def darkweb_search(q: str = Query(..., description="Search query"), limit: int = 10):
    """Search Tor-hidden services for the query."""
    results = search_dark_web(q, num=limit)
    return [SearchResult(title=t, link=l) for t, l in results]