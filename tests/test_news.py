"""Tests for function.news module."""

from unittest.mock import MagicMock, patch

import pytest

from function.news import fetch_news, print_news


class MockEntry:
    """Mock RSS feed entry with title attribute."""

    def __init__(self, title):
        self.title = title


class MockFeedParser:
    """Mock feedparser.parse return value."""

    def __init__(self, entries):
        self.entries = [MockEntry(e["title"]) if isinstance(e, dict) else e for e in entries]


class TestFetchNews:
    """Tests for fetch_news function."""

    @patch("function.news.feedparser.parse")
    def test_fetch_news_returns_list_of_titles(self, mock_parse, sample_rss_feed):
        mock_parse.return_value = MockFeedParser(sample_rss_feed["entries"])

        result = fetch_news(limit=3)

        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0] == "Breaking News: Test Headline One"
        assert result[1] == "Another Important Story Here"

    @patch("function.news.feedparser.parse")
    def test_fetch_news_respects_limit(self, mock_parse, sample_rss_feed):
        mock_parse.return_value = MockFeedParser(sample_rss_feed["entries"])

        result = fetch_news(limit=2)

        assert len(result) == 2

    @patch("function.news.feedparser.parse")
    def test_fetch_news_truncates_long_titles(self, mock_parse):
        long_title = "A" * 100
        mock_parse.return_value = MockFeedParser([{"title": long_title}])

        result = fetch_news(limit=1)

        # textwrap.shorten with width=84 and placeholder="..."
        assert len(result[0]) <= 84
        assert result[0].endswith("...")

    @patch("function.news.feedparser.parse")
    def test_fetch_news_empty_feed(self, mock_parse):
        mock_parse.return_value = MockFeedParser([])

        result = fetch_news(limit=5)

        assert result == []

    @patch("function.news.feedparser.parse")
    def test_fetch_news_uses_default_url(self, mock_parse, sample_rss_feed):
        mock_parse.return_value = MockFeedParser(sample_rss_feed["entries"])

        fetch_news()

        mock_parse.assert_called_once()
        args, kwargs = mock_parse.call_args
        assert "thehindu.com" in args[0]


class TestPrintNews:
    """Tests for print_news function."""

    @patch("function.news.fetch_news")
    def test_print_news_formats_output(self, mock_fetch_news, mock_printer):
        mock_fetch_news.return_value = ["Headline One", "Headline Two"]
        print_news(mock_printer)

        # Check print_title and hr were called via printer methods
        mock_printer.set.assert_called()
        mock_printer.text.assert_called()

    @patch("function.news.fetch_news")
    def test_print_news_empty_list(self, mock_fetch_news, mock_printer):
        mock_fetch_news.return_value = []
        print_news(mock_printer)

        # Should not print any headlines if none fetched
        mock_fetch_news.assert_called_once()

    @patch("function.news.fetch_news")
    def test_print_news_numbered_list(self, mock_fetch_news, mock_printer):
        mock_fetch_news.return_value = ["First", "Second", "Third"]
        print_news(mock_printer)

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "1. First" in output
        assert "2. Second" in output
        assert "3. Third" in output

    @patch("function.news.fetch_news")
    def test_print_news_custom_rss_url(self, mock_fetch_news, mock_printer):
        mock_fetch_news.return_value = ["Test"]
        print_news(mock_printer, rss_url="https://custom.feed/rss", limit=3)

        mock_fetch_news.assert_called_with("https://custom.feed/rss", 3)