import os
import base64
import serpapi
from serpapi.exceptions import HTTPError

API_KEY = os.getenv("SERPAPI_KEY")


def search_by_image(image_path: str, num: int = 5) -> list:
    """Reverse image search via SerpApi.

    Returns a list of (title, link) tuples. Empty list on failure or missing API
    key.
    """
    if not API_KEY:
        return []
    with open(image_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    params = {
        "engine": "google_reverse_image",
        "api_key": API_KEY,
        "image_content": content,
        "num": num,
    }
    try:
        results = serpapi.search(params)
    except HTTPError:
        return []

    # API returns results under "image_results" or similar
    hits = results.get("image_results", [])
    return [(r.get("title"), r.get("link")) for r in hits][:num]
