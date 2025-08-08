#!/usr/bin/env python3
"""
最终版YouTube缩略图生成器
按用户要求修改：Logo左边距=上边距，只保留title+subtitle，author大写
"""

from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional, Dict, Any
import os
from dataclasses import dataclass
import textwrap
import platform
try:
    from .text_png_generator import create_text_png
except ImportError:
    from text_png_generator import create_text_png

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
    
    def __init__(self, template_path: str):
        """初始化生成器"""
        self.template_path = template_path
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")
            
        # 获取系统信息
        self.system_info = detect_system()
        self.current_system = self.system_info.get('system', 'Unknown')
        print(f"检测到系统: {self.current_system}")
        
        # 字体优先级列表
        self.font_paths = {
            # 中文字体
            "chinese": self._get_chinese_font_paths(),
            # 英文字体 - Lexend Bold
            "english": self._get_english_font_paths()
        }
    
    def _get_chinese_font_paths(self):
        """获取中文字体路径"""
        if self.current_system in ['RunPod', 'AWS', 'TB']:
            return [
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/lxgw/LXGWWenKai-Bold.ttf",
                "/usr/local/share/fonts/LXGWWenKai-Bold.ttf",
                "/home/ubuntu/.local/share/fonts/LXGWWenKai-Bold.ttf"
            ]
        else:  # Mac
            return [
                "/System/Library/Fonts/NotoSansCJK-Bold.ttc",
                "/Library/Fonts/NotoSansCJK-Bold.ttc",
                "/Users/lgg/Library/Fonts/NotoSansCJK-Bold.ttc"
            ]
    
    def _get_english_font_paths(self):
        """获取英文字体路径"""
        if self.current_system in ['RunPod', 'AWS', 'TB']:
            return [
                "/usr/share/fonts/truetype/lexend/Lexend-Bold.ttf",
                "/home/ubuntu/.local/share/fonts/Lexend/Lexend-Bold.ttf",
                "/usr/local/share/fonts/Lexend-Bold.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
                "/usr/share/fonts/ubuntu/Ubuntu-B.ttf",
                "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-Bold.ttf"
            ]
        else:  # Mac
            return [
                "/Users/lgg/Library/Fonts/Lexend/Lexend-Bold.ttf",
                "/Library/Fonts/Lexend-Bold.ttf",
                "/System/Library/Fonts/Lexend-Bold.ttf",
                "/System/Library/Fonts/Ubuntu-Bold.ttf",
                "/Library/Fonts/Ubuntu-Bold.ttf"
            ]
    
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
        elif text_type == "subtitle":
            return int(base_dimension * 0.06)   # 副标题中等
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
    
    def _convert_to_square(self, image: Image.Image) -> Image.Image:
        """将图片转换为正方形（居中裁剪）"""
        width, height = image.size
        
        # 选择较小的边作为正方形的边长
        size = min(width, height)
        
        # 计算裁剪位置（居中）
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        
        # 裁剪为正方形
        square_image = image.crop((left, top, right, bottom))
        print(f"图片转换为正方形: {width}x{height} -> {size}x{size}")
        
        return square_image
    
    def generate_final_thumbnail(self, 
                               title: str,
                               subtitle: str = None,
                               author: str = None, 
                               logo_path: str = None,
                               right_image_path: str = None,
                               output_path: str = "output.jpg") -> str:
        """生成最终版缩略图"""
        
        print(f"开始生成最终缩略图: {output_path}")
        print(f"模板: {self.template_path}")
        
        # 打开模板图片
        template = Image.open(self.template_path)
        if template.mode != 'RGBA':
            template = template.convert('RGBA')
        
        width, height = template.size
        print(f"模板尺寸: {width}x{height}")
        
        # 判断是否为专业模板
        is_professional = width >= 1500
        
        # 创建绘图对象
        draw = ImageDraw.Draw(template)
        
        # 计算字体大小
        title_size = self._calculate_font_size(width, height, "title")
        subtitle_size = self._calculate_font_size(width, height, "subtitle") 
        author_size = self._calculate_font_size(width, height, "author")
        
        print(f"计算字体大小 - 标题:{title_size} 副标题:{subtitle_size} 作者:{author_size}")
        
        # 第一层: 添加右侧图片（如果有）
        if right_image_path and os.path.exists(right_image_path):
            try:
                right_img = Image.open(right_image_path)
                if right_img.mode != 'RGBA':
                    right_img = right_img.convert('RGBA')
                
                # 将输入图片转换为正方形
                right_img = self._convert_to_square(right_img)
                
                # 确定右侧区域 - 新布局：左侧700px，右侧900px
                if is_professional:  # 1600x900 -> 700x900 + 900x900
                    right_area = (700, 0, 1600, 900)
                else:  # 1280x720
                    right_area = (640, 0, 1280, 720)
                
                right_width = right_area[2] - right_area[0]
                right_height = right_area[3] - right_area[1]
                
                print(f"右侧区域: {right_width}x{right_height}")
                
                # 对于专业模板，直接缩放正方形图片到900x900
                if is_professional:
                    # 缩放到900x900填满右侧区域
                    right_img = right_img.resize((900, 900), Image.Resampling.LANCZOS)
                    
                    # 如果需要斜角效果，先在right_img上贴三角形
                    # TODO: 这里可以添加斜角参数控制
                    add_diagonal = True  # 暂时硬编码，后续可作为参数
                    
                    if add_diagonal:
                        try:
                            triangle_path = "templates/triangle_template.png"
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
                                
                                # 在right_img的左侧贴三角形 (x=0位置)
                                right_img.paste(triangle, (0, 0), triangle)
                                print(f"三角形已贴到right_img左侧: 尺寸{triangle.size}")
                                
                        except Exception as e:
                            print(f"在right_img上贴三角形失败: {e}")
                    
                    paste_x = 700  # 直接放在右侧区域起始位置
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
                
                template.paste(right_img, (paste_x, paste_y), right_img)
                print(f"右侧图片已添加: {right_image_path} -> ({paste_x}, {paste_y})")
                
            except Exception as e:
                print(f"右侧图片添加失败: {e}")
        
        # 第二层: 添加Logo（如果有） - 修复：左边距=上边距
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                
                # Logo区域 - 修复：左边距=上边距
                if is_professional:
                    logo_area = (50, 50, 290, 200)  # 左边距从60改为50，与上边距相同
                else:
                    logo_area = (40, 40, 240, 160)  # 标准版本保持一致
                
                logo_width = logo_area[2] - logo_area[0]
                logo_height = logo_area[3] - logo_area[1]
                
                # 按比例缩放Logo
                logo_ratio = logo.width / logo.height
                area_ratio = logo_width / logo_height
                
                if logo_ratio > area_ratio:
                    new_width = logo_width
                    new_height = int(new_width / logo_ratio)
                else:
                    new_height = logo_height
                    new_width = int(new_height * logo_ratio)
                
                logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 直接放置Logo在左上角（左边距=上边距）
                paste_x = logo_area[0]  # 直接使用左边距，不居中
                paste_y = logo_area[1]  # 直接使用上边距，不居中
                
                template.paste(logo, (paste_x, paste_y), logo)
                print(f"Logo已添加: {logo_path} -> ({paste_x}, {paste_y})")
                
            except Exception as e:
                print(f"Logo添加失败: {e}")
        
        # 第三层: 使用PNG贴图方式添加文字
        if is_professional:
            text_x = 55  # 从50px调整到55px，往右5像素
            # 如果没有副标题，标题下移50px居中显示
            if not subtitle:
                title_y = 330  # 标题位置下移50px (280 + 50)
                print("无副标题，标题位置下移50px居中显示")
            else:
                title_y = 280  # 标题位置
            subtitle_y = 580  # 副标题位置（在标题下方）
            
            # 定义PNG尺寸
            title_png_size = (600, 300)
            subtitle_png_size = (600, 50)
        else:
            text_x = 45  # 从40px调整到45px，往右5像素
            # 标准模板也应用同样逻辑
            if not subtitle:
                title_y = 280  # 标准模板下移50px (230 + 50)
                print("无副标题，标题位置下移50px居中显示")
            else:
                title_y = 230
            subtitle_y = 480
            title_png_size = (500, 250)
            subtitle_png_size = (500, 180)
        
        # 暂存标题和副标题PNG，等三角形覆盖后再贴入
        title_img_data = None
        subtitle_img_data = None
        
        # 生成标题PNG（但先不贴入）
        if title:
            print(f"生成标题PNG（固定区域 600x280）")
            # 检测标题语言
            title_language = self._detect_language(title)
            # 英文标题限制3行
            max_title_lines = 3 if title_language == "english" else 6
            
            success, title_img, _ = create_text_png(
                text=title,
                width=550,  # 从600改为550，给右侧更多缓冲空间
                height=280,  # 固定高度，不再自动调整
                text_color=(255, 255, 255),  # 白色
                language=title_language,
                auto_height=False,  # 关闭自动高度调整
                max_lines=max_title_lines  # 英文3行，中文6行
            )
            
            if success:
                title_img_data = (title_img, text_x, title_y)
                print(f"标题PNG已生成，等待最终贴入: 位置({text_x}, {title_y}), 固定尺寸(550, 280) [宽度优化]")
                
                # 副标题固定位置
                subtitle_y = title_y + 280 + 20  # 280px标题区域 + 20px间距 = 580px
        
        # 生成副标题PNG（但先不贴入）
        if subtitle:
            print(f"生成副标题PNG（智能高度）")
            # 检测副标题语言
            subtitle_language = self._detect_language(subtitle)
            
            success, subtitle_img, actual_height = create_text_png(
                text=subtitle,
                width=550,  # 与标题保持一致，从600改为550
                height=50,  # 初始高度，会自动调整
                text_color=(255, 235, 156),  # 浅黄色 #FFEB9C
                language=subtitle_language,
                auto_height=True,
                line_height_px=30,  # 每行30px高度
                max_lines=3
            )
            
            if success:
                subtitle_img_data = (subtitle_img, text_x, subtitle_y, actual_height)
                print(f"副标题PNG已生成，等待最终贴入: 位置({text_x}, {subtitle_y}), 实际尺寸(550, {actual_height}) [宽度优化]")
        
        # 作者 - 调整位置：往右往上
        if author:
            if is_professional:
                # 往上调整：从820调整到800，往上20px
                author_y = 800  # 900 - 100(底边距) = 800，往上20px
            else:
                author_y = 640  # 往上20px
            
            # 将作者名改为全大写
            author_upper = author.upper()
            
            author_font = self._get_best_font(author_upper, author_size)
            self._draw_text_with_effects(
                draw, author_upper, (text_x, author_y), author_font,
                color="#CCCCCC",
                max_width=550 if is_professional else 450  # 与标题副标题保持一致
            )
            
            print(f"作者位置: ({text_x}, {author_y}) - 全大写: {author_upper} [右移5px, 上移20px]")
        
        # 三角形已经在right_img处理阶段贴入，这里不再需要单独处理
        print("三角形效果已集成到右侧图片中")
        
        # 最终步骤: 贴入标题和副标题PNG（在三角形之上）
        if title_img_data:
            title_img, tx, ty = title_img_data
            template.paste(title_img, (tx, ty), title_img)
            print(f"标题PNG最终贴入: 位置({tx}, {ty}) [最上层]")
        
        if subtitle_img_data:
            subtitle_img, sx, sy, sh = subtitle_img_data
            template.paste(subtitle_img, (sx, sy), subtitle_img)
            print(f"副标题PNG最终贴入: 位置({sx}, {sy}), 高度{sh} [最上层]")
        
        # 保存结果
        if template.mode == 'RGBA':
            # 转换为RGB保存为JPG，使用黑色背景
            rgb_image = Image.new('RGB', template.size, (0, 0, 0))
            rgb_image.paste(template, mask=template.split()[-1])
            rgb_image.save(output_path, 'JPEG', quality=95)
        else:
            template.save(output_path, 'JPEG', quality=95)
        
        print(f"最终缩略图生成完成: {output_path}")
        return output_path

# 如需测试，请运行 example_usage.py