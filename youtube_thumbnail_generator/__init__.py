from .thumbnail_generator import ThumbnailGenerator
from .text_optimizer import TextOptimizer
from .background_manager import BackgroundManager
from .font_manager import FontManager

__version__ = "2.6.2"

# Backward compatibility function
def create_generator(**kwargs):
    """Create a ThumbnailGenerator instance (backward compatibility).
    
    This function is provided for backward compatibility with v2.5.x.
    New code should use ThumbnailGenerator directly.
    """
    return ThumbnailGenerator(**kwargs)

__all__ = [
    "ThumbnailGenerator",
    "TextOptimizer",
    "BackgroundManager",
    "FontManager",
    "create_generator",  # Added for backward compatibility
]