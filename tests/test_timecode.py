"""Tests for timecode module."""

import pytest
from videotools.timecode import parse_timecode, format_timecode, validate_timecode


class TestParseTimecode:
    """Test parse_timecode function."""
    
    def test_parse_seconds(self):
        """Test parsing plain seconds."""
        assert parse_timecode("90") == 90.0
        assert parse_timecode("60") == 60.0
        assert parse_timecode("0") == 0.0
        assert parse_timecode("12.5") == 12.5
    
    def test_parse_mm_ss(self):
        """Test parsing MM:SS format."""
        assert parse_timecode("1:30") == 90.0
        assert parse_timecode("0:00") == 0.0
        assert parse_timecode("1:12") == 72.0
        assert parse_timecode("3:25") == 205.0
        assert parse_timecode("3:25.500") == pytest.approx(205.5)
        assert parse_timecode("60:00") == 3600.0  # 60 minutes = 1 hour
        assert parse_timecode("99:30") == 5970.0  # Large minutes work
    
    def test_parse_hh_mm_ss(self):
        """Test parsing HH:MM:SS format."""
        assert parse_timecode("0:01:30") == 90.0
        assert parse_timecode("1:00:00") == 3600.0
        assert parse_timecode("0:00:00") == 0.0
        assert parse_timecode("2:30:45") == 9045.0
        assert parse_timecode("0:00:12.250") == pytest.approx(12.25)
    
    def test_invalid_format(self):
        """Test invalid timecode formats."""
        with pytest.raises(ValueError):
            parse_timecode("invalid")
        with pytest.raises(ValueError):
            parse_timecode("1:2:3:4")
        with pytest.raises(ValueError):
            parse_timecode("1:60")  # Invalid seconds


class TestFormatTimecode:
    """Test format_timecode function."""
    
    def test_format_basic(self):
        """Test basic formatting."""
        assert format_timecode(90) == "00:01:30"
        assert format_timecode(0) == "00:00:00"
        assert format_timecode(3600) == "01:00:00"
        assert format_timecode(3661) == "01:01:01"
        assert format_timecode(12.5) == "00:00:12.500"


class TestValidateTimecode:
    """Test validate_timecode function."""
    
    def test_valid_timecodes(self):
        """Test valid timecode validation."""
        assert validate_timecode("0:00") is True
        assert validate_timecode("1:30") is True
        assert validate_timecode("0:01:30") is True
        assert validate_timecode("90") is True
    
    def test_invalid_timecodes(self):
        """Test invalid timecode validation."""
        assert validate_timecode("invalid") is False
        assert validate_timecode("1:60") is False
