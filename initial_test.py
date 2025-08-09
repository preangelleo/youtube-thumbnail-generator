#!/usr/bin/env python3
"""
Interactive YouTube Thumbnail Generator Test
Tests all themes and configurations with user-provided title
"""

import os
import sys
from final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path, create_default_templates

def get_default_template():
    """Get path to the default professional template"""
    return get_resource_path("templates/professional_template.jpg")

def test_youtube_thumbnails():
    """Interactive test for all thumbnail templates and configurations."""
    
    # Create output directory if it doesn't exist
    output_dir = "Outputs/interactive_test"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Initialize generator with default template
    generator = FinalThumbnailGenerator(get_default_template())
    
    # Get user input
    print("\n" + "="*60)
    print("🎨 YouTube Thumbnail Generator - Interactive Test")
    print("="*60)
    
    # Get title from user
    title = input("\n请输入要测试的标题 (Enter title to test): ").strip()
    if not title:
        title = "测试标题 Test Title"
        print(f"使用默认标题: {title}")
    
    # Common parameters
    author = "leowang.net"
    logo_path = None  # Use system default logo
    right_image_path = None  # Use system default image
    
    # Custom template path for custom theme
    custom_template_path = "/Users/lgg/coding/sumatman/Temps/web_1754109069175_1aptvbwpn/images/scene_007_chinese.png"
    
    # Test configurations
    test_configs = []
    
    # For dark and light themes: 2 flip states × 2 triangle directions = 4 variations each
    for theme in ["dark", "light"]:
        for flip in [False, True]:
            for triangle_dir in ["bottom", "top"]:
                test_configs.append({
                    "theme": theme,
                    "flip": flip,
                    "triangle_direction": triangle_dir,
                    "desc": f"{theme}_{['std','flip'][flip]}_{triangle_dir}"
                })
    
    # For custom theme: 2 flip states only (no triangle)
    for flip in [False, True]:
        test_configs.append({
            "theme": "custom",
            "flip": flip,
            "triangle_direction": None,
            "desc": f"custom_{['std','flip'][flip]}"
        })
    
    print(f"\n测试配置 (Test configurations):")
    print(f"- Dark theme: 4 variations (2 flip × 2 triangle)")
    print(f"- Light theme: 4 variations (2 flip × 2 triangle)")  
    print(f"- Custom theme: 2 variations (2 flip only)")
    print(f"Total: 10 configurations")
    print(f"\n使用标题: '{title}'")
    
    generated_files = []
    
    # Test all configurations
    for i, config in enumerate(test_configs, 1):
        theme = config["theme"]
        flip = config["flip"]
        triangle_dir = config["triangle_direction"]
        desc = config["desc"]
        
        # Generate output filename
        output_path = f"{output_dir}/test_{desc}.jpg"
        
        print(f"\n[{i}/10] 生成: {desc}")
        print(f"  Theme: {theme}")
        print(f"  Flip: {'Yes' if flip else 'No'}")
        print(f"  Triangle: {triangle_dir if triangle_dir else 'N/A'}")
        
        try:
            # Generate thumbnail based on theme
            if theme == "custom":
                result = generator.generate_final_thumbnail(
                    title=title,
                    logo_path=logo_path,
                    right_image_path=right_image_path,
                    output_path=output_path,
                    theme=theme,
                    custom_template=custom_template_path,
                    flip=flip,
                    youtube_ready=True
                )
            else:
                result = generator.generate_final_thumbnail(
                    title=title,
                    author=author,
                    logo_path=logo_path,
                    right_image_path=right_image_path,
                    output_path=output_path,
                    theme=theme,
                    triangle_direction=triangle_dir,
                    flip=flip,
                    youtube_ready=True
                )
            
            if result:
                file_size = os.path.getsize(output_path) / 1024  # KB
                print(f"  ✅ 成功: {output_path} ({file_size:.1f} KB)")
                generated_files.append(output_path)
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎉 测试完成 (Test completed)!")
    print(f"{'='*60}")
    print(f"\n生成文件: {len(generated_files)}/10")
    print(f"输出目录: {output_dir}")
    
    print("\n文件列表:")
    for file in generated_files:
        print(f"  - {os.path.basename(file)}")
    
    print("\n文件说明:")
    print("  - std = 标准布局 (standard layout)")
    print("  - flip = 镜像布局 (mirrored layout)")
    print("  - bottom = 倒梯形 (triangle pointing down)")
    print("  - top = 正梯形 (triangle pointing up)")

if __name__ == "__main__":
    test_youtube_thumbnails()