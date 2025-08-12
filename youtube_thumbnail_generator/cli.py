#!/usr/bin/env python3
"""
CLI interface for YouTube Thumbnail Generator
"""

import argparse
import sys
import os
from .thumbnail_generator import ThumbnailGenerator
from .utils import detect_language, normalize_language_code

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate YouTube thumbnails with optional AI optimization'
    )
    
    # Required arguments
    parser.add_argument(
        'text',
        help='Text to display on the thumbnail'
    )
    
    # Output
    parser.add_argument(
        '-o', '--output',
        default='thumbnail.png',
        help='Output file path (default: thumbnail.png)'
    )
    
    # Background options
    parser.add_argument(
        '-bt', '--background-type',
        choices=['solid', 'gradient', 'pattern', 'image'],
        default='gradient',
        help='Background type (default: gradient)'
    )
    
    parser.add_argument(
        '--bg-color1',
        default='#667eea',
        help='Background color 1 (for solid/gradient)'
    )
    
    parser.add_argument(
        '--bg-color2',
        default='#764ba2',
        help='Background color 2 (for gradient/pattern)'
    )
    
    parser.add_argument(
        '--bg-direction',
        choices=['vertical', 'horizontal', 'diagonal'],
        default='diagonal',
        help='Gradient direction'
    )
    
    parser.add_argument(
        '--bg-image',
        help='Path to background image'
    )
    
    parser.add_argument(
        '--pattern',
        choices=['dots', 'lines', 'grid', 'waves'],
        default='dots',
        help='Pattern type'
    )
    
    # Font options
    parser.add_argument(
        '--font',
        help='Font name or path to font file'
    )
    
    parser.add_argument(
        '--font-size',
        type=int,
        default=72,
        help='Font size (default: 72)'
    )
    
    parser.add_argument(
        '--font-color',
        default='#FFFFFF',
        help='Font color (default: #FFFFFF)'
    )
    
    parser.add_argument(
        '--text-position',
        choices=['center', 'top', 'bottom'],
        default='center',
        help='Text position (default: center)'
    )
    
    # AI options
    parser.add_argument(
        '--enable-ai',
        action='store_true',
        help='Enable AI text optimization'
    )
    
    parser.add_argument(
        '--disable-ai',
        action='store_true',
        help='Disable AI text optimization'
    )
    
    parser.add_argument(
        '--api-key',
        help='Gemini API key for AI optimization'
    )
    
    parser.add_argument(
        '--source-language',
        choices=['en', 'zh', 'english', 'chinese', 'English', 'Chinese'],
        help='Specify input text language to skip auto-detection (en/zh/english/chinese)'
    )
    
    parser.add_argument(
        '--target-language',
        choices=['en', 'zh', 'english', 'chinese', 'English', 'Chinese'],
        help='Target language for translation (en/zh/english/chinese, only with AI optimization)'
    )
    
    parser.add_argument(
        '--ai-prompt',
        help='Custom AI optimization prompt'
    )
    
    # Other options
    parser.add_argument(
        '--quality',
        type=int,
        default=95,
        help='Output quality 1-100 (default: 95)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=1280,
        help='Thumbnail width (default: 1280)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=720,
        help='Thumbnail height (default: 720)'
    )
    
    parser.add_argument(
        '--batch',
        nargs='+',
        help='Generate multiple thumbnails with different texts'
    )
    
    parser.add_argument(
        '--detect-language',
        action='store_true',
        help='Only detect language and exit'
    )
    
    parser.add_argument(
        '--list-fonts',
        action='store_true',
        help='List available fonts and exit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='YouTube Thumbnail Generator 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle special actions
    if args.detect_language:
        lang = detect_language(args.text)
        print(f"Detected language: {lang} ({'English' if lang == 'en' else 'Chinese'})")
        return 0
    
    # Determine AI optimization setting
    enable_ai = None
    if args.enable_ai:
        enable_ai = True
    elif args.disable_ai:
        enable_ai = False
    
    # Initialize generator
    try:
        generator = ThumbnailGenerator(
            gemini_api_key=args.api_key or os.getenv('GEMINI_API_KEY'),
            enable_ai_optimization=enable_ai,
            default_language='auto',  # Always auto-detect by default
            width=args.width,
            height=args.height
        )
    except Exception as e:
        print(f"Error initializing generator: {e}", file=sys.stderr)
        return 1
    
    # Handle list fonts
    if args.list_fonts:
        fonts = generator.font_manager.list_available_fonts()
        print("Available fonts:")
        for font in fonts:
            print(f"  - {font}")
        return 0
    
    # Build background config
    background_config = {}
    
    if args.background_type == 'solid':
        background_config['color'] = args.bg_color1
    
    elif args.background_type == 'gradient':
        background_config['color1'] = args.bg_color1
        background_config['color2'] = args.bg_color2
        background_config['direction'] = args.bg_direction
    
    elif args.background_type == 'image':
        if not args.bg_image:
            print("Error: --bg-image required for image background", file=sys.stderr)
            return 1
        background_config['image_path'] = args.bg_image
    
    elif args.background_type == 'pattern':
        background_config['pattern'] = args.pattern
        background_config['color1'] = args.bg_color1
        background_config['color2'] = args.bg_color2
    
    # Handle batch generation
    if args.batch:
        texts = [args.text] + args.batch
        print(f"Generating {len(texts)} thumbnails...")
        
        try:
            output_dir = os.path.dirname(args.output) or '.'
            paths = generator.batch_generate(
                texts=texts,
                output_dir=output_dir,
                background_type=args.background_type,
                background_config=background_config,
                font_name=args.font,
                font_size=args.font_size,
                font_color=args.font_color,
                text_position=args.text_position,
                enable_ai_optimization=enable_ai,
                source_language=normalize_language_code(args.source_language) if args.source_language else None,
                target_language=normalize_language_code(args.target_language) if args.target_language else None,
                custom_prompt=args.ai_prompt,
                quality=args.quality
            )
            
            print(f"Successfully generated {len(paths)} thumbnails:")
            for path in paths:
                print(f"  - {path}")
        
        except Exception as e:
            print(f"Error generating thumbnails: {e}", file=sys.stderr)
            return 1
    
    else:
        # Single thumbnail generation
        print(f"Generating thumbnail...")
        
        try:
            output_path = generator.generate(
                text=args.text,
                output_path=args.output,
                background_type=args.background_type,
                background_config=background_config,
                font_name=args.font,
                font_size=args.font_size,
                font_color=args.font_color,
                text_position=args.text_position,
                enable_ai_optimization=enable_ai,
                source_language=normalize_language_code(args.source_language) if args.source_language else None,
                target_language=normalize_language_code(args.target_language) if args.target_language else None,
                custom_prompt=args.ai_prompt,
                quality=args.quality
            )
            
            print(f"Successfully generated: {output_path}")
        
        except Exception as e:
            print(f"Error generating thumbnail: {e}", file=sys.stderr)
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())