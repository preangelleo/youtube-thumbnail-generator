#!/usr/bin/env python3
"""
YouTube Thumbnail Generator - Example Usage

This script demonstrates all features of the YouTube Thumbnail Generator.
Copy this script and modify the parameters to suit your needs.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.thumbnail_generator import ThumbnailGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def example_basic():
    """Basic thumbnail generation without AI."""
    print("\n=== Basic Thumbnail Generation ===")
    
    generator = ThumbnailGenerator(
        enable_ai_optimization=False  # Explicitly disable AI
    )
    
    # Generate a simple thumbnail
    output_path = generator.generate(
        text="Python Tutorial 2024",
        output_path="output/basic_thumbnail.png",
        background_type="gradient",
        background_config={
            "color1": "#667eea",
            "color2": "#764ba2",
            "direction": "diagonal"
        },
        font_size=80,
        font_color="#FFFFFF",
        text_position="center"
    )
    
    print(f"✓ Basic thumbnail saved to: {output_path}")


def example_ai_optimization():
    """Thumbnail with AI text optimization."""
    print("\n=== AI-Optimized Thumbnail ===")
    
    # Check if API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  Skipping AI example: No GEMINI_API_KEY found in environment")
        print("   Get your API key from: https://ai.google.dev/")
        return
    
    generator = ThumbnailGenerator(
        gemini_api_key=api_key,
        enable_ai_optimization=True,  # Enable AI optimization
        default_language="en"
    )
    
    # Generate with AI optimization
    output_path = generator.generate(
        text="Learn Python programming basics",  # AI will optimize this
        output_path="output/ai_optimized_thumbnail.png",
        background_type="gradient",
        background_config={
            "color1": "#f093fb",
            "color2": "#f5576c",
            "direction": "horizontal"
        },
        font_size=75,
        font_color="#FFFFFF",
        text_position="center",
        enable_ai_optimization=True,  # Can override per-generation
        target_language="en"  # Force English optimization
    )
    
    print(f"✓ AI-optimized thumbnail saved to: {output_path}")


def example_chinese_text():
    """Thumbnail with Chinese text."""
    print("\n=== Chinese Text Thumbnail ===")
    
    generator = ThumbnailGenerator(
        enable_ai_optimization=False
    )
    
    output_path = generator.generate(
        text="Python编程教程",
        output_path="output/chinese_thumbnail.png",
        background_type="solid",
        background_config={
            "color": "#FF6B6B"
        },
        font_size=90,
        font_color="#FFFFFF",
        text_position="center"
    )
    
    print(f"✓ Chinese thumbnail saved to: {output_path}")


def example_image_background():
    """Thumbnail with image background."""
    print("\n=== Image Background Thumbnail ===")
    
    generator = ThumbnailGenerator()
    
    # First create a sample background image if it doesn't exist
    sample_bg_path = "output/sample_background.png"
    if not os.path.exists(sample_bg_path):
        # Create a sample gradient background
        temp_gen = ThumbnailGenerator()
        temp_gen.generate(
            text="",
            output_path=sample_bg_path,
            background_type="gradient",
            background_config={
                "color1": "#4facfe",
                "color2": "#00f2fe"
            }
        )
    
    # Use image as background
    output_path = generator.generate(
        text="Advanced Python Tips",
        output_path="output/image_bg_thumbnail.png",
        background_type="image",
        background_config={
            "image_path": sample_bg_path,
            "blur": 5,  # Apply blur to background
            "overlay_color": "#000000",  # Dark overlay
            "overlay_opacity": 0.4  # 40% opacity
        },
        font_size=85,
        font_color="#FFFFFF",
        text_position="center"
    )
    
    print(f"✓ Image background thumbnail saved to: {output_path}")


def example_pattern_background():
    """Thumbnail with pattern background."""
    print("\n=== Pattern Background Thumbnail ===")
    
    generator = ThumbnailGenerator()
    
    patterns = ["dots", "lines", "grid", "waves"]
    
    for pattern in patterns:
        output_path = generator.generate(
            text=f"{pattern.capitalize()} Pattern",
            output_path=f"output/pattern_{pattern}_thumbnail.png",
            background_type="pattern",
            background_config={
                "pattern": pattern,
                "color1": "#667eea",
                "color2": "#764ba2",
                "spacing": 40,
                "radius": 8 if pattern == "dots" else None,
                "line_width": 3 if pattern in ["lines", "grid"] else None,
                "amplitude": 30 if pattern == "waves" else None,
                "frequency": 0.02 if pattern == "waves" else None
            },
            font_size=70,
            font_color="#FFFFFF",
            text_position="center"
        )
        
        print(f"✓ {pattern.capitalize()} pattern thumbnail saved to: {output_path}")


def example_text_positions():
    """Thumbnails with different text positions."""
    print("\n=== Text Position Examples ===")
    
    generator = ThumbnailGenerator()
    
    positions = [
        ("center", "center"),
        ("top", "top"),
        ("bottom", "bottom"),
        ((100, 200), "custom_100_200")  # Custom position
    ]
    
    for position, name in positions:
        output_path = generator.generate(
            text=f"Text at {name}",
            output_path=f"output/position_{name}_thumbnail.png",
            background_type="gradient",
            background_config={
                "color1": "#a8edea",
                "color2": "#fed6e3",
                "direction": "vertical"
            },
            font_size=60,
            font_color="#333333",
            text_position=position
        )
        
        print(f"✓ {name.capitalize()} position thumbnail saved to: {output_path}")


def example_batch_generation():
    """Batch generation of multiple thumbnails."""
    print("\n=== Batch Generation ===")
    
    generator = ThumbnailGenerator()
    
    # List of video titles
    titles = [
        "Python Basics #1: Variables",
        "Python Basics #2: Functions",
        "Python Basics #3: Classes",
        "Python Basics #4: Modules",
        "Python Basics #5: Error Handling"
    ]
    
    # Generate thumbnails in batch
    output_paths = generator.batch_generate(
        texts=titles,
        output_dir="output/batch",
        background_type="gradient",
        background_config={
            "color1": "#FF416C",
            "color2": "#FF4B2B",
            "direction": "diagonal"
        },
        font_size=65,
        font_color="#FFFFFF",
        text_position="center"
    )
    
    print(f"✓ Generated {len(output_paths)} thumbnails in batch")
    for path in output_paths:
        print(f"  - {path}")


def example_custom_configuration():
    """Full example with all customizable parameters."""
    print("\n=== Fully Customized Thumbnail ===")
    
    # Initialize with all parameters
    generator = ThumbnailGenerator(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),  # Optional API key
        enable_ai_optimization=True if os.getenv("GEMINI_API_KEY") else False,
        default_language="auto",  # Auto-detect language
        width=1280,  # HD width
        height=720   # HD height
    )
    
    # Generate with all parameters specified
    output_path = generator.generate(
        text="Ultimate Python Masterclass 2024 🚀",
        output_path="output/custom_full_thumbnail.png",
        
        # Background configuration
        background_type="gradient",  # Options: solid, gradient, image, pattern
        background_config={
            "color1": "#8E2DE2",  # Start color
            "color2": "#4A00E0",  # End color
            "direction": "diagonal"  # Options: vertical, horizontal, diagonal
        },
        
        # Font configuration
        font_name=None,  # Use default font (or specify: "arial", "helvetica", etc.)
        font_size=85,  # Font size in pixels
        font_color="#FFFFFF",  # White text
        
        # Text positioning
        text_position="center",  # Options: center, top, bottom, or (x, y) tuple
        
        # AI optimization settings
        enable_ai_optimization=True if os.getenv("GEMINI_API_KEY") else False,
        target_language="en",  # Options: en, zh, auto
        custom_prompt=None,  # Optional custom AI prompt
        
        # Output settings
        quality=95  # Image quality (1-100)
    )
    
    print(f"✓ Fully customized thumbnail saved to: {output_path}")


def main():
    """Run all examples."""
    print("\n" + "="*50)
    print("YouTube Thumbnail Generator - Examples")
    print("="*50)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/batch", exist_ok=True)
    
    # Run examples
    try:
        example_basic()
        example_ai_optimization()
        example_chinese_text()
        example_image_background()
        example_pattern_background()
        example_text_positions()
        example_batch_generation()
        example_custom_configuration()
        
        print("\n" + "="*50)
        print("✓ All examples completed successfully!")
        print("Check the 'output' directory for generated thumbnails.")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()