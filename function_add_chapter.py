
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import platform

def detect_system():
    """检测系统环境"""
    system = platform.system()
    if system == "Darwin":
        return {"system": "Mac"}
    elif system == "Linux":
        hostname = platform.node()
        if "runpod" in hostname.lower():
            return {"system": "RunPod"}
        elif "aws" in hostname.lower() or "ec2" in hostname.lower():
            return {"system": "AWS"}
        else:
            return {"system": "TB"}
    else:
        return {"system": "Unknown"}

def add_chapter_to_image(text, image_path=None, output_path=None, font_size=None, text_color=(255, 255, 255), shadow_color=(0, 0, 0), shadow_offset=5, line_spacing=1.2, max_width_ratio=0.8, is_landscape=True, width=1600, height=900, font_name=None, language='chinese'):
    """
    Adds a centered quotation text to an image, supporting Chinese and English.
    Automatically selects Chinese font based on environment (TB, Mac, AWS).
    English uses system default font.
    Args:
        text (str): The text to add
        image_path (str): Optional, path to base image
        output_path (str): Optional, path to save output
        font_size (int): Optional, font size
        text_color (tuple): RGB color for text
        shadow_color (tuple): RGB color for shadow
        shadow_offset (int): Shadow offset
        line_spacing (float): Line spacing multiplier
        max_width_ratio (float): Max width ratio for text
        is_landscape (bool): If True, landscape; else portrait
        width (int): Image width
        height (int): Image height
    Returns:
        bool: True if successful, False otherwise
        str: Path to the output image if successful, None otherwise
    """
    # Setup output directory
    if output_path is None:
        os.makedirs("Temps", exist_ok=True)
        output_path = "Temps/quoted_image.png"

    # Fix portrait/landscape dimensions
    if not is_landscape and width > height:
        width, height = height, width
    
    # Load existing image or create a new one
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            width, height = img.size
        except Exception as e:
            print(f"Error opening image: {e}")
            return False, None
    else: img = Image.new('RGB', (width, height), color='black')
    
    # Create draw object
    draw = ImageDraw.Draw(img)
    
    # Check for Chinese/non-ASCII characters
    # has_chinese = any(ord(c) > 127 for c in text)
    
    # Calculate font size if not provided
    if font_size is None:
        base_dimension = min(width, height)
        # Use 9.6% of the shorter dimension for font size
        font_size = int(base_dimension * 0.096)
    
    # Load font based on font_name
    font = None
    font_paths = []

    if language == 'chinese': font_name = "Noto Sans CJK SC"
    else: font_name = "Lexend Bold"

    # 检测系统环境来优化字体路径搜索顺序
    system_info = detect_system()
    current_system = system_info.get('system', 'Unknown')
    
    if font_name == "Lexend Bold":
        if current_system in ['RunPod', 'AWS', 'TB']:
            # Linux系统优先搜索系统字体目录
            font_paths = [
                "/usr/share/fonts/truetype/lexend/Lexend-Bold.ttf",
                "/home/ubuntu/.local/share/fonts/Lexend/Lexend-Bold.ttf",
                "/usr/local/share/fonts/Lexend-Bold.ttf"
            ]
        else:
            # Mac系统
            font_paths = [
                "/Users/lgg/Library/Fonts/Lexend/Lexend-Bold.ttf",
                "/Library/Fonts/Lexend-Bold.ttf",
                "/System/Library/Fonts/Lexend-Bold.ttf"
            ]
    elif font_name == "Ubuntu Bold" or font_name == "Ubuntu": 
       font_paths = [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",  
            "/usr/share/fonts/ubuntu/Ubuntu-B.ttf",
            "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-Bold.ttf",
            "/System/Library/Fonts/Ubuntu-Bold.ttf",
            "/Library/Fonts/Ubuntu-Bold.ttf"
        ]
    elif font_name == "Noto Sans CJK SC":
        if current_system in ['RunPod', 'AWS', 'TB']:
            # Linux系统使用标准路径
            font_paths = [
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
            ]
        else:
            # Mac系统
            font_paths = [
                "/System/Library/Fonts/NotoSansCJK-Bold.ttc",
                "/Library/Fonts/NotoSansCJK-Bold.ttc"
            ]
    
    # Try to load the font
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size=font_size)
                break
            except Exception as e:
                print(f"Failed to load {path}: {e}")
                continue
    
    # Fallback to default font if not found
    if font is None:
        print(f"Font {font_name} not found, using default font.")
        font = ImageFont.load_default()
    
    # Calculate maximum text width
    max_text_width = int(width * max_width_ratio)
    
    # Text wrapping based on language
    lines = []
    if language.lower() == 'chinese':
        # For Chinese text in Portrait mode, also split at colon for better formatting
        # Support both Chinese full-width colon (：) and English half-width colon (:)
        if ('：' in text or ':' in text) and not is_landscape:  # Portrait mode
            # Split at colon and create two lines - try Chinese colon first, then English
            if '：' in text:
                parts = text.split('：', 1)  # Split only at first Chinese colon
                if len(parts) == 2:
                    initial_lines = [parts[0] + '：', parts[1].strip()]
                else:
                    initial_lines = [text]
            elif ':' in text:
                parts = text.split(':', 1)  # Split only at first English colon
                if len(parts) == 2:
                    initial_lines = [parts[0] + ':', parts[1].strip()]
                else:
                    initial_lines = [text]
            else:
                initial_lines = [text]
            
            # Now check each line for width and wrap if necessary
            lines = []
            for line in initial_lines:
                # For Chinese text, measure actual width of each character
                current_line = ""
                for char in line:
                    test_line = current_line + char
                    
                    # Get text width using the appropriate method
                    try:
                        if hasattr(font, 'getlength'): line_width = font.getlength(test_line)
                        else: line_width = font.getbbox(test_line)[2]
                        
                        if line_width > max_text_width:
                            if current_line:  # Only append if not empty
                                lines.append(current_line)
                            current_line = char
                        else:
                            current_line = test_line
                    except Exception:
                        # Fallback if measurement fails
                        if len(test_line) > max_text_width // 30:
                            if current_line:  # Only append if not empty
                                lines.append(current_line)
                            current_line = char
                        else:
                            current_line = test_line
                
                # Add the final line for this segment
                if current_line:
                    lines.append(current_line)
        else:
            # For Chinese text in Landscape mode or without colon, use character-by-character wrapping
            current_line = ""
            for char in text:
                test_line = current_line + char
                
                # Get text width using the appropriate method
                try:
                    if hasattr(font, 'getlength'): line_width = font.getlength(test_line)
                    else: line_width = font.getbbox(test_line)[2]
                        
                    if line_width > max_text_width:
                        lines.append(current_line)
                        current_line = char
                    else:
                        current_line = test_line
                except Exception:
                    # Fallback if measurement fails
                    if len(test_line) > max_text_width // 30:
                        lines.append(current_line)
                        current_line = char
                    else:
                        current_line = test_line
            
            # Add the final line
            if current_line:
                lines.append(current_line)
    else:
        # For English text, split at colon if present for better formatting
        if ':' in text and language.lower() == 'english':
            # Split at colon and create two lines
            parts = text.split(':', 1)  # Split only at first colon
            if len(parts) == 2:
                initial_lines = [parts[0] + ':', parts[1].strip()]
            else:
                initial_lines = [text]
            
            # Now check each line for width and wrap if necessary
            lines = []
            for line in initial_lines:
                # Check if line fits within max width
                try:
                    if hasattr(font, 'getlength'): line_width = font.getlength(line)
                    else: line_width = font.getbbox(line)[2]
                    
                    # If line is too long, wrap it
                    if line_width > max_text_width:
                        avg_char_width = font_size // 2
                        chars_per_line = max(1, int(max_text_width / avg_char_width))
                        wrapped_lines = textwrap.wrap(line, width=chars_per_line)
                        lines.extend(wrapped_lines)
                    else: lines.append(line)

                except Exception:
                    # Fallback: estimate character width
                    avg_char_width = font_size // 2
                    chars_per_line = max(1, int(max_text_width / avg_char_width))
                    if len(line) > chars_per_line:
                        wrapped_lines = textwrap.wrap(line, width=chars_per_line)
                        lines.extend(wrapped_lines)
                    else:
                        lines.append(line)
        else:
            # For non-Chinese text without colon, use simpler text wrapping
            avg_char_width = font_size // 2
            chars_per_line = max(1, int(max_text_width / avg_char_width))
            lines = textwrap.wrap(text, width=chars_per_line)
    
    # Calculate text layout dimensions
    line_height = int(font_size * line_spacing)
    total_text_height = line_height * len(lines)
    
    # Calculate starting Y position for vertical centering
    start_y = (height - total_text_height) // 2
    
    # Draw each line
    current_y = start_y
    for line in lines:
        # Get text width for horizontal centering
        try: text_width = font.getlength(line) if hasattr(font, 'getlength') else font.getbbox(line)[2]
        except Exception: text_width = len(line) * (font_size // 2)
        
        # Calculate X position for centering
        x_position = (width - text_width) // 2
        
        # Draw shadow
        if shadow_offset > 0:
            draw.text(
                (x_position + shadow_offset, current_y + shadow_offset),
                line,
                font=font,
                fill=shadow_color
            )
        
        # Draw text
        draw.text(
            (x_position, current_y),
            line,
            font=font,
            fill=text_color
        )
        
        current_y += line_height
    
    # Save image
    try:
        img.save(output_path)
        return True, output_path
    except Exception as e: return False, e
    