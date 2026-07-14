"""Tests for function.text_inp module."""

from unittest.mock import MagicMock

import pytest

from function.text_inp import print_text_input


class TestPrintTextInput:
    """Tests for print_text_input function."""

    def test_print_text_input_formats_with_hr(self, mock_printer):
        print_text_input(mock_printer, "Hello, World!")

        # Check hr() called twice (before and after text)
        assert mock_printer.text.call_count >= 2

        # Check text content
        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "Hello, World!" in output

    def test_print_text_input_empty_string(self, mock_printer):
        print_text_input(mock_printer, "")

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "--------------------------------" in output  # hr lines

    def test_print_text_input_multiline(self, mock_printer):
        print_text_input(mock_printer, "Line 1\nLine 2\nLine 3")

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "Line 1" in output
        assert "Line 2" in output
        assert "Line 3" in output

    def test_print_text_input_special_characters(self, mock_printer):
        print_text_input(mock_printer, "Test: @#$%^&*()")

        calls = [call.args[0] for call in mock_printer.text.call_args_list]
        output = "".join(calls)
        assert "@#$%^&*()" in output