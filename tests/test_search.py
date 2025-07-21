from src.search_service.serpapi_client import search_web, search_youtube

def test_web_search_returns_list():
    res = search_web("OpenAI", num=2)
    assert isinstance(res, list)
    assert len(res) <= 2
    for title, link in res:
        assert isinstance(title, str)
        assert link.startswith("http")

def test_youtube_search_returns_list():
    res = search_youtube("Deepfake tutorial", num=3)
    assert isinstance(res, list)
    assert len(res) <= 3
    for title, link in res:
        assert isinstance(title, str)
        assert "youtube.com" in link or link.startswith("http")