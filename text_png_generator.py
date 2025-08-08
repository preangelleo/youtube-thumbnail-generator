#!/usr/bin/env python3
"""
基于function_add_chapter逻辑的文字PNG生成器
专门用于生成指定尺寸的透明背景文字图片
"""

from PIL import Image, ImageDraw, ImageFont
import os
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

def create_text_png(text, width=600, height=300, font_size=None, 
                   text_color=(255, 255, 255), output_path=None, 
                   language='english', margin_ratio=0.05, auto_height=False, 
                   line_height_px=50, max_lines=3):
    """
    创建指定尺寸的透明背景文字PNG
    基于function_add_chapter的逻辑但针对小尺寸图片优化
    
    Args:
        text (str): 要渲染的文字
        width (int): PNG宽度
        height (int): PNG高度  
        font_size (int): 字体大小，None时自动计算
        text_color (tuple): 文字颜色RGB
        output_path (str): 输出路径，None时返回Image对象
        language (str): 语言类型 'english' 或 'chinese'
        margin_ratio (float): 边距比例，默认5%
        auto_height (bool): 是否根据文字行数自动调整高度
        line_height_px (int): 每行高度（像素）
        max_lines (int): 最大行数，超过则截断
    
    Returns:
        tuple: (success, result, actual_height) success为bool，result为路径或Image对象，actual_height为实际高度
    """
    
    # 计算字体大小（如果未提供）
    if font_size is None:
        base_dimension = min(width, height)
        if auto_height and line_height_px >= 50:  # 标题模式
            font_size = 45  # 标题固定45px字体
        elif height <= 50:  # 对于副标题（600x50），使用固定20px字体
            font_size = 20  # 固定20px
        elif height <= 120:  # 对于矮的PNG，使用更大比例
            font_size = int(base_dimension * 0.35)  # 35%比例
        else:
            font_size = int(base_dimension * 0.15)  # 15%比例
    
    # 中文字体增大30%
    if language == 'chinese':
        font_size = int(font_size * 1.3)  # 中文字体比英文大30%
        print(f"中文字体增大30%: {int(font_size/1.3)}px -> {font_size}px")

    # 获取字体 - 判断是否为标题（大字体或固定大尺寸都算标题）
    is_title = (auto_height and line_height_px >= 50) or (font_size >= 40 and height >= 200)
    font = _get_best_font(text, font_size, language, is_title)
    
    # 如果启用auto_height，预计算所需行数
    if auto_height:
        # 临时计算可用宽度
        if height <= 50:  # 副标题特殊处理
            temp_left_margin = 20
            temp_max_width = width - temp_left_margin - 5
        else:
            temp_margin = int(min(width, height) * margin_ratio)
            temp_max_width = width - 2 * temp_margin
        
        # 预计算换行
        lines = _wrap_text(text, font, temp_max_width, language, is_title)
        num_lines = len(lines)
        
        print(f"预计算: 文字需要{num_lines}行")
        
        # 如果超过最大行数，进行截断
        if num_lines > max_lines:
            print(f"需要截断: {num_lines}行 > {max_lines}行限制")
            
            # 截断到max_lines-1行，最后一行加省略号
            truncated_lines = lines[:max_lines-1]
            last_line = lines[max_lines-1]
            
            # 为最后一行添加省略号，并确保不超宽
            while True:
                test_line = last_line + "..."
                try:
                    if hasattr(font, 'getlength'):
                        test_width = font.getlength(test_line)
                    else:
                        bbox = font.getbbox(test_line)
                        test_width = bbox[2] - bbox[0]
                except:
                    test_width = len(test_line) * (font_size * 0.6)
                
                if test_width <= temp_max_width:
                    truncated_lines.append(test_line)
                    break
                else:
                    # 缩短最后一行文字
                    if len(last_line) > 3:
                        last_line = last_line[:-3]
                    else:
                        truncated_lines.append("...")
                        break
            
            lines = truncated_lines
            num_lines = len(lines)
            text = ' '.join(lines)  # 重新组合文字
            print(f"截断后: {num_lines}行, 文字: {text}")
        
        # 根据行数调整高度，为多行文字添加额外间距
        if num_lines > 1:
            # 多行时：基础高度 + 行间距 - 标题用更大间距
            if is_title and line_height_px >= 50:  # 标题
                extra_spacing = (num_lines - 1) * 16  # 标题每行之间16px间距
            else:  # 副标题
                extra_spacing = (num_lines - 1) * 8   # 副标题每行之间8px间距
            height = num_lines * line_height_px + extra_spacing
            print(f"智能调整高度: {height}px ({num_lines}行 x {line_height_px}px + {extra_spacing}px行间距)")
        else:
            height = num_lines * line_height_px
            print(f"智能调整高度: {height}px ({num_lines}行 x {line_height_px}px/行)")
        
        # 中文副标题增加20%高度
        if language == 'chinese' and not is_title:  # 仅对副标题生效
            original_height = height
            height = int(height * 1.2)  # 中文副标题高度增加20%
            print(f"中文副标题高度增加20%: {original_height}px -> {height}px")
    
    # 创建透明背景的RGBA图片
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 透明背景
    draw = ImageDraw.Draw(img)
    
    # 计算可用区域（统一左边距）
    if height <= 50:  # 副标题特殊处理，增加左边距
        left_margin = 20  # 左边距20px
        top_margin = int(height * margin_ratio)
        max_width = width - left_margin - 5  # 右边距只留5px，给文字更多空间
        max_height = height - 2 * top_margin
    else:  # 标题也使用相同的左边距20px，保持左对齐
        left_margin = 20  # 与副标题相同的左边距
        top_margin = int(min(width, height) * margin_ratio)
        max_width = width - left_margin - 20  # 右边距20px
        max_height = height - 2 * top_margin
    
    print(f"创建文字PNG: {width}x{height}, 字体{font_size}px, 可用区域{max_width}x{max_height}")
    
    # 处理文字换行
    lines = _wrap_text(text, font, max_width, language, is_title)
    
    # 英文标题强制3行限制（即使auto_height=False）
    if language == 'english' and font_size >= 40:  # 大字体标题
        if len(lines) > 3:
            print(f"英文标题截断: {len(lines)}行 -> 3行")
            # 截断到2行，第3行加省略号
            truncated_lines = lines[:2]
            last_line = lines[2]
            
            # 为第3行添加省略号
            while True:
                test_line = last_line + "..."
                try:
                    if hasattr(font, 'getlength'):
                        test_width = font.getlength(test_line)
                    else:
                        bbox = font.getbbox(test_line)
                        test_width = bbox[2] - bbox[0]
                except:
                    test_width = len(test_line) * (font_size * 0.6)
                
                if test_width <= max_width:
                    truncated_lines.append(test_line)
                    break
                else:
                    if len(last_line) > 3:
                        last_line = last_line[:-3]
                    else:
                        truncated_lines.append("...")
                        break
            
            lines = truncated_lines
    
    # 计算总文字高度
    line_height = _get_line_height(font)
    total_text_height = len(lines) * line_height
    
    # 如果文字太高，缩小字体
    if total_text_height > max_height:
        scale_factor = max_height / total_text_height * 0.9  # 留10%缓冲
        new_font_size = int(font_size * scale_factor)
        font = _get_best_font(text, new_font_size, language)
        lines = _wrap_text(text, font, max_width, language, is_title)
        line_height = _get_line_height(font)
        total_text_height = len(lines) * line_height
        print(f"文字过高，缩小字体: {font_size}px -> {new_font_size}px")
    
    # 计算起始位置（居中）
    start_x = left_margin
    start_y = top_margin + (max_height - total_text_height) // 2
    
    # 绘制文字（添加描边和阴影效果）
    for i, line in enumerate(lines):
        # 为多行文字添加行间距 - 标题使用更大的行间距
        if len(lines) > 1:
            if font_size >= 40:  # 标题大字体
                line_spacing = 16  # 标题用16px行间距
            else:  # 副标题小字体
                line_spacing = 8   # 副标题用8px行间距
            line_y = start_y + i * (line_height + line_spacing)
        else:
            line_y = start_y + i * line_height
        
        # 增强阴影效果（特别是接近三角形区域的文字）
        shadow_offset = max(2, font_size // 25)  # 增大阴影偏移
        draw.text((start_x + shadow_offset, line_y + shadow_offset), 
                 line, font=font, fill=(0, 0, 0, 200))  # 更浓的阴影
        
        # 增强描边效果
        stroke_width = max(2, font_size // 30)  # 增大描边宽度
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((start_x + dx, line_y + dy), 
                             line, font=font, fill=(0, 0, 0, 255))  # 黑色描边
        
        # 额外的白色背景层（确保文字在任何背景上都清晰）
        bg_stroke = max(1, font_size // 35)
        for dx in range(-bg_stroke, bg_stroke + 1):
            for dy in range(-bg_stroke, bg_stroke + 1):
                if dx != 0 or dy != 0:
                    draw.text((start_x + dx, line_y + dy), 
                             line, font=font, fill=(50, 50, 50, 255))  # 深灰背景层
        
        # 绘制更亮的主文字
        bright_color = tuple(min(255, c + 30) for c in text_color[:3]) + (255,)  # 更亮的颜色
        draw.text((start_x, line_y), line, font=font, fill=bright_color)
        print(f"绘制文字行: '{line}' at ({start_x}, {line_y})")
    
    # 保存或返回
    if output_path:
        img.save(output_path, 'PNG')
        print(f"文字PNG已保存: {output_path}")
        return True, output_path, height
    else:
        return True, img, height

def _get_best_font(text, font_size, language, is_title=False):
    """获取最佳字体（基于function_add_chapter逻辑）"""
    system_info = detect_system()
    current_system = system_info.get('system', 'Unknown')
    
    font_paths = []
    
    if language == 'chinese':
        if current_system in ['RunPod', 'AWS', 'TB']:
            if is_title:  # 中文大标题：方正黑体
                font_paths = [
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
                ]
            else:  # 中文副标题：霞鹜文楷 Bold
                font_paths = [
                    "/usr/share/fonts/truetype/lxgw/LXGWWenKai-Bold.ttf",
                    "/usr/local/share/fonts/LXGWWenKai-Bold.ttf",
                    "/home/ubuntu/.local/share/fonts/LXGWWenKai-Bold.ttf",
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
                ]
        else:  # Mac
            if is_title:  # 中文大标题：方正黑体
                font_paths = [
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/STHeiti Medium.ttc", 
                    "/System/Library/Fonts/STHeiti Light.ttc",
                    "/Library/Fonts/NotoSansCJK-Bold.ttc"
                ]
            else:  # 中文副标题：霞鹜文楷 Bold
                font_paths = [
                    "/usr/share/fonts/truetype/lxgw/LXGWWenKai-Bold.ttf",
                    "/usr/local/share/fonts/LXGWWenKai-Bold.ttf", 
                    "/home/ubuntu/.local/share/fonts/LXGWWenKai-Bold.ttf",
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/STHeiti Medium.ttc"
                ]
    else:  # English - 英文标题用Lexend Bold，限制3行
        if current_system in ['RunPod', 'AWS', 'TB']:
            font_paths = [
                "/usr/share/fonts/truetype/lexend/Lexend-Bold.ttf",
                "/home/ubuntu/.local/share/fonts/Lexend/Lexend-Bold.ttf",
                "/usr/local/share/fonts/Lexend-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf"
            ]
        else:  # Mac
            font_paths = [
                "/Users/lgg/Library/Fonts/Lexend/Lexend-Bold.ttf",
                "/Library/Fonts/Lexend-Bold.ttf",
                "/System/Library/Fonts/Lexend-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/Ubuntu-Bold.ttf"
            ]
    
    # 尝试加载字体
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                print(f"加载字体成功: {font_path}")
                return font
            except Exception as e:
                continue
    
    # 使用默认字体
    print("使用默认字体")
    return ImageFont.load_default()

def _chinese_smart_wrap(text, max_chars=20, is_title=False):
    """中文智能换行算法"""
    # 标题和副标题使用不同的字符限制
    if is_title:
        max_chars = 9  # 标题限制9个字一行
    else:
        max_chars = 20  # 副标题限制20个字一行
    
    # 去掉空格再计算字符数（空格不算字符）
    text_no_space = text.replace(' ', '')
    if len(text_no_space) <= max_chars:
        return [text]
    
    # 超过限制，需要换行
    print(f"中文{'标题' if is_title else '副标题'}超过{max_chars}字，需要换行: {len(text_no_space)}字")
    
    # 除以2算法 - 基于原始文本（包含空格）
    total_chars = len(text)
    if total_chars % 2 == 0:
        # 偶数：平均分配
        first_line_chars = total_chars // 2
        second_line_chars = total_chars // 2
    else:
        # 奇数：第二行比第一行多一个字
        first_line_chars = total_chars // 2
        second_line_chars = total_chars // 2 + 1
    
    first_line = text[:first_line_chars]
    second_line = text[first_line_chars:first_line_chars + second_line_chars]
    
    print(f"中文智能换行: 第一行{len(first_line)}字, 第二行{len(second_line)}字")
    print(f"第一行: '{first_line}'")
    print(f"第二行: '{second_line}'")
    
    return [first_line, second_line]

def _wrap_text(text, font, max_width, language='english', is_title=False):
    """文字换行处理 - 支持中文智能换行"""
    
    # 中文特殊处理
    if language == 'chinese':
        return _chinese_smart_wrap(text, is_title=is_title)
    
    # 英文原有逻辑
    # 先尝试单行显示
    try:
        if hasattr(font, 'getlength'):
            text_width = font.getlength(text)
        else:
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
    except:
        text_width = len(text) * (font.size if hasattr(font, 'size') else 12) * 0.6
    
    # 如果单行能显示，直接返回
    if text_width <= max_width:
        return [text]
    
    # 否则按空格分词换行
    words = text.split(' ')
    lines = []
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
            test_width = len(test_line) * (font.size if hasattr(font, 'size') else 12) * 0.6
        
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)  # 单词太长也要加入
    
    if current_line:
        lines.append(current_line)
    
    return lines

def _get_line_height(font):
    """获取行高"""
    try:
        if hasattr(font, 'getbbox'):
            bbox = font.getbbox("A")
            text_height = bbox[3] - bbox[1]
            return int(text_height + 8)  # 文字高度 + 8px行间距
        elif hasattr(font, 'size'):
            return int(font.size + 8)  # 字体大小 + 8px行间距
        else:
            return 28  # 20px字体 + 8px间距
    except:
        return 28

# 如需测试PNG生成，请运行 example_usage.py