import feedparser
import textwrap

# https://github.com/plenaryapp/awesome-rss-feeds
RSS_URL = "https://indianexpress.com/section/business/banking-and-finance/feed/"

feed = feedparser.parse(RSS_URL)

print("HEADLINES")
print("-" * 32)

for entry in feed.entries[:5]:
    title = textwrap.shorten(entry.title, width=84, placeholder="...")
    print(f"• {title}")