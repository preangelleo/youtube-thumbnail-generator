"""
YouTube Thumbnail Generator v2.2

A professional YouTube thumbnail generation library with three theme modes, intelligent Chinese/English 
text processing, smart line-breaking algorithms, and full color customization.

Features:
- Three Theme Modes: Dark, Light, Custom with automatic color defaults
- Full Color Customization: title_color, author_color parameters with hex support
- Dynamic Font Scaling: Auto-scaling based on text length (1-17 characters)
- Triangle Control: enable_triangle parameter for overlay management
- Custom Background Support: Use your own 1600x900 templates
- Chinese/English Optimization: 30% larger fonts for Chinese, optimal lengths guidance
- Smart Line-breaking: 9 chars for Chinese titles, intelligent English wrapping
- Professional Templates: All templates included automatically in package

Basic Usage:
    from youtube_thumbnail_generator import FinalThumbnailGenerator
    
    generator = FinalThumbnailGenerator("templates/professional_template.jpg")
    result = generator.generate_final_thumbnail(
        title="Your Amazing Title",
        author="Your Name", 
        theme="dark",  # "dark", "light", or "custom"
        title_color="#FFFFFF",  # Custom colors
        output_path="output.jpg"
    )
"""

__version__ = "2.5.0"
__author__ = "Leo Wang"
__email__ = "me@leowang.net"
__license__ = "MIT"

# Import main classes and functions
from .final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path, create_default_templates, optimize_for_youtube_api, generate_triangle_template, get_random_template_config, generate_random_thumbnail
from .text_png_generator import create_text_png
from .function_add_chapter import add_chapter_to_image

def get_default_template():
    """Get path to the default professional template"""
    return get_resource_path("templates/professional_template.jpg")

def init_templates():
    """Initialize default templates in current directory if needed"""
    return create_default_templates()

def create_generator(template_path=None, google_api_key=None):
    """创建缩略图生成器 - 支持模板路径和Gemini API key
    
    Args:
        template_path (str, optional): 模板文件路径。如果不提供，使用默认黑色模板
        google_api_key (str, optional): Gemini API key for title optimization.
                                       If not provided, tries environment variable GEMINI_API_KEY.
                                       For backwards compatibility, also checks GOOGLE_API_KEY.
                                       If unavailable, title optimization is disabled.
        
    Returns:
        FinalThumbnailGenerator: 缩略图生成器实例
        
    Example:
        # 使用默认模板
        generator = create_generator()
        
        # 使用自定义模板
        generator = create_generator('my_template.jpg')
        
        # 启用title优化功能
        generator = create_generator(google_api_key='your_gemini_api_key')
        
        # 或设置环境变量
        # export GEMINI_API_KEY=your_gemini_api_key
        generator = create_generator()  # 会自动从环境变量获取API key
    """
    return FinalThumbnailGenerator(template_path, google_api_key)

# Define what gets imported with "from youtube_thumbnail_generator import *"
__all__ = [
    'FinalThumbnailGenerator',
    'create_text_png', 
    'add_chapter_to_image',
    'get_default_template',
    'get_resource_path',
    'init_templates',
    'create_generator',
    'optimize_for_youtube_api',
    'generate_triangle_template',
    'get_random_template_config',
    'generate_random_thumbnail',
    '__version__'
]