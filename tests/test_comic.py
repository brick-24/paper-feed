"""Tests for function.comic module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from function.comic import download_xkcd, print_xkcd


class TestDownloadXKCD:
    """Tests for download_xkcd function."""

    @patch("function.comic.requests.get")
    @patch("function.comic.tempfile.NamedTemporaryFile")
    @patch("function.comic.Image.open")
    def test_download_xkcd_success(self, mock_image_open, mock_tempfile, mock_get):
        # Mock XKCD API response
        mock_api = MagicMock()
        mock_api.json.return_value = {
            "safe_title": "Test Comic",
            "num": 1234,
            "img": "https://imgs.xkcd.com/comics/test.png",
        }
        mock_api.raise_for_status = MagicMock()

        # Mock image response
        mock_img = MagicMock()
        mock_img.content = b"fake image data"
        mock_img.raise_for_status = MagicMock()

        mock_get.side_effect = [mock_api, mock_img]

        # Mock temp file
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/test_comic.png"
        mock_temp.__enter__ = MagicMock(return_value=mock_temp)
        mock_temp.__exit__ = MagicMock(return_value=None)
        mock_tempfile.return_value = mock_temp

        # Mock PIL Image
        mock_pil = MagicMock()
        mock_pil.convert.return_value = mock_pil  # convert returns self for chaining
        mock_image_open.return_value = mock_pil

        result = download_xkcd()

        assert result["title"] == "Test Comic"
        assert result["num"] == 1234
        assert result["image_path"] == Path("/tmp/test_comic.png")
        mock_pil.convert.assert_called_with("L")
        mock_pil.save.assert_called()

    @patch("function.comic.requests.get")
    def test_download_xkcd_api_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")

        with pytest.raises(Exception, match="API error"):
            download_xkcd()

    @patch("function.comic.requests.get")
    def test_download_xkcd_image_download_failure(self, mock_get):
        mock_api = MagicMock()
        mock_api.json.return_value = {
            "safe_title": "Test",
            "num": 1,
            "img": "https://example.com/img.png",
        }
        mock_api.raise_for_status = MagicMock()

        mock_img = MagicMock()
        mock_img.raise_for_status.side_effect = Exception("Image download failed")

        mock_get.side_effect = [mock_api, mock_img]

        with pytest.raises(Exception, match="Image download failed"):
            download_xkcd()


class TestPrintXKCD:
    """Tests for print_xkcd function."""

    @patch("function.comic.download_xkcd")
    def test_print_xkcd_formats_output(self, mock_download, mock_printer):
        mock_download.return_value = {
            "title": "Test Comic",
            "num": 1234,
            "image_path": Path("/tmp/test.png"),
        }

        print_xkcd(mock_printer)

        mock_download.assert_called_once()
        mock_printer.set.assert_called()
        mock_printer.text.assert_called()
        mock_printer.image.assert_called_with(str(Path("/tmp/test.png")), center=True)
        mock_printer.ln.assert_called()

    @patch("function.comic.download_xkcd")
    def test_print_xkcd_includes_title_and_number(self, mock_download, mock_printer):
        mock_download.return_value = {
            "title": "Flying Cars",
            "num": 5678,
            "image_path": Path("/tmp/test.png"),
        }

        print_xkcd(mock_printer)

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "#5678" in output
        assert "Flying Cars" in output