import re
from typing import Tuple
from langdetect import detect, LangDetectException


def detect_language(text: str) -> str:
    """Detect the language of the text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code ('en' for English, 'zh' for Chinese)
    """
    try:
        # Try langdetect first
        detected = detect(text)
        
        if detected.startswith('zh'):
            return 'zh'
        elif detected == 'en':
            return 'en'
        else:
            # Fallback to character-based detection
            return _detect_by_characters(text)
    
    except (LangDetectException, Exception):
        # Fallback to character-based detection
        return _detect_by_characters(text)


def _detect_by_characters(text: str) -> str:
    """Detect language by character analysis.
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code ('en' or 'zh')
    """
    # Count Chinese characters
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]+', text))
    # Count English characters
    english_chars = len(re.findall(r'[a-zA-Z]+', text))
    
    total_chars = chinese_chars + english_chars
    
    if total_chars == 0:
        return 'en'  # Default to English
    
    # If more than 60% Chinese characters, consider it Chinese
    if chinese_chars / total_chars > 0.6:
        return 'zh'
    else:
        return 'en'


def validate_dimensions(width: int, height: int) -> Tuple[int, int]:
    """Validate and adjust thumbnail dimensions.
    
    Args:
        width: Desired width
        height: Desired height
    
    Returns:
        Valid width and height tuple
    """
    # YouTube recommended thumbnail dimensions
    STANDARD_DIMENSIONS = [
        (1280, 720),   # HD (16:9)
        (1920, 1080),  # Full HD (16:9)
        (2560, 1440),  # 2K (16:9)
        (640, 360),    # SD (16:9)
    ]
    
    # Check if dimensions are already standard
    if (width, height) in STANDARD_DIMENSIONS:
        return width, height
    
    # Calculate aspect ratio
    aspect_ratio = width / height
    
    # YouTube recommends 16:9 aspect ratio
    target_ratio = 16 / 9
    
    # If aspect ratio is close to 16:9, adjust slightly
    if abs(aspect_ratio - target_ratio) < 0.1:
        # Round to nearest standard dimension
        for std_width, std_height in STANDARD_DIMENSIONS:
            if abs(width - std_width) < 100 and abs(height - std_height) < 100:
                return std_width, std_height
    
    # Otherwise, maintain aspect ratio but ensure minimum size
    min_width, min_height = 640, 360
    
    if width < min_width or height < min_height:
        scale = max(min_width / width, min_height / height)
        width = int(width * scale)
        height = int(height * scale)
    
    return width, height


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe file system usage.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"|?*\\/]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    max_length = 100
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        name = name[:max_length - len(ext) - 1]
        filename = f"{name}.{ext}" if ext else name
    
    return filename


def normalize_language_code(lang: str) -> str:
    """Normalize language input to standard ISO 639-1 code.
    
    Args:
        lang: Language code or name (e.g., 'en', 'English', 'chinese', 'zh')
    
    Returns:
        Normalized language code ('en' or 'zh')
    """
    if not lang:
        return None
    
    lang_lower = lang.lower().strip()
    
    # Map full names and variations to standard codes
    language_map = {
        # English variations
        'en': 'en',
        'eng': 'en',
        'english': 'en',
        'en-us': 'en',
        'en-gb': 'en',
        'en_us': 'en',
        'en_gb': 'en',
        
        # Chinese variations
        'zh': 'zh',
        'chi': 'zh',
        'chinese': 'zh',
        'zh-cn': 'zh',
        'zh-tw': 'zh',
        'zh_cn': 'zh',
        'zh_tw': 'zh',
        'mandarin': 'zh',
        'simplified': 'zh',
        'traditional': 'zh',
        '中文': 'zh',
        '中国': 'zh',
    }
    
    return language_map.get(lang_lower, lang_lower)


def parse_color(color_str: str) -> Tuple[int, int, int]:
    """Parse color string to RGB tuple.
    
    Args:
        color_str: Color string (hex or rgb)
    
    Returns:
        RGB tuple
    """
    # Handle hex colors
    if color_str.startswith('#'):
        hex_color = color_str[1:]
        if len(hex_color) == 3:
            # Convert 3-digit hex to 6-digit
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Handle rgb() format
    elif color_str.startswith('rgb'):
        numbers = re.findall(r'\d+', color_str)
        if len(numbers) >= 3:
            return tuple(int(n) for n in numbers[:3])
    
    # Handle named colors (basic ones)
    named_colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
    }
    
    if color_str.lower() in named_colors:
        return named_colors[color_str.lower()]
    
    # Default to white
    return (255, 255, 255)