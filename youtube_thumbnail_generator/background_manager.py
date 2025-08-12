from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw
import numpy as np


class BackgroundManager:
    """Manages different types of backgrounds for thumbnails."""
    
    def __init__(self, width: int = 1280, height: int = 720):
        """Initialize the background manager.
        
        Args:
            width: Background width
            height: Background height
        """
        self.width = width
        self.height = height
    
    def create_background(
        self,
        background_type: str = "gradient",
        config: Dict[str, Any] = None
    ) -> Image.Image:
        """Create a background based on type and configuration.
        
        Args:
            background_type: Type of background (solid/gradient/image/pattern)
            config: Configuration dictionary for the background
        
        Returns:
            PIL Image object
        """
        config = config or {}
        
        if background_type == "solid":
            return self._create_solid_background(config)
        elif background_type == "gradient":
            return self._create_gradient_background(config)
        elif background_type == "image":
            return self._create_image_background(config)
        elif background_type == "pattern":
            return self._create_pattern_background(config)
        else:
            # Default to gradient
            return self._create_gradient_background(config)
    
    def _create_solid_background(self, config: Dict[str, Any]) -> Image.Image:
        """Create a solid color background.
        
        Args:
            config: Configuration with 'color' key
        
        Returns:
            PIL Image object
        """
        color = config.get('color', '#667eea')
        
        # Convert hex to RGB if needed
        if isinstance(color, str) and color.startswith('#'):
            color = self._hex_to_rgb(color)
        
        image = Image.new('RGB', (self.width, self.height), color)
        return image
    
    def _create_gradient_background(self, config: Dict[str, Any]) -> Image.Image:
        """Create a gradient background.
        
        Args:
            config: Configuration with 'color1', 'color2', and optional 'direction'
        
        Returns:
            PIL Image object
        """
        color1 = config.get('color1', '#667eea')
        color2 = config.get('color2', '#764ba2')
        direction = config.get('direction', 'diagonal')  # vertical, horizontal, diagonal
        
        # Convert hex to RGB
        if isinstance(color1, str):
            color1 = self._hex_to_rgb(color1)
        if isinstance(color2, str):
            color2 = self._hex_to_rgb(color2)
        
        # Create gradient array
        gradient = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        if direction == 'vertical':
            for y in range(self.height):
                ratio = y / self.height
                color = self._interpolate_color(color1, color2, ratio)
                gradient[y, :] = color
        
        elif direction == 'horizontal':
            for x in range(self.width):
                ratio = x / self.width
                color = self._interpolate_color(color1, color2, ratio)
                gradient[:, x] = color
        
        else:  # diagonal
            for y in range(self.height):
                for x in range(self.width):
                    ratio = (x + y) / (self.width + self.height)
                    gradient[y, x] = self._interpolate_color(color1, color2, ratio)
        
        return Image.fromarray(gradient, 'RGB')
    
    def _create_image_background(self, config: Dict[str, Any]) -> Image.Image:
        """Create a background from an image file.
        
        Args:
            config: Configuration with 'image_path' key
        
        Returns:
            PIL Image object
        """
        image_path = config.get('image_path')
        
        if not image_path:
            # Return default gradient if no image specified
            return self._create_gradient_background({})
        
        try:
            image = Image.open(image_path)
            
            # Resize to fit thumbnail dimensions
            image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Apply blur if specified
            blur = config.get('blur', 0)
            if blur > 0:
                from PIL import ImageFilter
                image = image.filter(ImageFilter.GaussianBlur(radius=blur))
            
            # Apply overlay if specified
            overlay_color = config.get('overlay_color')
            overlay_opacity = config.get('overlay_opacity', 0.3)
            
            if overlay_color:
                overlay = Image.new('RGB', (self.width, self.height), 
                                  self._hex_to_rgb(overlay_color) if isinstance(overlay_color, str) else overlay_color)
                image = Image.blend(image, overlay, overlay_opacity)
            
            return image
            
        except Exception as e:
            print(f"Warning: Failed to load image {image_path}: {e}")
            return self._create_gradient_background({})
    
    def _create_pattern_background(self, config: Dict[str, Any]) -> Image.Image:
        """Create a patterned background.
        
        Args:
            config: Configuration with pattern type and colors
        
        Returns:
            PIL Image object
        """
        pattern_type = config.get('pattern', 'dots')  # dots, lines, grid, waves
        color1 = self._hex_to_rgb(config.get('color1', '#667eea'))
        color2 = self._hex_to_rgb(config.get('color2', '#764ba2'))
        
        image = Image.new('RGB', (self.width, self.height), color1)
        draw = ImageDraw.Draw(image)
        
        if pattern_type == 'dots':
            spacing = config.get('spacing', 50)
            radius = config.get('radius', 10)
            
            for y in range(0, self.height + spacing, spacing):
                for x in range(0, self.width + spacing, spacing):
                    draw.ellipse(
                        [(x - radius, y - radius), (x + radius, y + radius)],
                        fill=color2
                    )
        
        elif pattern_type == 'lines':
            spacing = config.get('spacing', 30)
            line_width = config.get('line_width', 3)
            
            # Diagonal lines
            for i in range(-self.height, self.width + self.height, spacing):
                draw.line(
                    [(i, 0), (i + self.height, self.height)],
                    fill=color2,
                    width=line_width
                )
        
        elif pattern_type == 'grid':
            spacing = config.get('spacing', 50)
            line_width = config.get('line_width', 2)
            
            # Vertical lines
            for x in range(0, self.width, spacing):
                draw.line([(x, 0), (x, self.height)], fill=color2, width=line_width)
            
            # Horizontal lines
            for y in range(0, self.height, spacing):
                draw.line([(0, y), (self.width, y)], fill=color2, width=line_width)
        
        elif pattern_type == 'waves':
            # Create wave pattern
            amplitude = config.get('amplitude', 30)
            frequency = config.get('frequency', 0.02)
            
            for x in range(self.width):
                for y_offset in range(-amplitude, amplitude + 1, 5):
                    y = self.height // 2 + int(amplitude * np.sin(frequency * x)) + y_offset
                    if 0 <= y < self.height:
                        draw.point((x, y), fill=color2)
        
        return image
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple.
        
        Args:
            hex_color: Hex color string (e.g., '#ffffff')
        
        Returns:
            RGB tuple
        """
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _interpolate_color(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        ratio: float
    ) -> Tuple[int, int, int]:
        """Interpolate between two colors.
        
        Args:
            color1: Start color RGB
            color2: End color RGB
            ratio: Interpolation ratio (0-1)
        
        Returns:
            Interpolated RGB color
        """
        return tuple([
            int(color1[i] + (color2[i] - color1[i]) * ratio)
            for i in range(3)
        ])