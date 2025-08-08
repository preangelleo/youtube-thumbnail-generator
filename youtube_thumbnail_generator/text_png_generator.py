#!/usr/bin/env python3
"""
基于通用字体检测的标题PNG生成器
专门用于生成指定尺寸的透明背景标题图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import platform

def _get_universal_font_paths(language="english"):
    """Get universal font paths based on system - no personalized detection"""
    system = platform.system()
    paths = []
    
    if language == "chinese":
        if system == "Linux":
            paths.extend([
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttf",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/arphic-uming/uming.ttc"
            ])
        elif system == "Darwin":  # macOS
            paths.extend([
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/Library/Fonts/NotoSansCJK-Bold.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/System/Library/Fonts/PingFang.ttc"
            ])
        elif system == "Windows":
            paths.extend([
                "C:\\Windows\\Fonts\\simhei.ttf",
                "C:\\Windows\\Fonts\\msyh.ttc", 
                "C:\\Windows\\Fonts\\simsun.ttc"
            ])
    else:  # english
        if system == "Linux":
            paths.extend([
                "/usr/share/fonts/truetype/lexend/Lexend-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf", 
                "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ])
        elif system == "Darwin":  # macOS
            paths.extend([
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/Arial.ttf", 
                "/Library/Fonts/Arial Bold.ttf"
            ])
        elif system == "Windows":
            paths.extend([
                "C:\\Windows\\Fonts\\arial.ttf",
                "C:\\Windows\\Fonts\\arialbd.ttf",
                "C:\\Windows\\Fonts\\calibri.ttf"
            ])
    
    return paths

def _get_best_font(text, font_size, language, is_title=False):
    """获取最佳字体（通用跨平台版本）"""
    font_paths = _get_universal_font_paths(language)
    
    # Try to load fonts in order
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception as e:
                print(f"Failed to load {path}: {e}")
                continue
    
    # Fallback to default font
    print(f"No suitable font found for {language}, using default")
    return ImageFont.load_default()

def create_text_png(text, width=600, height=300, font_size=None, 
                   text_color=(255, 255, 255), output_path=None, 
                   language='english', margin_ratio=0.05, auto_height=False, 
                   line_height_px=50, max_lines=3):
    """
    创建指定尺寸的透明背景文字PNG
    使用通用字体检测，支持跨平台
    
    Args:
        text (str): 要渲染的文本
        width (int): 图片宽度
        height (int): 图片高度  
        font_size (int): 字体大小，None时自动计算
        text_color (tuple): 文字颜色RGB
        output_path (str): 输出路径，None时不保存
        language (str): 语言 'chinese' 或 'english'
        margin_ratio (float): 边距比例
        auto_height (bool): 是否自动调整高度
        line_height_px (int): 行高像素
        max_lines (int): 最大行数
        
    Returns:
        tuple: (success, image, actual_height)
    """
    
    # 检测中文字符
    has_chinese = any(ord(c) > 127 for c in text)
    if has_chinese and language == 'english':
        language = 'chinese'
    
    # 创建透明背景图片
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算字体大小
    if font_size is None:
        base_dimension = min(width, height)
        font_size = int(base_dimension * 0.096)  # 9.6% of smaller dimension
    
    # 获取字体
    font = _get_best_font(text, font_size, language)
    
    # 计算最大文本宽度
    margin = int(width * margin_ratio)
    max_text_width = width - 2 * margin
    
    # 文本换行处理
    lines = []
    if language == 'chinese':
        # 中文换行逻辑
        current_line = ""
        for char in text:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_text_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    lines.append(char)
                    current_line = ""
                    
                if len(lines) >= max_lines:
                    break
                    
        if current_line and len(lines) < max_lines:
            lines.append(current_line)
    else:
        # 英文换行逻辑  
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= max_text_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
                    current_line = ""
                    
                if len(lines) >= max_lines:
                    break
                    
        if current_line and len(lines) < max_lines:
            lines.append(current_line)
    
    # 限制行数
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip() + "..."
    
    # 计算文本总高度
    if lines:
        bbox = draw.textbbox((0, 0), lines[0], font=font)
        single_line_height = bbox[3] - bbox[1]
        total_text_height = len(lines) * line_height_px
    else:
        total_text_height = 0
        
    # 自动调整高度
    actual_height = height
    if auto_height and total_text_height > 0:
        actual_height = total_text_height + 2 * margin
        img = Image.new('RGBA', (width, actual_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
    
    # 计算起始Y位置（垂直居中）
    start_y = (actual_height - total_text_height) // 2
    
    # 绘制文本
    current_y = start_y
    for line in lines:
        if line.strip():  # 只绘制非空行
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2  # 水平居中
            
            draw.text((x, current_y), line, fill=text_color, font=font)
        
        current_y += line_height_px
    
    # 保存文件
    if output_path:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        img.save(output_path, 'PNG')
        print(f"Text PNG saved: {output_path}")
    
    return True, img, actual_height

if __name__ == "__main__":
    # 测试代码
    print("Testing universal text PNG generator...")
    
    # 测试英文
    success, img, height = create_text_png(
        "Hello World Universal Test", 
        width=600, 
        height=300,
        language='english',
        output_path="test_english_universal.png"
    )
    print(f"English test: {'✓' if success else '✗'}")
    
    # 测试中文
    success, img, height = create_text_png(
        "通用中文字体测试", 
        width=600, 
        height=300,
        language='chinese',
        output_path="test_chinese_universal.png"
    )
    print(f"Chinese test: {'✓' if success else '✗'}")