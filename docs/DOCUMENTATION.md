# YouTube Thumbnail Generator - Documentation

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Configuration](#configuration)
5. [AI Text Optimization](#ai-text-optimization)
6. [Background Types](#background-types)
7. [Font Management](#font-management)
8. [Language Support](#language-support)
9. [Advanced Usage](#advanced-usage)
10. [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8 or higher
- PIL/Pillow library
- Optional: Gemini API key for AI features

### Install from Source

```bash
git clone https://github.com/preangelleo/youtube-thumbnail-generator.git
cd youtube-thumbnail-generator
pip install -r requirements.txt
```

### Install via pip (coming soon)

```bash
pip install youtube-thumbnail-generator
```

## Quick Start

```python
from src.thumbnail_generator import ThumbnailGenerator

# Basic usage
generator = ThumbnailGenerator()
thumbnail = generator.generate(
    text="Amazing Python Tutorial",
    output_path="thumbnail.png"
)

# With AI optimization
generator = ThumbnailGenerator(
    gemini_api_key="your-api-key",
    enable_ai_optimization=True
)
thumbnail = generator.generate(
    text="Python Tutorial",
    target_language="en"
)
```

## API Reference

### ThumbnailGenerator Class

#### Constructor

```python
ThumbnailGenerator(
    gemini_api_key: Optional[str] = None,
    enable_ai_optimization: Optional[bool] = None,
    default_language: str = "auto",
    width: int = 1280,
    height: int = 720
)
```

**Parameters:**

- `gemini_api_key` (str, optional): API key for Gemini AI text optimization
- `enable_ai_optimization` (bool, optional): Enable/disable AI optimization
- `default_language` (str): Default language for text ("en", "zh", "auto")
- `width` (int): Thumbnail width in pixels (default: 1280)
- `height` (int): Thumbnail height in pixels (default: 720)

#### generate() Method

```python
generate(
    text: str,
    output_path: str = "thumbnail.png",
    background_type: str = "gradient",
    background_config: Optional[Dict] = None,
    font_name: Optional[str] = None,
    font_size: int = 72,
    font_color: str = "#FFFFFF",
    text_position: str = "center",
    enable_ai_optimization: Optional[bool] = None,
    target_language: Optional[str] = None,
    custom_prompt: Optional[str] = None,
    quality: int = 95
) -> str
```

**Parameters:**

- `text` (str): The text to display on the thumbnail
- `output_path` (str): Path to save the thumbnail
- `background_type` (str): Type of background ("solid", "gradient", "image", "pattern")
- `background_config` (dict): Configuration for the background
- `font_name` (str): Font name or path to font file
- `font_size` (int): Font size in pixels
- `font_color` (str): Text color (hex, rgb, or named color)
- `text_position` (str/tuple): Text position ("center", "top", "bottom", or (x, y))
- `enable_ai_optimization` (bool): Override default AI setting
- `target_language` (str): Target language for optimization
- `custom_prompt` (str): Custom AI optimization prompt
- `quality` (int): Output image quality (1-100)

**Returns:**
- `str`: Path to the generated thumbnail

#### batch_generate() Method

```python
batch_generate(
    texts: list,
    output_dir: str = "thumbnails",
    **kwargs
) -> list
```

**Parameters:**

- `texts` (list): List of texts for thumbnails
- `output_dir` (str): Directory to save thumbnails
- `**kwargs`: Additional arguments passed to generate()

**Returns:**
- `list`: List of paths to generated thumbnails

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Gemini AI API Key
GEMINI_API_KEY=your-api-key-here

# Enable AI by default
ENABLE_AI_OPTIMIZATION=true

# Default language
DEFAULT_LANGUAGE=auto

# Thumbnail dimensions
THUMBNAIL_WIDTH=1280
THUMBNAIL_HEIGHT=720

# Default font settings
DEFAULT_FONT_SIZE=72
DEFAULT_FONT_COLOR=#FFFFFF

# Default background
DEFAULT_BACKGROUND_TYPE=gradient
DEFAULT_BACKGROUND_COLOR1=#667eea
DEFAULT_BACKGROUND_COLOR2=#764ba2

# Output settings
OUTPUT_QUALITY=95
OUTPUT_FORMAT=PNG
```

## AI Text Optimization

### Setting Up Gemini AI

1. Get an API key from [Google AI Studio](https://ai.google.dev/)
2. Add the key to your `.env` file or pass it to the constructor
3. Enable AI optimization in the generator

### AI Optimization Features

- **Automatic Enhancement**: Makes text more engaging and clickable
- **Language Optimization**: Optimizes for specific language audiences
- **Style Adjustment**: Different styles (engaging, professional, casual, dramatic)
- **Length Control**: Ensures text fits within character limits

### Controlling AI Optimization

```python
# Enable globally
generator = ThumbnailGenerator(
    gemini_api_key="key",
    enable_ai_optimization=True
)

# Disable for specific generation
thumbnail = generator.generate(
    text="My Text",
    enable_ai_optimization=False
)

# Custom optimization prompt
thumbnail = generator.generate(
    text="My Text",
    custom_prompt="Make this text viral: {text}"
)
```

## Background Types

### Solid Background

```python
background_config = {
    "color": "#FF6B6B"  # Hex, RGB, or named color
}
```

### Gradient Background

```python
background_config = {
    "color1": "#667eea",     # Start color
    "color2": "#764ba2",     # End color
    "direction": "diagonal"  # vertical, horizontal, diagonal
}
```

### Image Background

```python
background_config = {
    "image_path": "path/to/image.jpg",
    "blur": 5,                # Blur radius (optional)
    "overlay_color": "#000000",  # Overlay color (optional)
    "overlay_opacity": 0.3    # Overlay opacity 0-1 (optional)
}
```

### Pattern Background

```python
# Dots pattern
background_config = {
    "pattern": "dots",
    "color1": "#667eea",  # Background color
    "color2": "#764ba2",  # Pattern color
    "spacing": 50,        # Space between dots
    "radius": 10          # Dot radius
}

# Lines pattern
background_config = {
    "pattern": "lines",
    "color1": "#667eea",
    "color2": "#764ba2",
    "spacing": 30,
    "line_width": 3
}

# Grid pattern
background_config = {
    "pattern": "grid",
    "color1": "#667eea",
    "color2": "#764ba2",
    "spacing": 50,
    "line_width": 2
}

# Waves pattern
background_config = {
    "pattern": "waves",
    "color1": "#667eea",
    "color2": "#764ba2",
    "amplitude": 30,
    "frequency": 0.02
}
```

## Font Management

### Using System Fonts

```python
# Use font by name
thumbnail = generator.generate(
    text="My Text",
    font_name="arial",  # or "helvetica", "impact", etc.
    font_size=80
)
```

### Using Custom Fonts

```python
# Use font file path
thumbnail = generator.generate(
    text="My Text",
    font_name="/path/to/custom-font.ttf",
    font_size=80
)
```

### Available System Fonts

The generator automatically detects these fonts if installed:
- Arial
- Helvetica
- Impact
- Roboto
- Montserrat
- Bebas Neue
- Oswald

## Language Support

### Automatic Language Detection

```python
generator = ThumbnailGenerator(default_language="auto")

# Will auto-detect Chinese
thumbnail = generator.generate(text="Python编程教程")

# Will auto-detect English
thumbnail = generator.generate(text="Python Tutorial")
```

### Manual Language Specification

```python
# Force English optimization
thumbnail = generator.generate(
    text="Mixed 中文 Text",
    target_language="en"
)

# Force Chinese optimization
thumbnail = generator.generate(
    text="Mixed 中文 Text",
    target_language="zh"
)
```

### Language Detection Logic

- Uses `langdetect` library for initial detection
- Falls back to character-based detection
- 60% threshold for determining dominant language
- Defaults to English if uncertain

## Advanced Usage

### Custom Text Position

```python
# Specific pixel coordinates
thumbnail = generator.generate(
    text="My Text",
    text_position=(100, 200)  # x=100, y=200
)
```

### Multiple Thumbnails with Different Styles

```python
styles = [
    {"background_type": "solid", "font_size": 60},
    {"background_type": "gradient", "font_size": 80},
    {"background_type": "pattern", "font_size": 70}
]

for i, style in enumerate(styles):
    generator.generate(
        text="Tutorial Part " + str(i+1),
        output_path=f"thumb_{i+1}.png",
        **style
    )
```

### Programmatic Color Generation

```python
import colorsys

# Generate complementary colors
def get_complementary_colors(hue):
    rgb1 = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    rgb2 = colorsys.hsv_to_rgb((hue + 0.5) % 1, 0.8, 0.9)
    
    return (
        "#{:02x}{:02x}{:02x}".format(int(rgb1[0]*255), int(rgb1[1]*255), int(rgb1[2]*255)),
        "#{:02x}{:02x}{:02x}".format(int(rgb2[0]*255), int(rgb2[1]*255), int(rgb2[2]*255))
    )

color1, color2 = get_complementary_colors(0.6)

thumbnail = generator.generate(
    text="Dynamic Colors",
    background_config={"color1": color1, "color2": color2}
)
```

## Troubleshooting

### Common Issues

#### 1. AI Optimization Not Working

**Problem**: Text is not being optimized despite having API key

**Solutions**:
- Check if `GEMINI_API_KEY` is set correctly
- Ensure `enable_ai_optimization=True`
- Verify API key has proper permissions
- Check network connectivity

#### 2. Font Not Found

**Problem**: Custom font not loading

**Solutions**:
- Use absolute path to font file
- Check font file permissions
- Verify font format (TTF, OTF supported)
- Fall back to system fonts

#### 3. Language Detection Issues

**Problem**: Wrong language detected

**Solutions**:
- Manually specify `target_language`
- Ensure text has sufficient characters for detection
- Check if `langdetect` is installed properly

#### 4. Image Quality Issues

**Problem**: Output image is blurry or low quality

**Solutions**:
- Increase `quality` parameter (up to 100)
- Use PNG format for better quality
- Ensure source images are high resolution
- Check font size is appropriate for dimensions

#### 5. Memory Issues with Batch Generation

**Problem**: Out of memory when generating many thumbnails

**Solutions**:
- Process in smaller batches
- Reduce image dimensions
- Clear cache between batches
- Use lower quality settings

### Debug Mode

Enable verbose output for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

generator = ThumbnailGenerator()
# Debug messages will now be printed
```

### Performance Tips

1. **Cache Fonts**: Fonts are automatically cached after first use
2. **Batch Processing**: Use `batch_generate()` for multiple thumbnails
3. **Image Formats**: Use JPEG for smaller file sizes, PNG for transparency
4. **AI Rate Limiting**: Add delays between AI-optimized generations
5. **Background Images**: Pre-process and cache background images

## Support

For issues, questions, or contributions:

- GitHub Issues: [https://github.com/preangelleo/youtube-thumbnail-generator/issues](https://github.com/preangelleo/youtube-thumbnail-generator/issues)
- Documentation: [https://github.com/preangelleo/youtube-thumbnail-generator/docs](https://github.com/preangelleo/youtube-thumbnail-generator/docs)

## License

MIT License - see LICENSE file for details.