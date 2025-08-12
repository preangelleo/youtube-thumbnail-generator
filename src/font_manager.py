import os
from typing import Optional, Dict
from PIL import ImageFont
import platform


class FontManager:
    """Manages fonts for thumbnail text."""
    
    def __init__(self):
        """Initialize the font manager."""
        self.font_cache: Dict[str, ImageFont.FreeTypeFont] = {}
        self.system_fonts = self._discover_system_fonts()
    
    def _discover_system_fonts(self) -> Dict[str, str]:
        """Discover available system fonts.
        
        Returns:
            Dictionary mapping font names to paths
        """
        fonts = {}
        system = platform.system()
        
        if system == "Darwin":  # macOS
            font_dirs = [
                "/System/Library/Fonts",
                "/Library/Fonts",
                os.path.expanduser("~/Library/Fonts")
            ]
        elif system == "Linux":
            font_dirs = [
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.fonts")
            ]
        elif system == "Windows":
            font_dirs = [
                "C:\\Windows\\Fonts"
            ]
        else:
            font_dirs = []
        
        # Common font mappings
        font_files = {
            "arial": ["Arial.ttf", "arial.ttf", "ArialMT.ttf"],
            "helvetica": ["Helvetica.ttc", "Helvetica.ttf", "HelveticaNeue.ttc"],
            "impact": ["Impact.ttf", "impact.ttf"],
            "roboto": ["Roboto-Regular.ttf", "Roboto.ttf"],
            "montserrat": ["Montserrat-Regular.ttf", "Montserrat.ttf"],
            "bebas": ["BebasNeue-Regular.ttf", "BebasNeue.ttf"],
            "oswald": ["Oswald-Regular.ttf", "Oswald.ttf"],
        }
        
        for font_name, possible_files in font_files.items():
            for font_dir in font_dirs:
                if not os.path.exists(font_dir):
                    continue
                
                for filename in possible_files:
                    font_path = os.path.join(font_dir, filename)
                    if os.path.exists(font_path):
                        fonts[font_name] = font_path
                        break
                
                if font_name in fonts:
                    break
        
        return fonts
    
    def get_font(
        self,
        font_name: Optional[str] = None,
        size: int = 72,
        bold: bool = False,
        italic: bool = False
    ) -> ImageFont.FreeTypeFont:
        """Get a font object.
        
        Args:
            font_name: Name of the font or path to font file
            size: Font size
            bold: Whether to use bold variant
            italic: Whether to use italic variant
        
        Returns:
            PIL Font object
        """
        cache_key = f"{font_name}_{size}_{bold}_{italic}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        font_path = None
        
        if font_name:
            # Check if it's a file path
            if os.path.exists(font_name):
                font_path = font_name
            # Check system fonts
            elif font_name.lower() in self.system_fonts:
                font_path = self.system_fonts[font_name.lower()]
            # Try to find font with modifiers
            elif bold or italic:
                modifiers = []
                if bold:
                    modifiers.append("Bold")
                if italic:
                    modifiers.append("Italic")
                
                for modifier in modifiers:
                    modified_name = f"{font_name}-{modifier}"
                    if modified_name.lower() in self.system_fonts:
                        font_path = self.system_fonts[modified_name.lower()]
                        break
        
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size)
            else:
                # Fall back to default font
                font = ImageFont.load_default()
                # Try to scale up the default font
                if size > 11:  # Default font size is usually 11
                    try:
                        # Try to use a basic TrueType font
                        font = self._get_fallback_font(size)
                    except:
                        pass
        except Exception as e:
            print(f"Warning: Failed to load font {font_name}: {e}")
            font = self._get_fallback_font(size)
        
        self.font_cache[cache_key] = font
        return font
    
    def _get_fallback_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get a fallback font.
        
        Args:
            size: Font size
        
        Returns:
            Fallback font object
        """
        # Try to find any available TrueType font
        for font_name, font_path in self.system_fonts.items():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
        
        # Last resort: use default font
        return ImageFont.load_default()
    
    def list_available_fonts(self) -> list:
        """List all available fonts.
        
        Returns:
            List of available font names
        """
        return list(self.system_fonts.keys())
    
    def add_custom_font(self, name: str, path: str) -> bool:
        """Add a custom font to the manager.
        
        Args:
            name: Name to register the font as
            path: Path to the font file
        
        Returns:
            True if successful, False otherwise
        """
        if os.path.exists(path):
            self.system_fonts[name.lower()] = path
            return True
        return False