import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import (
    detect_language,
    validate_dimensions,
    sanitize_filename,
    parse_color
)


class TestLanguageDetection:
    """Test language detection utilities."""
    
    def test_detect_english_text(self):
        """Test detection of English text."""
        text = "This is an English sentence about Python programming"
        assert detect_language(text) == "en"
    
    def test_detect_chinese_text(self):
        """Test detection of Chinese text."""
        text = "这是一个关于Python编程的中文句子"
        assert detect_language(text) == "zh"
    
    def test_detect_mixed_text_english_dominant(self):
        """Test detection of mixed text with English dominant."""
        text = "This is English text with some 中文 characters"
        assert detect_language(text) == "en"
    
    def test_detect_mixed_text_chinese_dominant(self):
        """Test detection of mixed text with Chinese dominant."""
        text = "这是中文文本 with some English"
        assert detect_language(text) == "zh"
    
    def test_detect_empty_text(self):
        """Test detection of empty text."""
        assert detect_language("") == "en"  # Default to English
    
    def test_detect_numbers_only(self):
        """Test detection of numbers only."""
        assert detect_language("123456789") == "en"  # Default to English


class TestDimensionValidation:
    """Test dimension validation utilities."""
    
    def test_standard_dimensions(self):
        """Test standard YouTube dimensions."""
        assert validate_dimensions(1280, 720) == (1280, 720)
        assert validate_dimensions(1920, 1080) == (1920, 1080)
        assert validate_dimensions(640, 360) == (640, 360)
    
    def test_non_standard_dimensions_close_to_16_9(self):
        """Test dimensions close to 16:9 ratio."""
        width, height = validate_dimensions(1270, 715)
        # Should round to nearest standard
        assert (width, height) == (1280, 720)
    
    def test_minimum_dimensions(self):
        """Test dimensions below minimum."""
        width, height = validate_dimensions(320, 180)
        # Should scale up to minimum
        assert width >= 640
        assert height >= 360
    
    def test_aspect_ratio_preservation(self):
        """Test aspect ratio is preserved."""
        original_ratio = 800 / 450
        width, height = validate_dimensions(800, 450)
        new_ratio = width / height
        assert abs(original_ratio - new_ratio) < 0.01


class TestFilenameUtilities:
    """Test filename sanitization utilities."""
    
    def test_sanitize_normal_filename(self):
        """Test sanitization of normal filename."""
        filename = "my_thumbnail.png"
        assert sanitize_filename(filename) == "my_thumbnail.png"
    
    def test_sanitize_filename_with_invalid_chars(self):
        """Test removal of invalid characters."""
        filename = "my<>thumbnail:*.png"
        sanitized = sanitize_filename(filename)
        assert "<" not in sanitized
        assert ">" not in sanitized
        assert ":" not in sanitized
        assert "*" not in sanitized
    
    def test_sanitize_filename_with_spaces(self):
        """Test replacement of spaces."""
        filename = "my thumbnail file.png"
        assert sanitize_filename(filename) == "my_thumbnail_file.png"
    
    def test_sanitize_long_filename(self):
        """Test truncation of long filename."""
        filename = "a" * 150 + ".png"
        sanitized = sanitize_filename(filename)
        assert len(sanitized) <= 104  # 100 + ".png"
    
    def test_sanitize_filename_preserves_extension(self):
        """Test that file extension is preserved."""
        filename = "my" * 60 + ".png"
        sanitized = sanitize_filename(filename)
        assert sanitized.endswith(".png")


class TestColorParsing:
    """Test color parsing utilities."""
    
    def test_parse_hex_color(self):
        """Test parsing of hex colors."""
        assert parse_color("#FF0000") == (255, 0, 0)
        assert parse_color("#00FF00") == (0, 255, 0)
        assert parse_color("#0000FF") == (0, 0, 255)
    
    def test_parse_short_hex_color(self):
        """Test parsing of 3-digit hex colors."""
        assert parse_color("#F00") == (255, 0, 0)
        assert parse_color("#0F0") == (0, 255, 0)
        assert parse_color("#00F") == (0, 0, 255)
    
    def test_parse_rgb_format(self):
        """Test parsing of rgb() format."""
        assert parse_color("rgb(255, 0, 0)") == (255, 0, 0)
        assert parse_color("rgb(0, 255, 0)") == (0, 255, 0)
        assert parse_color("rgba(0, 0, 255, 0.5)") == (0, 0, 255)
    
    def test_parse_named_colors(self):
        """Test parsing of named colors."""
        assert parse_color("white") == (255, 255, 255)
        assert parse_color("black") == (0, 0, 0)
        assert parse_color("red") == (255, 0, 0)
        assert parse_color("green") == (0, 255, 0)
        assert parse_color("blue") == (0, 0, 255)
    
    def test_parse_invalid_color(self):
        """Test parsing of invalid color defaults to white."""
        assert parse_color("invalid") == (255, 255, 255)
        assert parse_color("") == (255, 255, 255)
    
    def test_parse_case_insensitive(self):
        """Test case-insensitive color parsing."""
        assert parse_color("WHITE") == (255, 255, 255)
        assert parse_color("Black") == (0, 0, 0)
        assert parse_color("ReD") == (255, 0, 0)