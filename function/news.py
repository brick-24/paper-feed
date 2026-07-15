"""RSS news headlines fetcher and printer."""

from __future__ import annotations

import textwrap

import feedparser

from printer import hr, print_title


# https://github.com/plenaryapp/awesome-rss-feeds
DEFAULT_RSS_URL = "https://www.thehindu.com/news/national/feeder/default.rss"


def fetch_news(rss_url: str = DEFAULT_RSS_URL, limit: int = 5) -> list[str]:
    """Fetch and parse RSS feed headlines.

    Args:
        rss_url: RSS feed URL.
        limit: Maximum number of headlines to return.

    Returns:
        List of headline strings (truncated to 84 chars).
    """
    feed = feedparser.parse(rss_url)
    entries = []
    for entry in feed.entries[:limit]:
        title = textwrap.shorten(entry.title, width=84, placeholder="...")
        entries.append(title)
    return entries


def print_news(printer, rss_url: str = DEFAULT_RSS_URL, limit: int = 5) -> None:
    """Print news headlines to thermal printer."""
    entries = fetch_news(rss_url, limit)
    if not entries:
        return

    print_title(printer, "NEWS:")
    hr(printer)

    printer.set(align="left", bold=False, width=1, height=1)
    for i, title in enumerate(entries, 1):
        printer.text(f"{i}. {title}\n")
    printer.ln()