import feedparser
import textwrap
from printer import hr, print_title

# https://www.thehindu.com/news/national/feeder/default.rss
DEFAULT_RSS_URL = "https://www.thehindu.com/news/national/feeder/default.rss"


def fetch_news(rss_url=DEFAULT_RSS_URL, limit=5):
    feed = feedparser.parse(rss_url)
    entries = []
    for entry in feed.entries[:limit]:
        title = textwrap.shorten(entry.title, width=84, placeholder="...")
        entries.append(title)
    return entries


def print_news(printer, rss_url=DEFAULT_RSS_URL, limit=5):
    entries = fetch_news(rss_url, limit)
    if not entries:
        return

    print_title(printer, "NEWS:")
    hr(printer)

    printer.set(align="left", bold=False, width=1, height=1)
    for i, title in enumerate(entries, 1):
        printer.text(f"{i}. {title}\n")
    printer.ln()