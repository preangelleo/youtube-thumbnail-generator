#!/usr/bin/env python3
"""
YouTube Thumbnail Generator - Enhanced Interactive Test
升级版交互测试工具，支持三种测试模式
"""

import os
from final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path

def get_all_combinations():
    """Define all 12 possible template combinations"""
    return [
        # With Triangle - 8 combinations
        {"id": 1, "theme": "dark", "enable_triangle": True, "triangle_direction": "top", "flip": False, 
         "desc": "Dark + Triangle ON (top ▲) + Standard"},
        {"id": 2, "theme": "dark", "enable_triangle": True, "triangle_direction": "top", "flip": True,
         "desc": "Dark + Triangle ON (top ▲) + Flip"},
        {"id": 3, "theme": "dark", "enable_triangle": True, "triangle_direction": "bottom", "flip": False,
         "desc": "Dark + Triangle ON (bottom ▼) + Standard"},
        {"id": 4, "theme": "dark", "enable_triangle": True, "triangle_direction": "bottom", "flip": True,
         "desc": "Dark + Triangle ON (bottom ▼) + Flip"},
        {"id": 5, "theme": "light", "enable_triangle": True, "triangle_direction": "top", "flip": False,
         "desc": "Light + Triangle ON (top ▲) + Standard"},
        {"id": 6, "theme": "light", "enable_triangle": True, "triangle_direction": "top", "flip": True,
         "desc": "Light + Triangle ON (top ▲) + Flip"},
        {"id": 7, "theme": "light", "enable_triangle": True, "triangle_direction": "bottom", "flip": False,
         "desc": "Light + Triangle ON (bottom ▼) + Standard"},
        {"id": 8, "theme": "light", "enable_triangle": True, "triangle_direction": "bottom", "flip": True,
         "desc": "Light + Triangle ON (bottom ▼) + Flip"},
        # Without Triangle - 4 combinations
        {"id": 9, "theme": "dark", "enable_triangle": False, "triangle_direction": "bottom", "flip": False,
         "desc": "Dark + Triangle OFF + Standard"},
        {"id": 10, "theme": "dark", "enable_triangle": False, "triangle_direction": "bottom", "flip": True,
         "desc": "Dark + Triangle OFF + Flip"},
        {"id": 11, "theme": "light", "enable_triangle": False, "triangle_direction": "bottom", "flip": False,
         "desc": "Light + Triangle OFF + Standard"},
        {"id": 12, "theme": "light", "enable_triangle": False, "triangle_direction": "bottom", "flip": True,
         "desc": "Light + Triangle OFF + Flip"}
    ]

def get_user_inputs():
    """Get common user inputs"""
    print("🎨 YouTube Thumbnail Generator - Enhanced Interactive Test")
    print("="*70)
    
    # Get title
    while True:
        title = input("\n请输入测试标题 (Enter your title): ").strip()
        if title:
            break
        print("❌ 请输入有效标题")
    
    # Get author name
    print(f"\n👤 作者信息设置")
    author = input("请输入作者名称 (按回车使用默认 'leowang.net'): ").strip()
    if not author:
        author = "leowang.net"
        print(f"✅ 使用默认作者: {author}")
    else:
        print(f"✅ 使用自定义作者: {author}")
    
    # Get logo path
    print(f"\n🏷️ Logo设置")
    logo_path = input("请输入Logo文件路径 (按回车使用默认logo): ").strip()
    if not logo_path:
        logo_path = None
        print("✅ 使用默认Logo")
    else:
        if os.path.exists(logo_path):
            print(f"✅ 使用自定义Logo: {logo_path}")
        else:
            print(f"❌ 文件不存在，将使用默认Logo: {logo_path}")
            logo_path = None
    
    # Get right image path  
    print(f"\n🖼️ 右侧图片设置")
    right_image_path = input("请输入右侧图片路径 (按回车使用默认图片): ").strip()
    if not right_image_path:
        right_image_path = None
        print("✅ 使用默认右侧图片")
    else:
        if os.path.exists(right_image_path):
            print(f"✅ 使用自定义图片: {right_image_path}")
        else:
            print(f"❌ 文件不存在，将使用默认图片: {right_image_path}")
            right_image_path = None
    
    # AI optimization settings
    print("\n🤖 AI Title Optimization Settings")
    enable_ai = input("启用AI标题优化? Enable AI optimization? (y/回车默认n): ").strip().lower()
    if not enable_ai:  # 回车默认为No
        enable_ai = 'n'
        print("✅ 使用默认设置: 不启用AI优化")
    elif enable_ai not in ['y', 'yes', 'n', 'no']:
        enable_ai = 'n'  # 无效输入默认为No
        print("✅ 无效输入，使用默认设置: 不启用AI优化")
    
    api_key = None
    if enable_ai in ['y', 'yes']:
        api_key = input("请输入Google API Key (或按回车跳过): ").strip()
        if not api_key:
            print("❌ 未提供API Key，将使用fallback模式")
    
    return title, author, logo_path, right_image_path, api_key

def comprehensive_test(title, author, logo_path, right_image_path, api_key):
    """Test all 12 combinations"""
    print(f"\n🔬 全面测试模式 - 生成所有12种组合")
    print("="*70)
    
    output_dir = "Outputs/comprehensive_test"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generator = FinalThumbnailGenerator(
        template_path=get_resource_path("templates/professional_template.jpg"),
        google_api_key=api_key
    )
    
    combinations = get_all_combinations()
    success_count = 0
    
    for combo in combinations:
        print(f"\n[{combo['id']}/12] 测试组合: {combo['desc']}")
        
        try:
            output_path = f"{output_dir}/combo_{combo['id']:02d}_{combo['theme']}{'_tri_' + combo['triangle_direction'] if combo['enable_triangle'] else '_no_tri'}{'_flip' if combo['flip'] else '_std'}.jpg"
            
            result = generator.generate_final_thumbnail(
                title=title,
                author=author,
                logo_path=logo_path,
                right_image_path=right_image_path,
                output_path=output_path,
                theme=combo["theme"],
                enable_triangle=combo["enable_triangle"],
                triangle_direction=combo["triangle_direction"],
                flip=combo["flip"]
            )
            
            if result == output_path:
                print(f"✅ 成功: {os.path.basename(output_path)}")
                success_count += 1
            else:
                print(f"❌ 失败: {result}")
        
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    print(f"\n🎯 全面测试完成!")
    print(f"   成功生成: {success_count}/12 种组合")
    print(f"   输出目录: {output_dir}")

def random_test(title, author, logo_path, right_image_path, api_key):
    """Test with random combination"""
    print(f"\n🎲 随机测试模式 - 随机选择1种组合")
    print("="*70)
    
    from final_thumbnail_generator import generate_random_thumbnail
    
    output_dir = "Outputs/random_test"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        output_path = f"{output_dir}/random_result.jpg"
        
        result = generate_random_thumbnail(
            title=title,
            author=author,
            logo_path=logo_path,
            right_image_path=right_image_path,
            output_path=output_path,
            google_api_key=api_key
        )
        
        if result == output_path:
            print(f"✅ 成功生成随机缩略图: {os.path.basename(output_path)}")
            print(f"📁 输出目录: {output_dir}")
        else:
            print(f"❌ 失败: {result}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")

def manual_selection_test(title, author, logo_path, right_image_path, api_key):
    """Test with manually selected combination"""
    print(f"\n🎯 选择模式测试 - 手动选择1种组合")
    print("="*70)
    
    combinations = get_all_combinations()
    
    # Display all combinations
    print("可选的12种组合:")
    for combo in combinations:
        print(f"  {combo['id']:2d}. {combo['desc']}")
    
    # Get user selection
    choice_input = input(f"\n请选择组合 (1-12, 回车默认1): ").strip()
    if not choice_input:  # 回车默认选择第一个组合
        choice = 1
        selected_combo = combinations[0]
        print("✅ 使用默认组合: 1 (Dark + Triangle ON (top ▲) + Standard)")
    else:
        try:
            choice = int(choice_input)
            if 1 <= choice <= 12:
                selected_combo = combinations[choice - 1]
            else:
                choice = 1  # 无效输入默认选择第一个
                selected_combo = combinations[0]
                print("✅ 无效输入，使用默认组合: 1 (Dark + Triangle ON (top ▲) + Standard)")
        except ValueError:
            choice = 1  # 非数字输入默认选择第一个
            selected_combo = combinations[0]
            print("✅ 无效输入，使用默认组合: 1 (Dark + Triangle ON (top ▲) + Standard)")
    
    print(f"\n选择的组合: {selected_combo['desc']}")
    
    # Generate thumbnail
    output_dir = "Outputs/manual_selection"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generator = FinalThumbnailGenerator(
        template_path=get_resource_path("templates/professional_template.jpg"),
        google_api_key=api_key
    )
    
    try:
        output_path = f"{output_dir}/manual_combo_{selected_combo['id']:02d}.jpg"
        
        result = generator.generate_final_thumbnail(
            title=title,
            author=author,
            logo_path=logo_path,
            right_image_path=right_image_path,
            output_path=output_path,
            theme=selected_combo["theme"],
            enable_triangle=selected_combo["enable_triangle"], 
            triangle_direction=selected_combo["triangle_direction"],
            flip=selected_combo["flip"]
        )
        
        if result == output_path:
            print(f"✅ 成功生成缩略图: {os.path.basename(output_path)}")
            print(f"📁 输出目录: {output_dir}")
        else:
            print(f"❌ 失败: {result}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")

def main():
    """Main test function"""
    try:
        # Get common inputs
        title, author, logo_path, right_image_path, api_key = get_user_inputs()
        
        # Test mode selection
        print(f"\n📋 选择测试模式:")
        print("  1. 全面测试 (生成所有12种组合)")
        print("  2. 随机测试 (随机选择1种组合)")  
        print("  3. 选择模式 (手动选择1种组合)")
        
        test_mode_input = input("请选择测试模式 (1-3, 回车默认3): ").strip()
        if not test_mode_input:  # 回车默认选择模式3
            test_mode = 3
            print("✅ 使用默认测试模式: 3 (选择模式)")
        else:
            try:
                test_mode = int(test_mode_input)
                if test_mode not in [1, 2, 3]:
                    test_mode = 3  # 无效输入默认为3
                    print("✅ 无效输入，使用默认测试模式: 3 (选择模式)")
            except ValueError:
                test_mode = 3  # 非数字输入默认为3
                print("✅ 无效输入，使用默认测试模式: 3 (选择模式)")
        
        # Execute selected test mode
        if test_mode == 1:
            comprehensive_test(title, author, logo_path, right_image_path, api_key)
        elif test_mode == 2:
            random_test(title, author, logo_path, right_image_path, api_key)
        elif test_mode == 3:
            manual_selection_test(title, author, logo_path, right_image_path, api_key)
        
        print(f"\n🎉 测试完成!")
    
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        print("请确保在正确的目录运行此脚本")

if __name__ == "__main__":
    main()