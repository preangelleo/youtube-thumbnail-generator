import os
import sys
import pytest
import tempfile
from unittest.mock import Mock, patch, MagicMock
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.thumbnail_generator import ThumbnailGenerator


class TestThumbnailGenerator:
    """Test cases for ThumbnailGenerator class."""
    
    def test_initialization_without_api_key(self):
        """Test initialization without API key."""
        generator = ThumbnailGenerator()
        
        assert generator.width == 1280
        assert generator.height == 720
        assert generator.default_language == "auto"
        assert generator.enable_ai_optimization == False
        assert generator.text_optimizer is None
    
    def test_initialization_with_api_key(self):
        """Test initialization with API key."""
        generator = ThumbnailGenerator(
            gemini_api_key="test-key",
            enable_ai_optimization=True
        )
        
        assert generator.gemini_api_key == "test-key"
        assert generator.enable_ai_optimization == True
        # Text optimizer should be created
        assert generator.text_optimizer is not None
    
    def test_initialization_with_custom_dimensions(self):
        """Test initialization with custom dimensions."""
        generator = ThumbnailGenerator(width=1920, height=1080)
        
        assert generator.width == 1920
        assert generator.height == 1080
    
    def test_generate_basic_thumbnail(self):
        """Test basic thumbnail generation."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="Test Thumbnail",
                output_path=tmp.name
            )
            
            assert os.path.exists(output_path)
            
            # Check image properties
            image = Image.open(output_path)
            assert image.size == (1280, 720)
            assert image.mode in ["RGB", "RGBA"]
            
            # Cleanup
            os.unlink(output_path)
    
    def test_generate_with_solid_background(self):
        """Test thumbnail with solid background."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="Solid Background",
                output_path=tmp.name,
                background_type="solid",
                background_config={"color": "#FF0000"}
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_generate_with_gradient_background(self):
        """Test thumbnail with gradient background."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="Gradient Background",
                output_path=tmp.name,
                background_type="gradient",
                background_config={
                    "color1": "#FF0000",
                    "color2": "#0000FF",
                    "direction": "vertical"
                }
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_generate_with_pattern_background(self):
        """Test thumbnail with pattern background."""
        generator = ThumbnailGenerator()
        
        patterns = ["dots", "lines", "grid", "waves"]
        
        for pattern in patterns:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                output_path = generator.generate(
                    text=f"{pattern} Pattern",
                    output_path=tmp.name,
                    background_type="pattern",
                    background_config={
                        "pattern": pattern,
                        "color1": "#FFFFFF",
                        "color2": "#000000"
                    }
                )
                
                assert os.path.exists(output_path)
                os.unlink(output_path)
    
    def test_text_positions(self):
        """Test different text positions."""
        generator = ThumbnailGenerator()
        
        positions = ["center", "top", "bottom", (100, 100)]
        
        for position in positions:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                output_path = generator.generate(
                    text="Position Test",
                    output_path=tmp.name,
                    text_position=position
                )
                
                assert os.path.exists(output_path)
                os.unlink(output_path)
    
    def test_different_output_formats(self):
        """Test JPEG and PNG output formats."""
        generator = ThumbnailGenerator()
        
        formats = [".png", ".jpg", ".jpeg"]
        
        for fmt in formats:
            with tempfile.NamedTemporaryFile(suffix=fmt, delete=False) as tmp:
                output_path = generator.generate(
                    text="Format Test",
                    output_path=tmp.name,
                    quality=90
                )
                
                assert os.path.exists(output_path)
                assert output_path.endswith(fmt)
                os.unlink(output_path)
    
    def test_batch_generate(self):
        """Test batch thumbnail generation."""
        generator = ThumbnailGenerator()
        
        texts = ["Thumbnail 1", "Thumbnail 2", "Thumbnail 3"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generator.batch_generate(
                texts=texts,
                output_dir=tmpdir
            )
            
            assert len(paths) == 3
            
            for path in paths:
                assert os.path.exists(path)
                assert path.startswith(tmpdir)
    
    @patch('src.text_optimizer.genai')
    def test_ai_optimization_toggle(self, mock_genai):
        """Test AI optimization toggle functionality."""
        # Mock the Gemini API
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Optimized Text"
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Test with AI enabled
        generator = ThumbnailGenerator(
            gemini_api_key="test-key",
            enable_ai_optimization=True
        )
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            # Generate with AI enabled
            output_path = generator.generate(
                text="Original Text",
                output_path=tmp.name,
                enable_ai_optimization=True
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
            
            # Generate with AI disabled for this call
            output_path = generator.generate(
                text="Original Text",
                output_path=tmp.name,
                enable_ai_optimization=False
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_custom_font_size_and_color(self):
        """Test custom font size and color."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="Custom Font",
                output_path=tmp.name,
                font_size=100,
                font_color="#FF00FF"
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="",
                output_path=tmp.name
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_very_long_text(self):
        """Test handling of very long text."""
        generator = ThumbnailGenerator()
        
        long_text = "This is a very long text " * 20
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text=long_text,
                output_path=tmp.name,
                font_size=30
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_chinese_text(self):
        """Test handling of Chinese text."""
        generator = ThumbnailGenerator()
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            output_path = generator.generate(
                text="Python编程教程",
                output_path=tmp.name,
                target_language="zh"
            )
            
            assert os.path.exists(output_path)
            os.unlink(output_path)
    
    def test_output_directory_creation(self):
        """Test automatic output directory creation."""
        generator = ThumbnailGenerator()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "nested", "dir", "thumb.png")
            
            output_path = generator.generate(
                text="Nested Directory",
                output_path=nested_path
            )
            
            assert os.path.exists(output_path)
            assert os.path.exists(os.path.dirname(output_path))