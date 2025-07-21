import os
import serpapi
from serpapi.exceptions import HTTPError

API_KEY = os.getenv("SERPAPI_KEY")

def search_web(query: str, num: int = 10) -> list:
    """
    Perform a web search via SerpApi and return a list of (title, link).
    Returns [] on missing API key or HTTP errors.
    """
    if not API_KEY:
        return []

    params = {
        "q": query,
        "num": num,
        "api_key": API_KEY,
    }
    try:
        results = serpapi.search(params)
    except HTTPError:
        return []
    organic = results.get("organic_results", [])
    return [(r.get("title"), r.get("link")) for r in organic]

def search_youtube(query: str, num: int = 5) -> list:
    """
    Perform a YouTube search via SerpApi and return a list of (title, link).
    Returns [] on missing API key or HTTP errors.
    """
    if not API_KEY:
        return []

    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": API_KEY,
        "num": num,
    }
    try:
        results = serpapi.search(params)
    except HTTPError:
        return []
    videos = results.get("video_results", [])
    return [(r.get("title"), r.get("link")) for r in videos]