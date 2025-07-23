# AI Deepfake Takedown

This project provides a collection of FastAPI services to help detect potential deepfake content and locate unauthorized media online.

## Services

### Detection Service
Exposes endpoints for comparing uploaded samples:
- `POST /detect/face/` – compare two face images
- `POST /detect/voice/` – compare two audio clips
- `POST /detect/video/` – compare an image with frames extracted from a YouTube video

### Identity Service
Creates embeddings for later comparison:
- `POST /fingerprint/face/` – extract face embedding
- `POST /fingerprint/voice/` – extract voice embedding

### Search Service
Uses [SerpApi](https://serpapi.com/) for basic web and YouTube search and includes placeholder functions for social media and dark web search.
- `GET /search/web/` – web search
- `GET /search/youtube/` – YouTube search
- `GET /search/social/` – **stub** social media search
- `GET /search/darkweb/` – **stub** dark web search
- `POST /search/image/` – reverse image search (SerpApi)

Set the environment variable `SERPAPI_KEY` for search endpoints.

## Running Tests

Install dependencies (DeepFace, Resemblyzer, cv2, pytube, serpapi) and run:

```bash
pytest
```

Some tests are placeholders and require sample media files.
