"""
YouTube Thumbnail Generator v2.1

A professional YouTube thumbnail generation library with intelligent Chinese/English text processing,
smart line-breaking algorithms, and dynamic layout adjustments.

Features:
- Chinese/English differentiated text processing (30% larger fonts for Chinese)
- Smart line-breaking: 9 chars for Chinese titles, 20 for subtitles
- Triangle overlay integration into right-side images
- Dynamic layout with title repositioning when no subtitle provided
- Professional templates with PNG-based text rendering
- Multi-platform font support (Mac/Linux/RunPod/AWS)

Basic Usage:
    from youtube_thumbnail_generator import FinalThumbnailGenerator
    
    generator = FinalThumbnailGenerator("path/to/template.jpg")
    result = generator.generate_final_thumbnail(
        title="Your Amazing Title",
        subtitle="Optional subtitle",
        author="Your Name",
        logo_path="path/to/logo.png",
        right_image_path="path/to/image.jpg",
        output_path="output.jpg"
    )
"""

__version__ = "2.1.0"
__author__ = "Leo Wang"
__email__ = "leo@example.com"
__license__ = "MIT"

# Import main classes and functions
from .final_thumbnail_generator import FinalThumbnailGenerator
from .text_png_generator import create_text_png
from .function_add_chapter import add_chapter_to_image

# Define what gets imported with "from youtube_thumbnail_generator import *"
__all__ = [
    'FinalThumbnailGenerator',
    'create_text_png', 
    'add_chapter_to_image',
    '__version__'
]