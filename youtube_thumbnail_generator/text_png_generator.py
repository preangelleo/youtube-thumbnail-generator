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
                "/Library/Fonts/Lexend-Bold.ttf",  # 优先使用Lexend Bold
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # Arial Bold优先于普通Arial
                "/Library/Fonts/Arial Bold.ttf",   # 用户安装的Arial Bold
                "/System/Library/Fonts/Arial.ttf", 
                "/System/Library/Fonts/Helvetica.ttc"  # Helvetica作为最后fallback
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
                font = ImageFont.truetype(path, font_size)
                print(f"成功加载字体: {path}")
                return font
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
    恢复完整的字体缩放、对齐、换行功能
    
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
    
    # 计算字体大小（恢复动态缩放逻辑）
    if font_size is None:
        base_dimension = min(width, height)
        
        # 判断是否为标题：大尺寸（宽度>=500且高度>=250）或者auto_height模式
        is_large_title = (width >= 500 and height >= 250)
        
        if auto_height and line_height_px >= 50:  # 标题模式
            font_size = 45  # 标题固定45px字体
        elif is_large_title:  # 大尺寸标题（final_thumbnail_generator调用的）
            font_size = 45  # 大标题固定45px字体
        elif height <= 120:  # 对于矮的PNG，使用更大比例
            font_size = int(base_dimension * 0.35)  # 35%比例
        else:
            font_size = int(base_dimension * 0.15)  # 15%比例
    
    # 中文字体增大30%（恢复中文字体优化）
    if language == 'chinese':
        font_size = int(font_size * 1.3)  # 中文字体比英文大30%
        print(f"中文字体增大30%: {int(font_size/1.3)}px -> {font_size}px")
    
    # 判断是否为标题
    is_title = (auto_height and line_height_px >= 50) or (font_size >= 40 and height >= 200)
    
    # 获取字体
    font = _get_best_font(text, font_size, language, is_title)
    
    # 创建透明背景图片
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算可用区域（恢复左对齐系统）
    left_margin = 20  # 固定左边距20px
    top_margin = int(min(width, height) * margin_ratio)
    max_width = width - left_margin - 20  # 右边距20px
    max_height = height - 2 * top_margin
    
    print(f"创建文字PNG: {width}x{height}, 字体{font_size}px, 可用区域{max_width}x{max_height}")
    
    # 处理文字换行（恢复智能换行算法）
    lines = _wrap_text(text, font, max_width, language, is_title)
    
    # 如果启用auto_height，重新计算高度（恢复自动高度调整）
    if auto_height:
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
                
                if test_width <= max_width:
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
            else:  # 小标题
                extra_spacing = (num_lines - 1) * 8   # 小标题每行之间8px间距
            height = num_lines * line_height_px + extra_spacing
            print(f"智能调整高度: {height}px ({num_lines}行 x {line_height_px}px + {extra_spacing}px行间距)")
        else:
            height = num_lines * line_height_px
            print(f"智能调整高度: {height}px ({num_lines}行 x {line_height_px}px/行)")
        
        # 重新创建图片
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        max_height = height - 2 * top_margin
    
    # 动态字体放大（中文和英文标题都生效）
    if is_title:
        if language == 'chinese':
            # 计算最长行的字符数
            max_line_chars = max(len(line.replace(' ', '')) for line in lines)
            
            # 根据最长行字符数计算字体放大倍数
            if max_line_chars < 9:  # 少于9个字需要放大
                # 计算放大倍数：9字=正常，8字=+20%，7字=+40%，以此类推
                scale_multiplier = 1.0 + (9 - max_line_chars) * 0.2
                new_font_size = int(font_size * scale_multiplier)
                
                print(f"动态字体放大: 最长行{max_line_chars}字 -> 字体{font_size}px * {scale_multiplier:.1f} = {new_font_size}px")
                
                # 重新生成字体和换行
                font = _get_best_font(text, new_font_size, language, is_title)
                lines = _wrap_text(text, font, max_width, language, is_title)
                font_size = new_font_size  # 更新字体大小变量
            else:
                print(f"字体大小保持不变: 最长行{max_line_chars}字 (≥9字)")
        
        elif language == 'english':
            # 英文动态缩放：计算总单词数
            total_words = len(text.split())
            
            # 英文动态缩放：7单词=正常，少于7单词需要放大
            if total_words < 7:  # 少于7个单词需要放大
                # 计算放大倍数：7单词=正常，6单词=+15%，5单词=+30%，以此类推
                scale_multiplier = 1.0 + (7 - total_words) * 0.15
                new_font_size = int(font_size * scale_multiplier)
                
                print(f"英文动态字体放大: {total_words}单词 -> 字体{font_size}px * {scale_multiplier:.1f} = {new_font_size}px")
                
                # 重新生成字体和换行
                font = _get_best_font(text, new_font_size, language, is_title)
                lines = _wrap_text(text, font, max_width, language, is_title)
                font_size = new_font_size  # 更新字体大小变量
            else:
                print(f"英文字体大小保持不变: {total_words}单词 (≥7单词)")
    
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
    
    # 计算起始位置（左对齐，垂直居中）
    start_x = left_margin
    start_y = top_margin + (max_height - total_text_height) // 2
    
    # 绘制文字（添加正确的行间距）
    for i, line in enumerate(lines):
        # 为多行文字添加行间距 - 标题使用更大的行间距
        if len(lines) > 1:
            if font_size >= 40:  # 标题大字体
                line_spacing = 16  # 标题用16px行间距
            else:  # 标题小字体
                line_spacing = 8   # 小字体用8px行间距
            line_y = start_y + i * (line_height + line_spacing)
        else:
            line_y = start_y + i * line_height
        
        # 绘制文字（左对齐）
        draw.text((start_x, line_y), line, font=font, fill=text_color)
        print(f"绘制文字行: '{line}' at ({start_x}, {line_y})")
    
    # 保存文件
    if output_path:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        img.save(output_path, 'PNG')
        print(f"Text PNG saved: {output_path}")
    
    return True, img, height

def _chinese_smart_wrap(text, max_chars=20, is_title=False):
    """中文智能换行算法 - 新增特殊换行规则"""
    # 标题和小字体使用不同的字符限制
    if is_title:
        max_chars = 9  # 标题限制9个字一行
    else:
        max_chars = 20  # 小字体限制20个字一行
    
    # 去掉空格再计算字符数（空格不算字符）
    text_no_space = text.replace(' ', '')
    total_chars_no_space = len(text_no_space)
    
    # 特殊规则：2-3个字强制单行显示，不允许换行
    if is_title and total_chars_no_space <= 3:
        print(f"特殊规则：{total_chars_no_space}个字强制单行显示")
        return [text]
    
    # 如果字符数在限制内，单行显示
    if total_chars_no_space <= max_chars:
        return [text]
    
    # 4个字及以上才允许换行
    if is_title and total_chars_no_space >= 4:
        print(f"中文标题{total_chars_no_space}字，需要换行")
        
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
    
    # 其他情况按原逻辑处理
    print(f"中文{'标题' if is_title else '文字'}超过{max_chars}字，需要换行: {total_chars_no_space}字")
    
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