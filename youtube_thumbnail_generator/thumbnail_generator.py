import os
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw
from dotenv import load_dotenv

from .text_optimizer import TextOptimizer
from .background_manager import BackgroundManager
from .font_manager import FontManager
from .utils import detect_language, validate_dimensions, normalize_language_code

load_dotenv()


class ThumbnailGenerator:
    """Main class for generating YouTube thumbnails with optional AI optimization."""
    
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        enable_ai_optimization: Optional[bool] = None,
        default_language: str = "auto",
        width: int = 1280,
        height: int = 720,
    ):
        """Initialize the thumbnail generator.
        
        Args:
            gemini_api_key: API key for Gemini AI (optional)
            enable_ai_optimization: Whether to enable AI text optimization
            default_language: Default language for text optimization (en/zh/auto)
            width: Thumbnail width in pixels
            height: Thumbnail height in pixels
        """
        self.width = width
        self.height = height
        self.default_language = default_language
        
        # Initialize AI optimizer if configured
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        # Determine if AI should be enabled
        if enable_ai_optimization is None:
            # Check environment variable
            env_enable = os.getenv("ENABLE_AI_OPTIMIZATION", "false").lower()
            self.enable_ai_optimization = env_enable == "true" and bool(self.gemini_api_key)
        else:
            self.enable_ai_optimization = enable_ai_optimization and bool(self.gemini_api_key)
        
        # Initialize components
        self.text_optimizer = TextOptimizer(self.gemini_api_key) if self.enable_ai_optimization else None
        self.background_manager = BackgroundManager(width, height)
        self.font_manager = FontManager()
    
    def generate(
        self,
        text: str,
        output_path: str = "thumbnail.png",
        background_type: str = "gradient",
        background_config: Optional[Dict[str, Any]] = None,
        font_name: Optional[str] = None,
        font_size: int = 72,
        font_color: str = "#FFFFFF",
        text_position: str = "center",
        enable_ai_optimization: Optional[bool] = None,
        source_language: Optional[str] = None,  # User-specified input language
        target_language: Optional[str] = None,  # For translation (only with AI)
        custom_prompt: Optional[str] = None,
        quality: int = 95,
    ) -> str:
        """Generate a YouTube thumbnail.
        
        Args:
            text: The text to display on the thumbnail
            output_path: Path to save the thumbnail
            background_type: Type of background (solid/gradient/image)
            background_config: Configuration for the background
            font_name: Font to use for the text
            font_size: Size of the text
            font_color: Color of the text
            text_position: Position of the text (center/top/bottom)
            enable_ai_optimization: Override default AI optimization setting
            source_language: Explicitly specify input language (en/zh) to skip detection
            target_language: Target language for translation (only used with AI optimization)
            custom_prompt: Custom prompt for AI optimization
            quality: JPEG/PNG quality (1-100)
        
        Returns:
            Path to the generated thumbnail
        """
        # Determine if AI optimization should be used for this generation
        use_ai = self.enable_ai_optimization if enable_ai_optimization is None else enable_ai_optimization
        use_ai = use_ai and self.text_optimizer is not None
        
        # Determine source language
        if source_language:
            # User explicitly specified the language - normalize and skip detection
            detected_language = normalize_language_code(source_language)
        else:
            # Auto-detect language
            detected_language = detect_language(text)
        
        # Optimize text if AI is enabled
        optimized_text = text
        if use_ai:
            # Determine optimization target language
            # If target_language is specified and different from source, it's translation
            # Otherwise, optimize in the same language
            optimization_language = normalize_language_code(target_language) if target_language else detected_language
            
            # Optimize the text
            optimized_text = self.text_optimizer.optimize(
                text,
                source_language=detected_language,
                target_language=optimization_language,
                custom_prompt=custom_prompt
            )
        
        # Create the background
        image = self.background_manager.create_background(
            background_type,
            background_config or {}
        )
        
        # Get the font
        font = self.font_manager.get_font(font_name, font_size)
        
        # Draw the text
        draw = ImageDraw.Draw(image)
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), optimized_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        if text_position == "center":
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
        elif text_position == "top":
            x = (self.width - text_width) // 2
            y = 50
        elif text_position == "bottom":
            x = (self.width - text_width) // 2
            y = self.height - text_height - 50
        else:
            # Custom position as tuple
            if isinstance(text_position, tuple) and len(text_position) == 2:
                x, y = text_position
            else:
                x = (self.width - text_width) // 2
                y = (self.height - text_height) // 2
        
        # Draw text with shadow for better visibility
        shadow_offset = 3
        draw.text(
            (x + shadow_offset, y + shadow_offset),
            optimized_text,
            font=font,
            fill="#000000"
        )
        draw.text((x, y), optimized_text, font=font, fill=font_color)
        
        # Save the image
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            image = image.convert("RGB")
            image.save(output_path, "JPEG", quality=quality, optimize=True)
        else:
            image.save(output_path, "PNG", quality=quality, optimize=True)
        
        return output_path
    
    def batch_generate(
        self,
        texts: list,
        output_dir: str = "thumbnails",
        **kwargs
    ) -> list:
        """Generate multiple thumbnails in batch.
        
        Args:
            texts: List of texts for thumbnails
            output_dir: Directory to save thumbnails
            **kwargs: Additional arguments for generate()
        
        Returns:
            List of paths to generated thumbnails
        """
        os.makedirs(output_dir, exist_ok=True)
        paths = []
        
        for i, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"thumbnail_{i+1}.png")
            path = self.generate(text, output_path, **kwargs)
            paths.append(path)
        
        return paths