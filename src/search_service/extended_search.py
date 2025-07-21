import os
from typing import List, Tuple


def search_social_media(account: str, num: int = 10) -> List[Tuple[str, str]]:
    """Placeholder for social media search.

    Ideally this would call APIs from Twitter, Instagram, Facebook, etc.
    Currently returns an empty list if the required API keys are missing.
    """
    # TODO: integrate with real social network APIs
    return []


def search_dark_web(query: str, num: int = 10) -> List[Tuple[str, str]]:
    """Placeholder for dark web search using Tor-hidden service APIs."""
    # TODO: integrate with dark web search engine such as Ahmia
    return []
