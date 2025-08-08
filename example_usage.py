#!/usr/bin/env python3
"""
YouTube缩略图生成器 - 示例用法
=====================================

这个示例展示了如何使用YouTube缩略图生成器创建专业的中英文缩略图。

功能特性：
- 支持中英文智能换行和字体优化
- 中文标题：超过9字自动换行，字体增大30%
- 中文副标题：超过20字自动换行，字体增大30%，高度增加20%
- 英文标题：最多3行，自动截断
- 三角形过渡效果集成到右侧图片
- 550px文字区域，完美适配700px左侧区域

使用方法：
1. 确保所需文件存在：
   - 模板: templates/professional_template.jpg
   - Logo: logos/your_logo.png  
   - 图片: assets/your_image.jpg

2. 运行此脚本：
   python example_usage.py

3. 查看生成结果：
   outputs/example_output.jpg
"""

from final_thumbnail_generator import FinalThumbnailGenerator
import os

def main():
    """主函数 - 演示缩略图生成的完整流程"""
    
    print("=" * 60)
    print("YouTube缩略图生成器 - 示例用法")
    print("=" * 60)
    
    # 初始化生成器
    try:
        generator = FinalThumbnailGenerator("templates/professional_template.jpg")
        print("✅ 生成器初始化成功")
    except FileNotFoundError as e:
        print(f"❌ 模板文件不存在: {e}")
        return
    
    # 示例1: 中文缩略图（展示智能换行功能）
    print("\n📝 生成中文示例缩略图...")
    print("标题: 终极人工智能技术革命完整指南 (14字 -> 自动换行)")
    print("副标题: 所有你需要知道的现代科技 (10字 -> 单行显示)")
    
    result1 = generator.generate_final_thumbnail(
        title="终极人工智能技术革命完整指南",        # 14字，触发9字换行规则
        subtitle="所有你需要知道的现代科技",         # 10字，不超过20字限制
        author="Leo Wang",
        logo_path="logos/animagent_logo.png",
        right_image_path="assets/testing_image.jpeg",
        output_path="outputs/chinese_example.jpg"
    )
    
    if os.path.exists(result1):
        print(f"✅ 中文示例生成成功: {result1}")
    else:
        print(f"❌ 中文示例生成失败: {result1}")
    
    # 示例2: 英文缩略图（展示3行截断功能）  
    print("\n📝 生成英文示例缩略图...")
    print("标题: The Ultimate Complete Guide... (长标题 -> 3行截断)")
    print("副标题: Everything You Need to Know (适中长度)")
    
    result2 = generator.generate_final_thumbnail(
        title="The Ultimate Complete Guide to Advanced AI Technology Revolution and Future Gaming Setup Reviews 2025",
        subtitle="Everything You Need to Know About Modern Technology and Future Developments",  
        author="Leo Wang",
        logo_path="logos/animagent_logo.png",
        right_image_path="assets/testing_image.jpeg", 
        output_path="outputs/english_example.jpg"
    )
    
    if os.path.exists(result2):
        print(f"✅ 英文示例生成成功: {result2}")
    else:
        print(f"❌ 英文示例生成失败: {result2}")
    
    # 示例3: 无副标题缩略图（展示标题居中功能）
    print("\n📝 生成无副标题示例...")
    print("标题: Amazing Tech Reviews (无副标题 -> 标题下移50px居中)")
    print("副标题: None (自动跳过)")
    
    result3 = generator.generate_final_thumbnail(
        title="Amazing Tech Reviews and Future Innovations",
        subtitle=None,  # 无副标题
        author="Leo Wang",
        logo_path="logos/animagent_logo.png",
        right_image_path="assets/testing_image.jpeg",
        output_path="outputs/no_subtitle_example.jpg"
    )
    
    if os.path.exists(result3):
        print(f"✅ 无副标题示例生成成功: {result3}")
    else:
        print(f"❌ 无副标题示例生成失败: {result3}")
    
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)
    print("\n📋 技术规格说明:")
    print("• 画布尺寸: 1600x900 (专业模板)")
    print("• 文字区域: 700x900 (左侧)")
    print("• 图片区域: 900x900 (右侧)")
    print("• 文字宽度: 550px (安全边界)")
    print("• 中文字体: PingFang/方正黑体系列")
    print("• 英文字体: Lexend Bold")
    print("• 三角形过渡: 200x900 集成到右侧图片")
    
    print("\n🔧 智能换行规则:")
    print("• 中文标题: >9字换行，除以2分配，奇数字符放第二行")
    print("• 中文副标题: >20字换行，除以2分配")  
    print("• 英文标题: 空格换行，最多3行，超过截断+省略号")
    print("• 英文副标题: 空格换行，最多3行")
    
    print("\n🎨 中文优化:")
    print("• 字体大小: 比英文大30%")
    print("• 副标题高度: 比英文高20%")
    print("• 行间距: 标题16px，副标题8px")
    
    print("\n📍 布局智能调整:")
    print("• 有副标题: 标题位置 (55, 280)")
    print("• 无副标题: 标题位置 (55, 330) - 下移50px居中")
    print("• 副标题可为 None 或空字符串")
    print("• 文字区域: 550px宽度，安全边界内")

def create_test_assets():
    """创建测试所需的资源文件（如果不存在）"""
    print("\n🔍 检查必需文件...")
    
    required_files = [
        "templates/professional_template.jpg",
        "logos/animagent_logo.png", 
        "assets/testing_image.jpeg"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n请确保这些文件存在后再运行示例。")
        return False
    
    print("✅ 所有必需文件都存在")
    return True

if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)
    
    # 检查文件
    if create_test_assets():
        # 运行示例
        main()
    else:
        print("\n💡 提示: 请参考README.md了解如何准备必需的资源文件。")