# social_and_dark.py
"""
Free-tier helpers for surface- & dark-web OSINT look-ups.

• search_social_media(account, num)   → recent posts for a public profile
• search_dark_web(query, num, use_tor) → .onion hits from Ahmia / OnionSearch via Tor
"""
from __future__ import annotations
import logging
import urllib.parse
from typing import List, Tuple

import requests  # ensure you have requests[socks] or pysocks installed

##########################
#  SOCIAL-MEDIA SCRAPERS #
##########################

def _twitter_posts(user: str, num: int) -> List[Tuple[str, str]]:
    """Scrape Tweets with snscrape – no API key required."""
    try:
        import snscrape.modules.twitter as sntwitter
    except ImportError:
        logging.warning("snscrape not installed → `pip install snscrape`")
        return []

    posts: List[Tuple[str, str]] = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(user).get_items()):
        if i >= num:
            break
        posts.append((
            tweet.content,
            f"https://twitter.com/{user}/status/{tweet.id}"
        ))
    return posts


def _instagram_posts(user: str, num: int) -> List[Tuple[str, str]]:
    """Grab public IG posts via instaloader (no login needed for public)."""
    try:
        import instaloader
    except ImportError:
        logging.warning("instaloader not installed → `pip install instaloader`")
        return []

    L = instaloader.Instaloader(
        download_pictures=False, download_videos=False,
        download_video_thumbnails=False, quiet=True,
    )
    posts: List[Tuple[str, str]] = []
    try:
        profile = instaloader.Profile.from_username(L.context, user)
        for i, post in enumerate(profile.get_posts()):
            if i >= num:
                break
            caption = (post.caption or "").strip().split("\n")[0][:120]
            posts.append((caption, post.url))
    except Exception as exc:
        logging.debug("Instagram scrape failed: %s", exc)
    return posts


PLATFORM_MAP = {
    "twitter":   _twitter_posts,
    "x":         _twitter_posts,
    "instagram": _instagram_posts,
    "ig":        _instagram_posts,
}


def search_social_media(account: str, num: int = 10) -> List[Tuple[str, str]]:
    """
    Fetch up to *num* recent public posts for an account.
    Expect **account** as "<platform>:<handle>", e.g. "twitter:OpenAI".
    """
    if ":" not in account:
        logging.error("account must be '<platform>:<handle>' (got %s)", account)
        return []

    platform, handle = account.split(":", 1)
    scraper = PLATFORM_MAP.get(platform.lower())
    if not scraper:
        logging.warning("No free scraper for platform '%s'", platform)
        return []
    return scraper(handle.lstrip("@"), num)


##########################
#     DARK-WEB SEARCH    #
##########################

# Tor SOCKS5 proxy (must be running locally on 127.0.0.1:9050)
TOR_PROXY = {
    "http":  "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}


def _ahmia_search(query: str, num: int, use_tor: bool = False) -> List[Tuple[str, str]]:
    """
    Query Ahmia's public JSON endpoint (clearnet).
    If use_tor=True, routes request through Tor.
    """
    url = (
        "https://ahmia.fi/search/"
        f"?q={urllib.parse.quote_plus(query)}&page=0&format=json"
    )
    kwargs = {"timeout": 15, **({"proxies": TOR_PROXY} if use_tor else {})}
    try:
        res = requests.get(url, **kwargs)
        res.raise_for_status()
        hits = res.json().get("results", [])[:num]
        return [(h.get("title") or h["link"], h["link"]) for h in hits]
    except Exception as exc:
        logging.debug("Ahmia fetch failed: %s", exc)
        return []


def _onionsearch(query: str, num: int) -> List[Tuple[str, str]]:
    """
    Use OnionSearch (scrapes multiple dark-web engines).
    """
    try:
        from onionsearch import OnionSearch
    except ImportError:
        logging.warning("onionsearch not installed → `pip install onionsearch`")
        return []

    engine = OnionSearch(query, limit=num)
    # .run() yields dicts {'link': url, 'title': '…', 'desc': '…'}
    return [(hit.get("title") or hit["link"], hit["link"]) for hit in engine.run()]


def search_dark_web(
    query: str,
    num: int = 10,
    use_tor: bool = False
) -> List[Tuple[str, str]]:
    """
    Search the dark web for *query*, returning up to *num* hits.
    - Ahmia (clearnet JSON) is always used without Tor.
    - OnionSearch hits are fetched via Tor if use_tor=True and only for .onion URLs.
    """
    # 1) Ahmia (clearnet) — never proxy this
    results = _ahmia_search(query, num, use_tor=False)

    # 2) If Ahmia didn't fill the list, back-fill via OnionSearch
    if len(results) < num:
        needed = num - len(results)
        onion_hits = _onionsearch(query, needed)

        for title, link in onion_hits:
            if link.lower().endswith(".onion") and use_tor:
                # fetch the .onion page through Tor to verify it's up
                try:
                    resp = requests.get(link, proxies=TOR_PROXY, timeout=15)
                    if resp.status_code == 200:
                        results.append((title, link))
                except Exception:
                    continue
            else:
                # non-.onion or Tor not desired: just append metadata
                results.append((title, link))

    # Deduplicate and trim to requested length
    seen, deduped = set(), []
    for title, link in results:
        if link not in seen:
            deduped.append((title, link))
            seen.add(link)
        if len(deduped) >= num:
            break

    return deduped
