import logging
import requests
from requests.exceptions import RequestException
from socks import SOCKS5Error
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Tor SOCKS proxy
TOR_PROXY = {
    "http":  "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}

def fetch_via_tor(url: str, timeout: int = 15) -> str | None:
    """Fetch page over Tor, return HTML or None if unreachable."""
    try:
        resp = requests.get(url, proxies=TOR_PROXY, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except (SOCKS5Error, RequestException) as e:
        logging.warning("⚠️  Unable to fetch %s: %s", url, e)
        return None

def _resolve(base_url: str, path: str) -> str:
    parsed = urlparse(path)
    # 1) Absolute URLs stay absolute
    if parsed.scheme in ("http", "https"):
        return path

    # 2) Leading-slash paths become base_path + stripped
    if path.startswith("/"):
        return base_url.rstrip("/") + "/" + path.lstrip("/")

    # 3) All other relative paths use normal urljoin
    return urljoin(base_url, path)

def extract_links(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    out = set()
    for a in soup.find_all("a", href=True):
        full = _resolve(base_url, a["href"])
        out.add(full)
    return out

def extract_images(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    out = set()
    for img in soup.find_all("img", src=True):
        full = _resolve(base_url, img["src"])
        out.add(full)
    return out

def scrape_page(url: str):
    html = fetch_via_tor(url)
    if not html:
        return [], []
    links = extract_links(html, url)
    images = extract_images(html, url)
    return links, images

if __name__ == "__main__":
    # example test against a known-live onion
    target = "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"
    links, images = scrape_page(target)

    print(f"\n🔗 Links found on {target}:")
    for u in sorted(links):
        print("  ", u)

    print(f"\n🖼️  Images found on {target}:")
    for src in sorted(images):
        print("  ", src)
