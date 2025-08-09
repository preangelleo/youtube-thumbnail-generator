#!/usr/bin/env python3
"""
YouTube Thumbnail Generator - Interactive Test
只供用户使用的简单测试工具
"""

import os
from final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path

def test_youtube_thumbnails():
    """交互式测试工具"""
    
    # 确保输出目录存在
    output_dir = "Outputs/interactive_test"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("🎨 YouTube Thumbnail Generator - Interactive Test")
    print("="*60)
    
    # 获取用户输入的标题
    while True:
        title = input("\n请输入要测试的标题: ").strip()
        if title:
            break
        print("❌ 请输入有效标题")
    
    # 询问是否启用AI优化
    while True:
        enable_ai = input("\n启用AI标题优化? (y/n): ").strip().lower()
        if enable_ai in ['y', 'yes', 'n', 'no']:
            break
        print("❌ 请输入 y 或 n")
    
    # 如果启用AI，获取API key
    api_key = None
    if enable_ai in ['y', 'yes']:
        api_key = input("\n请输入你的Google API Key: ").strip()
        if not api_key:
            print("❌ 未提供API Key，将使用fallback模式")
    
    print(f"\n{'='*60}")
    print("🚀 开始生成缩略图...")
    print(f"{'='*60}")
    
    # 创建生成器
    try:
        if enable_ai in ['y', 'yes'] and api_key:
            generator = FinalThumbnailGenerator(
                template_path=get_resource_path("templates/professional_template.jpg"),
                google_api_key=api_key
            )
        else:
            generator = FinalThumbnailGenerator(
                template_path=get_resource_path("templates/professional_template.jpg")
            )
        
        # 生成缩略图
        output_path = f"{output_dir}/test_result.jpg"
        result = generator.generate_final_thumbnail(
            title=title,
            author="测试作者",
            theme="dark",
            output_path=output_path
        )
        
        if result == output_path:
            print(f"\n✅ 成功!")
            print(f"📁 缩略图已保存到: {output_path}")
            print(f"💡 请查看文件验证效果")
        else:
            print(f"\n❌ 失败: {result}")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    print(f"\n🎯 测试完成!")

if __name__ == "__main__":
    try:
        test_youtube_thumbnails()
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        print("请确保在正确的目录运行此脚本")