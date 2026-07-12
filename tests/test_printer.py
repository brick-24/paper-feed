"""Tests for printer module."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from printer import TerminalPrinter, create_printer, print_title, hr


class TestTerminalPrinter:
    """Tests for TerminalPrinter class."""

    def test_init_defaults(self):
        """Test TerminalPrinter initialization with defaults."""
        printer = TerminalPrinter()
        assert printer.WIDTH == 32
        assert printer.align == "left"

    def test_set_align_center(self, capsys):
        """Test setting alignment to center."""
        printer = TerminalPrinter()
        printer.set(align="center")
        printer.text("hello\n")
        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_set_align_left(self, capsys):
        """Test setting alignment to left."""
        printer = TerminalPrinter()
        printer.set(align="left")
        printer.text("hello\n")
        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_text_with_newline(self, capsys):
        """Test text method with newline."""
        printer = TerminalPrinter()
        printer.text("hello\n")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"

    def test_text_without_newline(self, capsys):
        """Test text method without newline."""
        printer = TerminalPrinter()
        printer.text("hello")
        captured = capsys.readouterr()
        assert captured.out == "hello"

    def test_image_method(self, capsys):
        """Test image method prints placeholder."""
        printer = TerminalPrinter()
        printer.image("/path/to/image.png")
        captured = capsys.readouterr()
        assert "[IMAGE: /path/to/image.png]" in captured.out

    def test_ln_method(self, capsys):
        """Test ln method prints newline."""
        printer = TerminalPrinter()
        printer.ln()
        captured = capsys.readouterr()
        assert captured.out == "\n"

    def test_center_alignment(self, capsys):
        """Test center alignment formatting."""
        printer = TerminalPrinter()
        printer.set(align="center")
        printer.text("centered\n")
        captured = capsys.readouterr()
        # Centered text should be padded to width 32
        assert "centered" in captured.out


class TestCreatePrinter:
    """Tests for create_printer function."""

    @patch("printer.Usb")
    def test_create_printer_returns_usb(self, mock_usb):
        """Test create_printer returns Usb instance."""
        mock_instance = MagicMock()
        mock_usb.return_value = mock_instance

        result = create_printer(0x0483, 0x5840)

        assert result == mock_instance
        mock_usb.assert_called_once_with(0x0483, 0x5840, in_ep=0x82, out_ep=0x04)


class TestPrintTitle:
    """Tests for print_title function."""

    def test_print_title_calls_printer_methods(self, mock_printer):
        """Test print_title calls printer methods correctly."""
        print_title(mock_printer, "TEST TITLE")

        # Check set was called for title formatting
        assert mock_printer.set.call_count >= 2
        # Check text was called with title
        mock_printer.text.assert_called()


class TestHr:
    """Tests for hr function."""

    def test_hr_prints_line(self, mock_printer):
        """Test hr prints horizontal rule."""
        hr(mock_printer)
        mock_printer.text.assert_called_with("--------------------------------\n")