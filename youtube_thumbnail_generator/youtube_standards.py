#!/usr/bin/env python3
"""
Thumbnail Output Optimization Module
Focus on size compression and encoding optimization to improve transmission efficiency and platform compatibility
"""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple, Optional

class ThumbnailOptimizer:
    """Thumbnail output optimizer"""
    
    # Preset output options
    OUTPUT_PRESETS = {
        'youtube_hd': {
            'size': (1280, 720),    # YouTube recommended minimum size
            'quality': 85,
            'description': 'YouTube HD (1280x720)'
        },
        'youtube_full': {
            'size': (1600, 900),    # YouTube recommended full size
            'quality': 80,
            'description': 'YouTube Full (1600x900)'
        },
        'blog_feature': {
            'size': (1200, 675),    # Blog feature image
            'quality': 75,
            'description': 'Blog Feature (1200x675)'
        },
        'social_share': {
            'size': (1080, 608),    # Social media sharing
            'quality': 80,
            'description': 'Social Media (1080x608)'
        }
    }
    
    def __init__(self):
        """Initialize output optimizer"""
        pass
    
    def optimize_for_preset(self, image: Image.Image, preset: str) -> Image.Image:
        """
        Optimize image size according to preset
        
        Args:
            image: PIL image object (assumes input is 1600x900)
            preset: Preset name
            
        Returns:
            Image.Image: Optimized image
        """
        if preset not in self.OUTPUT_PRESETS:
            raise ValueError(f"Unknown preset: {preset}, available presets: {list(self.OUTPUT_PRESETS.keys())}")
        
        preset_config = self.OUTPUT_PRESETS[preset]
        target_size = preset_config['size']
        
        current_size = image.size
        print(f"📐 尺寸优化: {current_size[0]}x{current_size[1]} -> {target_size[0]}x{target_size[1]}")
        print(f"🎯 预设: {preset_config['description']}")
        
        # 如果目标尺寸与当前相同，直接返回
        if current_size == target_size:
            print("✅ 尺寸已匹配，无需调整")
            return image
        
        # 执行高质量缩放
        optimized_image = image.resize(target_size, Image.Resampling.LANCZOS)
        print(f"✅ 尺寸优化完成")
        
        return optimized_image
    
    def optimize_thumbnail(self, input_path: str, output_path: str = None, 
                          preset: str = 'youtube_hd') -> Tuple[bool, str]:
        """
        优化缩略图：尺寸压缩和编码优化
        
        Args:
            input_path: 输入图片路径（假设是1600x900）
            output_path: 输出路径，如果为None则自动生成
            preset: 输出预设 ('youtube_hd', 'youtube_full', 'blog_feature', 'social_share')
            
        Returns:
            tuple: (成功标志, 输出路径或错误信息)
        """
        try:
            if not os.path.exists(input_path):
                return False, f"输入文件不存在: {input_path}"
            
            # 验证预设
            if preset not in self.OUTPUT_PRESETS:
                return False, f"未知预设: {preset}，可用: {list(self.OUTPUT_PRESETS.keys())}"
            
            preset_config = self.OUTPUT_PRESETS[preset]
            
            # 打开图片
            with Image.open(input_path) as image:
                original_width, original_height = image.size
                print(f"🎯 缩略图输出优化")
                print(f"📁 输入: {input_path} ({original_width}x{original_height})")
                
                # 执行尺寸优化
                optimized_image = self.optimize_for_preset(image, preset)
                
                # 生成输出路径
                if not output_path:
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    output_dir = os.path.dirname(input_path)
                    output_path = os.path.join(output_dir, f"{base_name}_{preset}.jpg")
                
                # 保存优化图片
                quality = preset_config['quality']
                optimized_image.save(
                    output_path, 
                    'JPEG', 
                    quality=quality, 
                    optimize=True, 
                    progressive=True
                )
                
                # 检查结果
                final_size = os.path.getsize(output_path)
                final_width, final_height = optimized_image.size
                print(f"✅ 输出优化完成!")
                print(f"📁 输出: {output_path}")
                print(f"📊 最终尺寸: {final_width}x{final_height}")
                print(f"🎯 质量设置: {quality}%")
                print(f"💾 文件大小: {final_size:,} bytes")
                
                return True, output_path
                
        except Exception as e:
            error_msg = f"缩略图优化失败: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg

def optimize_thumbnail_output(input_path: str, output_path: str = None, 
                             preset: str = 'youtube_hd') -> Tuple[bool, str]:
    """
    便捷函数：优化缩略图输出
    
    Args:
        input_path: 输入图片路径（1600x900）
        output_path: 输出路径
        preset: 输出预设 ('youtube_hd', 'blog_feature', etc.)
        
    Returns:
        tuple: (成功标志, 输出路径或错误信息)
    """
    optimizer = ThumbnailOptimizer()
    return optimizer.optimize_thumbnail(input_path, output_path, preset)

# 保持向后兼容的函数名
def standardize_thumbnail_for_youtube(input_path: str, output_path: str = None, 
                                    preset: str = 'youtube_hd') -> Tuple[bool, str]:
    """向后兼容的函数名，实际调用新的优化函数"""
    return optimize_thumbnail_output(input_path, output_path, preset)