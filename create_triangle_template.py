#!/usr/bin/env python3
"""
创建三角形PNG模板
宽200px, 高900px, 从右上角到左下角的对角线
左上三角形: 黑色
右下三角形: 透明
"""

from PIL import Image, ImageDraw

def create_triangle_template(width=200, height=900, output_path="templates/triangle_template.png"):
    """
    创建三角形模板
    
    Args:
        width (int): 图片宽度
        height (int): 图片高度  
        output_path (str): 输出路径
    """
    # 创建透明背景的RGBA图片
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 定义三角形顶点：左上三角形
    # 从右上角(width, 0)到左下角(0, height)的对角线
    # 左上三角形的三个顶点：(0,0), (width,0), (0,height)
    triangle_points = [
        (0, 0),          # 左上角
        (width, 0),      # 右上角  
        (0, height)      # 左下角
    ]
    
    # 绘制黑色三角形
    draw.polygon(triangle_points, fill=(0, 0, 0, 255))  # 黑色不透明
    
    print(f"创建三角形模板:")
    print(f"  尺寸: {width}x{height}")
    print(f"  对角线: 右上角({width},0) -> 左下角(0,{height})")
    print(f"  左上三角形: 黑色")
    print(f"  右下三角形: 透明")
    print(f"  保存路径: {output_path}")
    
    # 保存为PNG格式保持透明度
    img.save(output_path, 'PNG')
    return output_path

if __name__ == "__main__":
    import os
    
    # 确保templates目录存在
    os.makedirs("templates", exist_ok=True)
    
    # 创建三角形模板
    result = create_triangle_template()
    print(f"✅ 三角形模板创建完成: {result}")