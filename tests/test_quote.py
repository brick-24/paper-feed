"""Tests for quote module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from function.quote import print_quote


class TestPrintQuote:
    """Tests for print_quote function."""

    @patch("function.quote.requests.get")
    def test_print_quote_success(self, mock_get, mock_printer, sample_quote_data):
        """Test successful quote fetch and print."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_quote_data
        mock_get.return_value = mock_response

        print_quote(mock_printer)

        # Verify request was made
        mock_get.assert_called_once_with("http://api.quotable.io/random", timeout=10)

        # Verify printer methods called
        mock_printer.set.assert_called()
        mock_printer.text.assert_called()
        mock_printer.ln.assert_called()

        # Check quote content in output
        text_calls = [call[0][0] for call in mock_printer.text.call_args_list]
        output = "".join(text_calls)
        assert "QUOTE:" in output
        assert sample_quote_data["content"] in output
        assert sample_quote_data["author"] in output

    @patch("function.quote.requests.get")
    def test_print_quote_request_params(self, mock_get, mock_printer):
        """Test print_quote makes correct request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"content": "Test", "author": "Author"}
        mock_get.return_value = mock_response

        print_quote(mock_printer)

        mock_get.assert_called_once_with("http://api.quotable.io/random", timeout=10)

    @patch("function.quote.requests.get")
    def test_print_quote_propagates_api_error(self, mock_get, mock_printer):
        """Test print_quote propagates API errors."""
        mock_get.side_effect = Exception("API Error")

        # Should raise the exception
        with pytest.raises(Exception, match="API Error"):
            print_quote(mock_printer)