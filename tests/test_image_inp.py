"""Tests for function.image_inp module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from function.image_inp import print_image_input


class TestPrintImageInput:
    """Tests for print_image_input function."""

    def test_print_image_input_success(self, mock_printer, temp_image_file):
        print_image_input(mock_printer, str(temp_image_file))

        mock_printer.image.assert_called_once_with(temp_image_file, center=True)
        mock_printer.ln.assert_called()

    def test_print_image_input_file_not_found(self, mock_printer):
        with pytest.raises(FileNotFoundError, match="Image not found"):
            print_image_input(mock_printer, "/nonexistent/path.png")

    def test_print_image_input_calls_hr(self, mock_printer, temp_image_file):
        print_image_input(mock_printer, str(temp_image_file))

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "--------------------------------" in output  # hr called

    def test_print_image_input_path_object(self, mock_printer, temp_image_file):
        print_image_input(mock_printer, Path(temp_image_file))

        mock_printer.image.assert_called_once()
        args, kwargs = mock_printer.image.call_args
        assert kwargs.get("center") is True