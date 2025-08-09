#!/usr/bin/env python3
"""
最终版YouTube缩略图生成器
按用户要求修改：Logo左边距=上边距，只保留title，author大写，去掉副标题功能
"""

from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional, Dict, Any
import os
from dataclasses import dataclass
import random

# ========== 配置常量 ==========
LOGO_SIZE = 100  # Logo目标尺寸 (像素), 100x100正方形
# 修改此值可以调整所有logo的显示大小

# Import title optimizer (optional dependency)
try:
    from title_optimizer import create_title_optimizer
    TITLE_OPTIMIZER_AVAILABLE = True
except ImportError:
    TITLE_OPTIMIZER_AVAILABLE = False
import textwrap
import platform
try:
    from importlib import resources
    from importlib.resources import files
except ImportError:
    # Fallback for Python < 3.9
    import pkg_resources

try:
    from .text_png_generator import create_text_png
except ImportError:
    from text_png_generator import create_text_png

def create_default_templates():
    """Create default templates in user's current directory if they don't exist"""
    import os
    from PIL import Image, ImageDraw
    
    # Create templates directory if it doesn't exist
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"Created templates directory: {templates_dir}")
    
    # Template paths to create
    templates_to_create = {
        "templates/professional_template.jpg": (1600, 900, (0, 0, 0)),  # Black background
        "templates/light_template.png": (1600, 900, (255, 255, 255, 255)),  # White background
        "templates/triangle_black.png": None,  # Special handling
        "templates/triangle_white.png": None   # Special handling
    }
    
    for template_path, config in templates_to_create.items():
        if not os.path.exists(template_path):
            try:
                if config:
                    width, height, color = config
                    if len(color) == 4:  # RGBA
                        img = Image.new('RGBA', (width, height), color)
                        img.save(template_path, 'PNG')
                    else:  # RGB
                        img = Image.new('RGB', (width, height), color)
                        img.save(template_path, 'JPEG', quality=95)
                    print(f"Created template: {template_path}")
                    
            except Exception as e:
                print(f"Failed to create template {template_path}: {e}")
    
    # Create triangles
    create_triangle_templates()
    print("All default templates created successfully!")

def generate_triangle_template(color: str = "black", direction: str = "bottom", 
                              output_path: str = None, width: int = 200, height: int = 900) -> str:
    """
    Generate triangle template with customizable color and direction
    
    Args:
        color (str): Triangle color - "black", "white", or hex color like "#FF0000"
        direction (str): Triangle point direction - "bottom" (point at bottom-left) or "top" (point at top-left)
        output_path (str): Custom output path (optional)
        width (int): Triangle width in pixels (default: 200)
        height (int): Triangle height in pixels (default: 900)
        
    Returns:
        str: Path to the generated triangle file
        
    Examples:
        generate_triangle_template("black", "bottom")  # Default black triangle, point at bottom-left
        generate_triangle_template("white", "top")     # White triangle, point at top-left
        generate_triangle_template("#FF0000", "bottom", "red_triangle.png")  # Custom red triangle
    """
    from PIL import Image, ImageDraw
    
    # Generate default output path if not provided
    if not output_path:
        direction_suffix = "bottom" if direction == "bottom" else "top"
        if color.startswith("#"):
            color_name = color.replace("#", "hex")
        else:
            color_name = color
        output_path = f"templates/triangle_{color_name}_{direction_suffix}.png"
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:  # Only if there's a directory component
        os.makedirs(output_dir, exist_ok=True)
    
    # Create transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define triangle points based on direction
    if direction == "bottom":
        # Point at bottom-left: top-right to top-left to bottom-left
        triangle_points = [(width, 0), (0, 0), (0, height)]
    else:  # direction == "top"  
        # Point at top-left: top-left to bottom-left to bottom-right
        triangle_points = [(0, 0), (0, height), (width, height)]
    
    # Convert color to RGB
    if color == "black":
        fill_color = (0, 0, 0, 255)
    elif color == "white":
        fill_color = (255, 255, 255, 255)
    elif color.startswith("#"):
        # Convert hex to RGBA
        hex_color = color.lstrip('#')
        if len(hex_color) == 6:
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            fill_color = (r, g, b, 255)
        else:
            print(f"Warning: Invalid hex color {color}, using black")
            fill_color = (0, 0, 0, 255)
    else:
        print(f"Warning: Unknown color {color}, using black")
        fill_color = (0, 0, 0, 255)
    
    # Draw triangle
    draw.polygon(triangle_points, fill=fill_color)
    
    # Save triangle
    img.save(output_path, 'PNG')
    print(f"Generated triangle: {output_path}")
    print(f"  Color: {color}, Direction: {direction}, Size: {width}x{height}")
    
    return output_path

def create_triangle_templates():
    """Create default triangle template files for dark and light themes"""
    # Create all four triangle variations
    # 尖朝下 (bottom - 倒梯形)
    generate_triangle_template("black", "bottom", "templates/triangle_black.png")  # 保持兼容性
    generate_triangle_template("white", "bottom", "templates/triangle_white.png")  # 保持兼容性
    generate_triangle_template("black", "bottom", "templates/triangle_black_bottom.png")
    generate_triangle_template("white", "bottom", "templates/triangle_white_bottom.png")
    
    # 尖朝上 (top - 正梯形)
    generate_triangle_template("black", "top", "templates/triangle_black_top.png")
    generate_triangle_template("white", "top", "templates/triangle_white_top.png")
    
    print("Default triangle templates created (4 variations: black/white × top/bottom)!")

def optimize_for_youtube_api(input_path: str, output_path: str = None) -> str:
    """
    Optimize thumbnail for YouTube API v3 upload compliance
    
    YouTube API v3 Requirements (2025):
    - Format: JPEG or PNG (JPEG recommended for smaller file size)
    - Dimensions: 1280x720 pixels (16:9 aspect ratio)
    - Minimum: 640x360 pixels
    - Maximum file size: 2MB
    - Color space: sRGB
    - MIME types: image/jpeg, image/png
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path for the optimized output (optional)
        
    Returns:
        str: Path to the YouTube-compliant thumbnail
    """
    from PIL import Image, ImageCms
    import os
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")
    
    # Generate output path if not provided
    if not output_path:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_youtube_ready.jpg"
    
    print(f"Optimizing thumbnail for YouTube API compliance...")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    
    try:
        # Open the image
        img = Image.open(input_path)
        original_size = img.size
        print(f"Original size: {original_size[0]}x{original_size[1]}")
        
        # Convert to RGB if needed (removes alpha channel)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparent areas
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
            print("Converted to RGB with white background")
        
        # Ensure sRGB color profile
        try:
            import io
            # Check if image has an embedded color profile
            if 'icc_profile' in img.info:
                # Convert to sRGB if it has a different profile
                input_profile = ImageCms.ImageCmsProfile(io.BytesIO(img.info['icc_profile']))
                srgb_profile = ImageCms.createProfile('sRGB')
                
                if input_profile.profile.profile_description != srgb_profile.profile.profile_description:
                    img = ImageCms.profileToProfile(img, input_profile, srgb_profile, renderingIntent=0)
                    print("Converted to sRGB color profile")
            else:
                # If no profile, assume it's already sRGB
                print("No color profile found, assuming sRGB")
        except Exception as e:
            print(f"Color profile conversion skipped: {e}")
        
        # YouTube API optimal dimensions: 1280x720 (16:9 aspect ratio)
        target_width, target_height = 1280, 720
        target_ratio = target_width / target_height  # 16:9 = 1.777...
        
        current_width, current_height = img.size
        current_ratio = current_width / current_height
        
        # Resize to fit YouTube's requirements
        if abs(current_ratio - target_ratio) < 0.01:  # Already 16:9
            # Direct resize
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            print(f"Resized to YouTube standard: {target_width}x{target_height}")
        else:
            # Need to crop or pad to maintain 16:9 ratio
            if current_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(current_height * target_ratio)
                left = (current_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, current_height))
                print(f"Cropped width to maintain 16:9 ratio")
            else:
                # Image is taller, crop height
                new_height = int(current_width / target_ratio)
                top = (current_height - new_height) // 2
                img = img.crop((0, top, current_width, top + new_height))
                print(f"Cropped height to maintain 16:9 ratio")
            
            # Resize to target dimensions
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            print(f"Final resize to: {target_width}x{target_height}")
        
        # Save with optimized settings for YouTube API
        save_kwargs = {
            'format': 'JPEG',
            'quality': 95,  # High quality
            'optimize': True,  # Enable optimization
            'progressive': False,  # YouTube prefers baseline JPEG
        }
        
        # Try different quality levels to meet 2MB limit
        max_file_size = 2 * 1024 * 1024  # 2MB in bytes
        quality_levels = [95, 90, 85, 80, 75, 70]
        
        for quality in quality_levels:
            save_kwargs['quality'] = quality
            
            # Save to temporary location to check file size
            import tempfile
            import io
            
            # Save to bytes buffer to check size
            buffer = io.BytesIO()
            img.save(buffer, **save_kwargs)
            file_size = len(buffer.getvalue())
            
            if file_size <= max_file_size:
                # File size is acceptable, save to final location
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                
                print(f"Saved with quality {quality}, file size: {file_size:,} bytes ({file_size/1024/1024:.2f}MB)")
                break
        else:
            # If even quality 70 is too large, save anyway with warning
            with open(output_path, 'wb') as f:
                save_kwargs['quality'] = 70
                img.save(f, **save_kwargs)
            
            final_size = os.path.getsize(output_path)
            print(f"Warning: File size {final_size:,} bytes ({final_size/1024/1024:.2f}MB) exceeds 2MB limit")
            print("YouTube API may reject or compress this thumbnail further")
        
        # Final verification
        final_size = os.path.getsize(output_path)
        print(f"✅ YouTube-compliant thumbnail created:")
        print(f"   📏 Dimensions: 1280x720 (16:9 aspect ratio)")
        print(f"   📁 Format: JPEG")
        print(f"   🎨 Color space: sRGB")
        print(f"   📊 File size: {final_size:,} bytes ({final_size/1024/1024:.2f}MB)")
        print(f"   🚀 YouTube API ready: {'✅ YES' if final_size <= max_file_size else '⚠️ SIZE WARNING'}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error optimizing thumbnail: {e}")
        raise e

def get_resource_path(filename: str) -> str:
    """Get absolute path to package resource file with fallback creation"""
    try:
        # Try modern importlib.resources first (Python 3.9+)
        try:
            package_files = files('youtube_thumbnail_generator')
            resource_path = package_files / filename
            if resource_path.exists():
                return str(resource_path)
        except:
            pass
        
        # Fallback to pkg_resources (Python < 3.9)
        try:
            resource_path = pkg_resources.resource_filename('youtube_thumbnail_generator', filename)
            if os.path.exists(resource_path):
                return resource_path
        except:
            pass
        
        # Final fallback: check relative to current file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        relative_path = os.path.join(parent_dir, filename)
        if os.path.exists(relative_path):
            return relative_path
        
        # Ultimate fallback: check in current working directory
        local_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(local_path):
            return local_path
        
        # If file doesn't exist anywhere, try to create default templates
        if filename.startswith("templates/"):
            print(f"Resource not found: {filename}. Creating default templates...")
            create_default_templates()
            
            # Check if the local path exists now
            if os.path.exists(local_path):
                return local_path
        
        # If all else fails, return the local path (user's current directory)
        print(f"Warning: Using fallback path for: {filename}")
        return local_path
        
    except Exception as e:
        print(f"Error resolving resource path for {filename}: {e}")
        # Return local path as final fallback
        return os.path.join(os.getcwd(), filename)


@dataclass
class TextConfig:
    """文字配置类"""
    text: str
    position: Tuple[int, int]
    font_path: str = None
    font_size: int = 60
    color: str = "#FFFFFF"
    max_width: Optional[int] = None
    align: str = "left"
    stroke_width: int = 0
    stroke_fill: str = "#000000"
    shadow_offset: Optional[Tuple[int, int]] = None
    shadow_color: str = "#333333"

@dataclass 
class LogoConfig:
    """Logo配置类"""
    logo_path: str
    position: Tuple[int, int]
    size: Optional[Tuple[int, int]] = None
    opacity: float = 1.0

class FinalThumbnailGenerator:
    """最终版缩略图生成器"""
    
    def __init__(self, template_path: str = None, google_api_key: str = None):
        """初始化生成器
        
        Args:
            template_path (str, optional): 模板文件路径。
                                         如果不提供，将使用默认黑色模板
            google_api_key (str, optional): Google API key for title optimization.
                                           If not provided, tries environment variable GOOGLE_API_KEY.
                                           If unavailable, title optimization is disabled.
        """
        if template_path is None:
            # 使用默认黑色模板
            template_path = get_resource_path("templates/professional_template.jpg")
            print(f"Using default black template: {template_path}")
        
        self.template_path = template_path
        if not os.path.exists(template_path):
            print(f"Template not found at {template_path}, creating default templates...")
            create_default_templates()
            # 再次检查模板是否存在
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"无法创建默认模板: {template_path}")
        
        # 注意：不在初始化时验证模板尺寸，因为用户应该在generate时选择模板
            
        # 系统初始化 - 使用通用字体检测
        print(f"Initialized with template: {os.path.basename(self.template_path)}")
        
        # 初始化字体优先级列表
        self.font_paths = {
            # 中文字体
            "chinese": self._get_chinese_font_paths(),
            # 英文字体
            "english": self._get_english_font_paths()
        }
        
        # Initialize title optimizer (optional)
        self.title_optimizer = None
        if TITLE_OPTIMIZER_AVAILABLE:
            try:
                self.title_optimizer = create_title_optimizer(google_api_key)
                if self.title_optimizer.is_available:
                    print("Title optimization enabled with Google Gemini API")
                else:
                    print("Title optimization disabled - no valid Google API key")
            except Exception as e:
                print(f"Failed to initialize title optimizer: {e}")
        else:
            print("Title optimization unavailable - google-generativeai package not installed")
    
    def _ensure_template_size(self, template_path: str) -> Image.Image:
        """确保模板尺寸为 1600x900，如果不是则强制转换"""
        try:
            from PIL import Image
            img = Image.open(template_path)
            width, height = img.size
            
            if width == 1600 and height == 900:
                print(f"Template size verified: {width}x{height} ✓")
                return img
            
            print(f"模板尺寸 {width}x{height} 不符合要求，强制转换为 1600x900")
            
            # 计算缩放比例
            target_width, target_height = 1600, 900
            scale_x = target_width / width
            scale_y = target_height / height
            
            # 使用较大的缩放比例，确保覆盖整个画布
            scale = max(scale_x, scale_y)
            
            # 缩放图片
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 创建1600x900的画布
            canvas = Image.new('RGB', (target_width, target_height))
            
            # 计算居中位置
            x = (target_width - new_width) // 2
            y = (target_height - new_height) // 2
            
            # 如果缩放后的图片大于目标尺寸，需要裁剪
            if new_width > target_width or new_height > target_height:
                # 裁剪中心部分
                left = max(0, -x)
                top = max(0, -y)
                right = left + target_width
                bottom = top + target_height
                img = img.crop((left, top, right, bottom))
                x = 0
                y = 0
            
            # 粘贴到画布上
            canvas.paste(img, (x, y))
            print(f"模板已转换为标准尺寸: 1600x900")
            return canvas
        except Exception as e:
            if "模板尺寸不正确" in str(e):
                raise e  # 重新抛出尺寸错误
            else:
                print(f"Warning: Could not validate template size: {e}")
    
    def _get_chinese_font_paths(self):
        """获取中文字体路径 - 跨平台通用"""
        import platform
        
        paths = []
        system = platform.system()
        
        if system == "Linux":
            # Linux通用字体路径
            paths.extend([
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttf",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/arphic-uming/uming.ttc",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ])
        elif system == "Darwin":
            # macOS系统字体
            paths.extend([
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/Library/Fonts/NotoSansCJK-Bold.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/System/Library/Fonts/PingFang.ttc"
            ])
        elif system == "Windows":
            # Windows系统字体
            paths.extend([
                "C:\\Windows\\Fonts\\simhei.ttf",
                "C:\\Windows\\Fonts\\msyh.ttc",
                "C:\\Windows\\Fonts\\simsun.ttc"
            ])
        
        return paths
    
    def _get_english_font_paths(self):
        """获取英文字体路径 - 跨平台通用"""
        import platform
        
        paths = []
        system = platform.system()
        
        if system == "Linux":
            # Linux通用字体路径
            paths.extend([
                "/usr/share/fonts/truetype/lexend/Lexend-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
                "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ])
        elif system == "Darwin":
            # macOS系统字体
            paths.extend([
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/Arial.ttf",
                "/Library/Fonts/Arial Bold.ttf"
            ])
        elif system == "Windows":
            # Windows系统字体
            paths.extend([
                "C:\\Windows\\Fonts\\arial.ttf",
                "C:\\Windows\\Fonts\\arialbd.ttf",
                "C:\\Windows\\Fonts\\calibri.ttf"
            ])
        
        return paths
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言"""
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        total_chars = len(text.replace(' ', ''))
        
        if chinese_chars > 0 and chinese_chars / total_chars >= 0.3:
            return "chinese"
        return "english"
    
    def _get_best_font(self, text: str, font_size: int) -> ImageFont.FreeTypeFont:
        """根据文本内容选择最佳字体"""
        language = self._detect_language(text)
        
        print(f"文本: {text[:20]}... 语言: {language} 字体大小: {font_size}")
        
        # 按语言选择合适的字体
        font_list = self.font_paths.get(language, self.font_paths["english"])
        
        for font_path in font_list:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"成功加载字体: {font_path}")
                    return font
                except Exception as e:
                    print(f"字体加载失败 {font_path}: {e}")
                    continue
        
        # 最后的备选方案
        print("警告: 使用默认字体")
        try:
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()
    
    def _calculate_text_height(self, text: str, font: ImageFont.FreeTypeFont, max_width: int = None) -> int:
        """计算文字实际高度（包括换行）"""
        if not max_width:
            try:
                if hasattr(font, 'getbbox'):
                    bbox = font.getbbox(text)
                    return bbox[3] - bbox[1]
                else:
                    return 30
            except:
                return 30
        
        # 处理换行的情况
        lines = []
        words = text.split(' ')
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            try:
                if hasattr(font, 'getlength'):
                    test_width = font.getlength(test_line)
                else:
                    bbox = font.getbbox(test_line)
                    test_width = bbox[2] - bbox[0]
            except:
                test_width = len(test_line) * 15
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(current_line)
        
        # 计算总高度
        try:
            if hasattr(font, 'getbbox'):
                single_line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
            else:
                single_line_height = 30
        except:
            single_line_height = 30
        
        total_height = len(lines) * int(single_line_height * 1.3)
        return total_height
    
    def _calculate_font_size(self, image_width: int, image_height: int, text_type: str = "title") -> int:
        """根据图片尺寸计算合适的字体大小"""
        base_dimension = min(image_width, image_height)
        
        # 参考chapter代码的逻辑: 使用9.6%的基准尺寸
        if text_type == "title":
            return int(base_dimension * 0.096)  # 主标题最大
        else:  # author
            return int(base_dimension * 0.04)   # 作者较小
    
    def _draw_text_with_effects(self, draw: ImageDraw.Draw, text: str, 
                               position: Tuple[int, int], font: ImageFont.FreeTypeFont,
                               color: str = "#FFFFFF", shadow_offset: Tuple[int, int] = None,
                               shadow_color: str = "#333333", stroke_width: int = 0,
                               stroke_fill: str = "#000000", max_width: int = None):
        """绘制带效果的文字"""
        x, y = position
        
        # 处理文字换行
        if max_width:
            lines = []
            words = text.split(' ')
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                try:
                    if hasattr(font, 'getlength'):
                        test_width = font.getlength(test_line)
                    else:
                        bbox = font.getbbox(test_line)
                        test_width = bbox[2] - bbox[0]
                except:
                    test_width = len(test_line) * 15
                
                if test_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(current_line)
        else:
            lines = [text]
        
        # 计算行高
        try:
            if hasattr(font, 'getbbox'):
                bbox = font.getbbox("A")
                line_height = int((bbox[3] - bbox[1]) * 1.3)
            elif hasattr(font, 'size'):
                line_height = int(font.size * 1.3)
            else:
                line_height = int(30 * 1.3)
        except:
            line_height = int(30 * 1.3)
        
        # 绘制每一行
        for i, line in enumerate(lines):
            line_y = y + i * line_height
            
            # 绘制阴影
            if shadow_offset:
                shadow_x = x + shadow_offset[0]
                shadow_y = line_y + shadow_offset[1]
                draw.text((shadow_x, shadow_y), line, font=font, fill=shadow_color)
            
            # 绘制描边
            if stroke_width > 0:
                for dx in range(-stroke_width, stroke_width + 1):
                    for dy in range(-stroke_width, stroke_width + 1):
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, line_y + dy), line, font=font, fill=stroke_fill)
            
            # 绘制主文字
            draw.text((x, line_y), line, font=font, fill=color)
            
            print(f"绘制文字: {line} 位置: ({x}, {line_y}) 颜色: {color}")
    
    def _convert_to_square(self, image: Image.Image, target_size: int = 900) -> Image.Image:
        """将图片智能转换为正方形
        
        处理逻辑：
        1. 如果已经是target_size x target_size，直接返回
        2. 如果最小边 < target_size，等比例放大到最小边 = target_size
        3. 居中裁剪为target_size x target_size正方形
        """
        width, height = image.size
        
        # 1. 已经是目标尺寸的正方形，直接返回
        if width == target_size and height == target_size:
            print(f"图片已是目标尺寸: {target_size}x{target_size}")
            return image
        
        # 2. 判断最小边长
        min_side = min(width, height)
        
        # 3. 如果最小边长小于目标尺寸，先等比例放大
        if min_side < target_size:
            scale_factor = target_size / min_side
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"图片等比例放大: {width}x{height} -> {new_width}x{new_height} (缩放比例: {scale_factor:.2f})")
            
            # 更新尺寸
            width, height = new_width, new_height
        
        # 4. 居中裁剪为目标尺寸的正方形
        if width != target_size or height != target_size:
            # 计算裁剪位置（居中）
            left = (width - target_size) // 2
            top = (height - target_size) // 2
            right = left + target_size
            bottom = top + target_size
            
            # 裁剪为正方形
            square_image = image.crop((left, top, right, bottom))
            
            if width > height:
                print(f"横向图片居中裁剪: {width}x{height} -> {target_size}x{target_size} (左右各去掉{left}px)")
            elif height > width:
                print(f"纵向图片居中裁剪: {width}x{height} -> {target_size}x{target_size} (上下各去掉{top}px)")
            else:
                print(f"正方形图片裁剪: {width}x{height} -> {target_size}x{target_size}")
        else:
            square_image = image
            print(f"图片无需裁剪，已是目标尺寸: {target_size}x{target_size}")
        
        return square_image
    
    def _preprocess_logo(self, logo_path: str, target_size: int = LOGO_SIZE) -> Image.Image:
        """预处理Logo为固定大小的正方形"""
        try:
            logo = Image.open(logo_path)
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            # 智能转换为目标尺寸的正方形
            logo = self._convert_to_square(logo, target_size)
            print(f"Logo预处理完成: {target_size}x{target_size}")
            
            return logo
        except Exception as e:
            print(f"Logo预处理失败: {e}")
            return None
    
    def generate_final_thumbnail(self, 
                               title: str,
                               author: str = None, 
                               logo_path: str = None,
                               right_image_path: str = None,
                               output_path: str = "output.jpg",
                               theme: str = "dark",  # "dark", "light", "custom", "random", or None
                               custom_template: str = None,  # 自定义模板路径
                               title_color: str = None,  # 标题颜色，hex格式如"#FFFFFF"
                               author_color: str = None,  # 作者颜色，hex格式如"#CCCCCC"
                               enable_triangle: bool = None,  # 是否启用三角形
                               triangle_direction: str = "bottom",  # 三角形方向: "bottom"(倒梯形) 或 "top"(正梯形)
                               flip: bool = False,  # 是否镜像翻转布局
                               flip_margin: int = None,  # flip时的右边距，None时使用默认值50
                               youtube_ready: bool = True) -> str:  # 是否优化为YouTube API兼容格式
        """生成最终版缩略图"""
        
        # Check if user wants random generation
        if theme == "random" or theme is None:
            print(f"🎲 检测到随机主题请求 (theme={theme})，调用随机生成函数")
            return generate_random_thumbnail(
                title=title,
                author=author,
                logo_path=logo_path,
                right_image_path=right_image_path,
                output_path=output_path,
                google_api_key=self.title_optimizer.api_key if self.title_optimizer else None,
                youtube_ready=youtube_ready
            )
        
        print(f"开始生成最终缩略图: {output_path}")
        print(f"主题模式: {theme}")
        if theme != "custom":
            print(f"三角形方向: {triangle_direction} ({'正梯形' if triangle_direction == 'top' else '倒梯形'})")
        if flip:
            print(f"布局模式: 镜像翻转 (Flip=True)")
        
        # 根据主题选择模板和默认颜色
        actual_template_path = self.template_path
        triangle_path = get_resource_path("templates/triangle_template.png")  # 默认黑色
        
        if theme == "light":
            # Light主题：白底黑字白三角
            actual_template_path = get_resource_path("templates/light_template.png")
            # 根据方向选择三角形
            if triangle_direction == "top":
                triangle_path = get_resource_path("templates/triangle_white_top.png")
            else:  # bottom
                triangle_path = get_resource_path("templates/triangle_white.png")
            default_title_color = "#000000"  # 黑色字体
            default_author_color = "#666666"  # 深灰色作者
        elif theme == "custom":
            # 自定义主题：必须提供模板路径
            if not custom_template:
                raise ValueError("Custom主题必须提供custom_template参数")
            if not os.path.exists(custom_template):
                raise FileNotFoundError(f"自定义模板文件不存在: {custom_template}")
            
            actual_template_path = custom_template
            default_title_color = "#FFFFFF"  # 默认白字
            default_author_color = "#CCCCCC"  # 默认浅灰
            triangle_path = None  # 自定义模板不使用三角形
        else:
            # Dark主题（默认）：黑底白字黑三角
            actual_template_path = self.template_path
            # 根据方向选择三角形
            if triangle_direction == "top":
                triangle_path = get_resource_path("templates/triangle_black_top.png")
            else:  # bottom
                triangle_path = get_resource_path("templates/triangle_black.png")
            default_title_color = "#FFFFFF"  # 白色字体
            default_author_color = "#CCCCCC"  # 浅灰色作者
        
        # 应用用户指定的颜色，如果没有则使用主题默认颜色
        final_title_color = title_color if title_color else default_title_color
        final_author_color = author_color if author_color else default_author_color
        
        # 三角形启用逻辑
        if enable_triangle is None:
            # 默认逻辑：Dark和Light主题启用，Custom主题禁用
            use_triangle = (theme in ["dark", "light"])
        else:
            # 用户明确指定
            use_triangle = enable_triangle
        
        # 设置默认的 logo 和 image 路径 - 仅对 dark 和 light 主题
        if theme != "custom":  # 只有非 custom 主题才使用默认值
            if logo_path is None:
                default_logo = get_resource_path("logos/animagent_logo.png")
                if os.path.exists(default_logo):
                    logo_path = default_logo
                    print(f"使用默认 Logo: {logo_path}")
            
            if right_image_path is None:
                default_image = get_resource_path("assets/testing_image.jpeg")
                if os.path.exists(default_image):
                    right_image_path = default_image
                    print(f"使用默认右侧图片: {right_image_path}")
        else:
            # Custom 主题：用户没提供的就不添加
            if logo_path is None:
                print("Custom 主题：未提供 Logo，不添加")
            if right_image_path is None:
                print("Custom 主题：未提供右侧图片，不添加")
        
        print(f"实际模板: {actual_template_path}")
        print(f"标题颜色: {final_title_color}, 作者颜色: {final_author_color}")
        print(f"三角形: {'启用' if use_triangle else '禁用'} - {triangle_path if use_triangle else 'None'}")
        
        # 打开模板图片
        if theme == "custom":
            # Custom模板需要确保尺寸为1600x900
            template = self._ensure_template_size(actual_template_path)
        else:
            template = Image.open(actual_template_path)
        
        if template.mode != 'RGBA':
            template = template.convert('RGBA')
        
        width, height = template.size
        print(f"模板尺寸: {width}x{height}")
        
        # 所有模板统一使用1600x900的布局
        is_professional = True  # 统一使用专业模板布局
        
        # Flip 布局计算辅助函数
        def calc_x_position(x, element_width=0):
            """根据 flip 参数计算 X 位置"""
            if not flip:
                return x
            else:
                # 镜像翻转：x' = width - x - element_width
                return width - x - element_width
        
        # 创建绘图对象
        draw = ImageDraw.Draw(template)
        
        # 计算字体大小
        title_size = self._calculate_font_size(width, height, "title")
 
        author_size = self._calculate_font_size(width, height, "author")
        
        print(f"计算字体大小 - 标题:{title_size} 作者:{author_size}")
        
        # 第一层: 添加右侧图片（如果有）
        if right_image_path and os.path.exists(right_image_path):
            try:
                right_img = Image.open(right_image_path)
                if right_img.mode != 'RGBA':
                    right_img = right_img.convert('RGBA')
                
                # 将输入图片转换为正方形
                right_img = self._convert_to_square(right_img)
                
                # 确定右侧区域 - 新布局：左侧700px，右侧900px（flip时相反）
                if is_professional:  # 1600x900 -> 700x900 + 900x900
                    if not flip:
                        right_area = (700, 0, 1600, 900)
                    else:
                        right_area = (0, 0, 900, 900)  # flip时图片在左侧
                else:  # 1280x720
                    if not flip:
                        right_area = (640, 0, 1280, 720)
                    else:
                        right_area = (0, 0, 640, 720)
                
                right_width = right_area[2] - right_area[0]
                right_height = right_area[3] - right_area[1]
                
                print(f"右侧区域: {right_width}x{right_height}")
                
                # 对于专业模板，直接缩放正方形图片到900x900
                if is_professional:
                    # 缩放到900x900填满右侧区域
                    right_img = right_img.resize((900, 900), Image.Resampling.LANCZOS)
                    
                    # 根据参数决定是否添加三角形效果
                    if use_triangle and triangle_path:
                        try:
                            if os.path.exists(triangle_path):
                                triangle = Image.open(triangle_path)
                                if triangle.mode != 'RGBA':
                                    triangle = triangle.convert('RGBA')
                                
                                # 确保三角形尺寸匹配right_img高度
                                triangle_width, triangle_height = triangle.size
                                if triangle_height != 900:
                                    # 按比例缩放到900高度
                                    new_width = int(triangle_width * 900 / triangle_height)
                                    triangle = triangle.resize((new_width, 900), Image.Resampling.LANCZOS)
                                    print(f"三角形缩放到right_img尺寸: {triangle_width}x{triangle_height} -> {new_width}x900")
                                
                                # 在right_img的左侧贴三角形 (flip时贴在右侧并水平翻转)
                                if not flip:
                                    right_img.paste(triangle, (0, 0), triangle)
                                    print(f"三角形已贴到right_img左侧: 尺寸{triangle.size}")
                                else:
                                    # flip时：1.水平翻转三角形 2.贴在右侧
                                    triangle = triangle.transpose(Image.FLIP_LEFT_RIGHT)
                                    triangle_x = right_img.width - triangle.width
                                    right_img.paste(triangle, (triangle_x, 0), triangle)
                                    print(f"三角形已水平翻转并贴到right_img右侧: 位置({triangle_x}, 0), 尺寸{triangle.size}")
                                
                        except Exception as e:
                            print(f"在right_img上贴三角形失败: {e}")
                    
                    # 使用right_area的x坐标，已经考虑了flip
                    paste_x = right_area[0]  # flip时是0，标准时是700
                    paste_y = 0
                else:
                    # 标准模板保持原有逻辑
                    img_ratio = right_img.width / right_img.height
                    area_ratio = right_width / right_height
                    
                    if img_ratio > area_ratio:
                        new_height = right_height
                        new_width = int(new_height * img_ratio)
                    else:
                        new_width = right_width
                        new_height = int(new_width / img_ratio)
                    
                    right_img = right_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 居中放置
                    paste_x = right_area[0] + (right_width - new_width) // 2
                    paste_y = right_area[1] + (right_height - new_height) // 2
                
                # 使用计算好的居中位置
                template.paste(right_img, (paste_x, paste_y), right_img)
                position_desc = "左侧" if flip else "右侧"
                print(f"{position_desc}图片已添加: {right_image_path} -> ({paste_x}, {paste_y})")
                
            except Exception as e:
                print(f"右侧图片添加失败: {e}")
        
        # 第二层: 添加Logo（如果有） - 修复：左边距=上边距
        if logo_path and os.path.exists(logo_path):
            try:
                # 使用预处理函数，确保logo是正方形
                logo = self._preprocess_logo(logo_path, target_size=LOGO_SIZE)
                if logo is None:
                    raise Exception("Logo预处理失败")
                
                # Logo位置计算（使用配置的logo尺寸）
                logo_margin = 20  # Logo边距设置为20px
                logo_size = LOGO_SIZE   # Logo配置大小
                
                if not flip:
                    # 标准布局：左上角
                    logo_x = logo_margin
                    logo_y = logo_margin
                else:
                    # flip布局：右上角，右边距等于原左边距
                    logo_x = width - logo_margin - logo_size
                    logo_y = logo_margin
                
                print(f"Logo位置: ({logo_x}, {logo_y}), 大小: {logo_size}x{logo_size}")
                
                # 直接贴图（logo已经是配置尺寸的正方形）
                template.paste(logo, (logo_x, logo_y), logo)
                
                position_desc = "左上角" if not flip else "右上角"
                print(f"Logo已添加到{position_desc}: {logo_path} -> 位置({logo_x}, {logo_y})")
                
            except Exception as e:
                print(f"Logo添加失败: {e}")
        
        # 第三层: 使用PNG贴图方式添加标题文字
        # 标题边距全局变量
        title_margin = 50  # 标题左边距，统一控制
        base_margin = flip_margin if flip_margin is not None else title_margin
        
        if is_professional:
            text_x = base_margin  # 标准左边距，与Logo对齐
            title_y = 330  # 标题位置居中显示
            
            # 定义PNG尺寸
            title_png_size = (600, 300)
        else:
            text_x = 45  # 从40px调整到45px，往右5像素
            title_y = 280  # 标准模板居中位置
            title_png_size = (500, 250)
        
        # 暂存标题PNG，等三角形覆盖后再贴入
        title_img_data = None
        
        # 生成标题PNG（但先不贴入）
        if title:
            print(f"生成标题PNG（固定区域 600x280）")
            
            # Optimize title with Gemini API (if available) - AI handles length and line-breaking
            original_title = title
            ai_optimized = False
            
            if self.title_optimizer and self.title_optimizer.is_available:
                try:
                    title, was_optimized = self.title_optimizer.optimize_title(title)
                    if was_optimized:
                        print(f"Title optimized by Gemini: '{original_title}' -> '{title}'")
                        ai_optimized = True
                        # AI-optimized titles already have proper line-breaking, skip manual processing
                    else:
                        print(f"Title unchanged by Gemini: '{title}'")
                except Exception as e:
                    print(f"Title optimization failed: {e}")
                    title = original_title
            else:
                print("Title optimization skipped - no API key or Gemini unavailable")
            
            # Only apply manual processing if AI optimization was not used (fallback logic)
            if not ai_optimized:
                # 检测标题语言 (fallback)
                title_language = self._detect_language(title)
                
                # 中文标题限制18个字符，英文不限制 (fallback)
                if title_language == "chinese":
                    if len(title) > 18:
                        original_title_fallback = title
                        title = title[:18] + "..."  # 保留前18个字符，再追加3个点
                        print(f"中文标题截短 (fallback): '{original_title_fallback}' -> '{title}' (保留前18字符+...)")
                    # 如果正好18字符或更少，不需要处理
                
                # 英文标题限制3行 (fallback)
                max_title_lines = 3 if title_language == "english" else 6
            else:
                # AI optimized - use flexible detection for display
                title_language = self._detect_language(title.replace('\\n', '').replace('\n', ''))
                max_title_lines = 6  # Allow AI to determine line count
            
            # 将hex颜色转换为RGB元组
            def hex_to_rgb(hex_color):
                """将hex颜色转换为RGB元组"""
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            title_rgb = hex_to_rgb(final_title_color)
            
            success, title_img, _ = create_text_png(
                text=title,
                width=550,  # 从600改为550，给右侧更多缓冲空间
                height=280,  # 固定高度，不再自动调整
                text_color=title_rgb,  # 使用主题颜色
                language=title_language,
                auto_height=False,  # 关闭自动高度调整
                max_lines=max_title_lines,  # 英文3行，中文6行
                use_stroke=(theme == "custom"),  # custom主题使用黑色描边
                align='right' if flip else 'left'  # flip模式下使用右对齐
            )
            
            if success:
                # 获取标题PNG图片的实际尺寸
                title_img_width = title_img.size[0]  # PNG图片宽度 (应该是550)
                
                # 计算X位置
                if not flip:
                    # 标准布局：使用原来的text_x
                    final_text_x = text_x
                else:
                    # flip布局：X = 1600 - title_image_width - title_margin_right
                    # 1600 - 550 - 50 = 1000
                    final_text_x = width - title_img_width - title_margin
                
                title_img_data = (title_img, final_text_x, title_y)
                print(f"标题PNG已生成: 位置({final_text_x}, {title_y}), PNG宽度: {title_img_width}px")
                print(f"标题布局: {'右对齐' if flip else '左对齐'}, 固定尺寸(550, 280)")
        
        
        # 作者 - 使用PNG方式，固定在底部上方100px位置
        author_img_data = None
        if author:
            # 无论什么模板，作者都应该在底部上方100px的位置
            author_y = height - 100  # 距离底部100px
            
            # 将作者名改为全大写
            author_upper = author.upper()
            
            # 生成作者PNG
            # 将hex颜色转换为RGB
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            author_rgb = hex_to_rgb(final_author_color)
            
            # 创建作者PNG，宽度限制为400px
            success, author_img, _ = create_text_png(
                text=author_upper,
                width=400,
                height=60,  # 作者文字高度
                text_color=author_rgb,
                language='english',
                auto_height=False,
                max_lines=1,
                align='right' if flip else 'left'  # flip模式下使用右对齐
            )
            
            if success:
                # 获取作者PNG图片的实际尺寸
                author_img_width = author_img.size[0]  # PNG图片宽度 (应该是400)
                
                # 计算X位置
                if not flip:
                    # 标准布局：左对齐
                    author_x = text_x
                else:
                    # flip布局：X = 1600 - author_image_width - title_margin_right
                    # 1600 - 400 - 50 = 1150
                    author_x = width - author_img_width - title_margin
                
                author_img_data = (author_img, author_x, author_y)
                print(f"作者PNG已生成: 位置({author_x}, {author_y}), PNG宽度: {author_img_width}px")
                print(f"作者全大写: {author_upper}, {'右对齐' if flip else '左对齐'}")
        
        # 三角形已经在right_img处理阶段贴入，这里不再需要单独处理
        print("三角形效果已集成到右侧图片中")
        
        # 最终步骤: 贴入标题和作者PNG（在三角形之上）
        if title_img_data:
            title_img, tx, ty = title_img_data
            template.paste(title_img, (tx, ty), title_img)
            print(f"标题PNG最终贴入: 位置({tx}, {ty}) [最上层]")
        
        if author_img_data:
            author_img, ax, ay = author_img_data
            template.paste(author_img, (ax, ay), author_img)
            print(f"作者PNG最终贴入: 位置({ax}, {ay}) [最上层]")
        
        # 保存结果
        if template.mode == 'RGBA':
            # 转换为RGB保存为JPG，使用黑色背景
            rgb_image = Image.new('RGB', template.size, (0, 0, 0))
            rgb_image.paste(template, mask=template.split()[-1])
            rgb_image.save(output_path, 'JPEG', quality=95)
        else:
            template.save(output_path, 'JPEG', quality=95)
        
        print(f"最终缩略图生成完成: {output_path}")
        
        # If YouTube API optimization is requested, process the output
        if youtube_ready:
            print("🚀 Processing for YouTube API compliance...")
            # Use the original output_path for the optimized version
            temp_path = output_path.replace('.jpg', '_temp_original.jpg')
            # Rename current output to temp
            os.rename(output_path, temp_path)
            # Optimize to the original output_path
            youtube_optimized_path = optimize_for_youtube_api(temp_path, output_path)
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            print(f"✅ YouTube-ready thumbnail: {youtube_optimized_path}")
            return youtube_optimized_path
        
        return output_path

# Random Template Selection Functions

def get_random_template_config():
    """
    Generate random template configuration for 12 possible combinations
    
    12 Combinations:
    - Theme: dark, light (2 options)
    - Triangle: enabled or disabled (2 options)
    - Layout: standard, flip (2 options)
    - Triangle Direction: top, bottom (when triangle enabled)
    
    Breakdown:
    - With Triangle: 2 themes × 2 directions × 2 layouts = 8 combinations
    - Without Triangle: 2 themes × 2 layouts = 4 combinations
    - Total: 8 + 4 = 12 combinations
    
    Returns:
        dict: Random configuration with theme, enable_triangle, triangle_direction, and flip
    """
    
    themes = ["dark", "light"]
    enable_triangles = [True, False]
    triangle_directions = ["top", "bottom"] 
    flips = [False, True]
    
    theme = random.choice(themes)
    enable_triangle = random.choice(enable_triangles)
    flip = random.choice(flips)
    
    # Only set triangle_direction if triangle is enabled
    triangle_direction = random.choice(triangle_directions) if enable_triangle else "bottom"
    
    config = {
        "theme": theme,
        "enable_triangle": enable_triangle,
        "triangle_direction": triangle_direction,
        "flip": flip
    }
    
    return config

def generate_random_thumbnail(title: str,
                            author: str,
                            logo_path: str = None,
                            right_image_path: str = None,
                            output_path: str = "random_thumbnail.jpg",
                            google_api_key: str = None,
                            youtube_ready: bool = True) -> str:
    """
    Generate thumbnail with randomly selected template configuration
    
    User only needs to provide 4 basic inputs:
    - title: Title text
    - author: Author name  
    - logo_path: Path to logo image (optional, uses default if None)
    - right_image_path: Path to right-side image (optional, uses default if None)
    
    Template configuration is randomly selected from 8 possible combinations.
    
    Args:
        title (str): Title text for the thumbnail
        author (str): Author name for the thumbnail
        logo_path (str, optional): Path to logo image file
        right_image_path (str, optional): Path to right-side image file
        output_path (str): Output file path. Defaults to "random_thumbnail.jpg"
        google_api_key (str, optional): Google API key for AI title optimization
        youtube_ready (bool): Whether to optimize for YouTube API compliance
        
    Returns:
        str: Path to generated thumbnail file
        
    Example:
        # Simple usage - only provide title and author
        result = generate_random_thumbnail(
            title="AI技术指南 Complete Tutorial",
            author="TechChannel"
        )
        
        # With custom images
        result = generate_random_thumbnail(
            title="Learn Python Programming",
            author="CodeMaster", 
            logo_path="/path/to/logo.png",
            right_image_path="/path/to/image.jpg",
            output_path="my_thumbnail.jpg"
        )
    """
    
    # Get random template configuration
    config = get_random_template_config()
    
    print(f"🎲 Random Template Configuration:")
    print(f"   Theme: {config['theme']}")
    if config['enable_triangle']:
        print(f"   Triangle: Enabled ({config['triangle_direction']} direction)")
    else:
        print(f"   Triangle: Disabled")
    print(f"   Layout: {'Flip' if config['flip'] else 'Standard'}")
    print(f"   📁 Output: {output_path}")
    
    # Create generator with optional AI optimization
    generator = FinalThumbnailGenerator(google_api_key=google_api_key)
    
    # Generate thumbnail with random configuration
    result = generator.generate_final_thumbnail(
        title=title,
        author=author,
        logo_path=logo_path,
        right_image_path=right_image_path,
        output_path=output_path,
        theme=config["theme"],
        enable_triangle=config["enable_triangle"],
        triangle_direction=config["triangle_direction"],
        flip=config["flip"],
        youtube_ready=youtube_ready
    )
    
    print(f"🎉 Random thumbnail generated successfully!")
    return result

# 如需测试，请运行 example_usage.py