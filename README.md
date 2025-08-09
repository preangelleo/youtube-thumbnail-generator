# YouTube Thumbnail Generator v2.4.3

Professional YouTube thumbnail generator with enhanced Chinese font bold rendering, AI-powered title optimization, and intelligent text layout system.

**Author**: Leo Wang (https://leowang.net)

[![PyPI version](https://badge.fury.io/py/youtube-thumbnail-generator.svg)](https://badge.fury.io/py/youtube-thumbnail-generator)
📦 [![Downloads](https://img.shields.io/pypi/dm/youtube-thumbnail-generator)](https://pypi.org/project/youtube-thumbnail-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🌍 Available on PyPI**: https://pypi.org/project/youtube-thumbnail-generator/  
**📂 GitHub Repository**: https://github.com/preangelleo/youtube-thumbnail-generator

## 📋 Core Features

- ✅ **Intelligent Chinese/English System**: PNG overlay technology, perfect Chinese/English text mixing
- ✅ **Smart Line-breaking Algorithm**: Chinese 9 character limits, English 3-line truncation  
- ✅ **Enhanced Chinese Font Bold**: STHeiti Medium priority + intelligent stroke effects for perfect bold rendering
- ✅ **Professional Visual Effects**: Triangle transition integrated into images, text always on top layer
- ✅ **Intelligent Image Processing**: Auto square conversion + 900x900 filling
- ✅ **Multi-endpoint API Support**: Flask RESTful API + Chapter functionality
- ✅ **Smart Font Selection**: Chinese PingFang/Founder, English Lexend Bold
- ✅ **Three Theme Modes**: Dark (black bg), Light (white bg), Custom (user template)
- ✅ **Full Color Customization**: Title color, author color, triangle toggle - all parameterized
- ✅ **Dynamic Font Scaling**: Auto font size adjustment based on text length (1-17 characters)
- ✅ **YouTube API Ready**: Built-in optimization for YouTube API v3 thumbnail upload compliance
- 🆕 **AI Title Optimization**: Google Gemini-powered mixed-language title optimization (optional)
- 🎲 **Random Template Generation**: One-click thumbnail creation with 12 random template combinations
- 🎮 **Enhanced Interactive Testing**: One-click default experience (enter-to-continue) with 3 testing modes

## 🎨 Three Theme Modes

**Canvas Size**: 1600x900 pixels

### 🎨 Template Examples with Enhanced Stroke Effects (v2.4.2)

#### Professional Dark Theme Sample
**Perfect for**: Tech content, gaming, serious topics  
**Features**: Enhanced Chinese bold rendering with intelligent stroke effects

![Professional Dark Theme Example](template_samples/v2.4.2_examples/combo_01_professional_dark_triangle_False_english.jpg)

#### 📖 **[View All Examples Gallery →](EXAMPLES.md)**

**More Examples Available:**
- **12 Template Combinations**: Professional, Standard, Triangle themes × Dark/Light × With/Without triangle overlays
- **Mixed Language Support**: Chinese and English title examples 
- **Enhanced Stroke Effects**: Perfect bold rendering for both dark and light backgrounds
- **API Generation Examples**: All samples generated using the latest API with stroke improvements

**[🎨 Complete Examples Gallery →](EXAMPLES.md)** - View all template combinations with enhanced stroke effects

## 💡 Optimal Length Recommendations

### 🎯 Best Results Guidelines
For the most professional and visually appealing thumbnails:

#### ⚠️ **IMPORTANT: Single Language Only**
**Our system is optimized for single-language titles. Mixed languages may cause formatting issues.**

🚫 **Avoid Mixed Languages**:
- ❌ "AI技术指南 Complete Guide" - English words may be improperly split in Chinese mode
- ❌ "Complete AI 技术指南" - Chinese characters may break English word spacing
- ❌ "学习 Python Programming" - Mixed mode causes unpredictable line breaks

✅ **Use Single Languages**:
- ✅ "AI技术指南完整教程" - Pure Chinese
- ✅ "Complete AI Technology Guide" - Pure English

#### 🇨🇳 Chinese Titles
**Optimal Length: 10-12 characters**
- **10 characters**: Perfect balance, excellent readability
- **12 characters**: Maximum recommended, maintains clarity
- **Pure Chinese Only**: Avoid mixing English words for best results
- **Examples**: "AI技术指南教程" (8 chars) ✅ "完整AI技术指南教程系统" (12 chars) ✅
- **Line Breaking**: Smart 9-character per line splitting optimized for Chinese text flow

#### 🇺🇸 English Titles  
**Optimal Length: 7 words**
- **7 words**: Perfect for 3-line layout without truncation
- **Pure English Only**: Avoid mixing Chinese characters for best results
- **Example**: "Complete AI Technology Guide Tutorial Series Episode" (7 words) ✅
- **Line Breaking**: Word-boundary wrapping preserves English word integrity
- **Note**: Longer titles may be truncated with ellipsis (...)

## 📦 Supported Parameters

### Required Parameters
1. **title** - Main title text (required)

### Optional Parameters  
2. **author** - Author name (optional, auto-capitalized)
3. **logo_path** - Logo file path (optional)
4. **right_image_path** - Right-side image path (optional)
5. **theme** - Theme mode: "dark", "light", "custom" (default: "dark")
6. **custom_template** - Custom background path for custom theme (required when theme="custom")
7. **title_color** - Title text color in hex format (e.g., "#FFFFFF")
8. **author_color** - Author text color in hex format (e.g., "#CCCCCC")  
9. **enable_triangle** - Enable/disable triangle overlay (boolean)
10. **triangle_direction** - Triangle direction: "top" (upward ▲) or "bottom" (downward ▼, default)
11. **flip** - Mirror layout: False (standard) or True (image left, text right)
12. **youtube_ready** - Generate YouTube API v3 compliant output (boolean, default: True)

### Theme Defaults
- **Dark Theme**: Black bg + White text (#FFFFFF) + Light gray author (#CCCCCC) + Black triangle
- **Light Theme**: White bg + Black text (#000000) + Dark gray author (#666666) + White triangle
- **Custom Theme**: User background + White text (#FFFFFF) + Light gray author (#CCCCCC) + No triangle

## 🤖 AI Title Optimization (New!)

### Solve Mixed Language Problems with Google Gemini
Our system now includes optional AI-powered title optimization using Google Gemini API to automatically fix mixed-language titles and improve formatting.

#### ⚠️ Why Title Optimization Matters
As mentioned earlier, mixed-language titles cause formatting issues:
- ❌ "AI技术指南 Complete Guide" - English words split incorrectly in Chinese mode
- ❌ "Learn Python编程" - Chinese characters break English word boundaries

#### ✅ How AI Optimization Fixes This
The Gemini API automatically converts mixed-language titles into clean, single-language versions with smart line-breaking:
- ✅ "AI技术指南 Complete Guide" → "AI技术完整\n指南教程" (2 lines, 6+4 chars)
- ✅ "Learn Python编程" → "Learn Python\nProgramming\nComplete Guide" (3 lines, balanced)
- ✅ "How to Build React Applications" → "Build React Apps\nFrom Scratch\nFull Guide" (natural breaks)

### 🔑 Setup & Configuration

#### Method 1: Environment Variable (Recommended)
```bash
# Set your Google API key as environment variable
export GOOGLE_API_KEY="your_google_api_key_here"

# Then use normally - optimization happens automatically
python your_script.py
```

#### Method 2: Direct API Key
```python
from youtube_thumbnail_generator import create_generator

# Pass API key directly
generator = create_generator(google_api_key="your_google_api_key_here")

# Or use FinalThumbnailGenerator directly
from youtube_thumbnail_generator import FinalThumbnailGenerator
generator = FinalThumbnailGenerator(google_api_key="your_google_api_key_here")
```

#### Method 3: No API Key (Fallback)
```python
# Works without API key - just skips optimization
generator = create_generator()
# Output: "Title optimization skipped - no API key or Gemini unavailable"
```

### 🧠 AI System Prompt

The AI uses this system prompt to optimize titles (you can modify this in `title_optimizer.py`):

```
You are a professional YouTube title optimizer. Your task is to convert mixed-language or poorly formatted titles into clean, single-language titles optimized for YouTube thumbnails.

CRITICAL RULES:
1. OUTPUT ONLY THE OPTIMIZED TITLE - No prefixes, suffixes, quotes, or explanations
2. Use SINGLE LANGUAGE ONLY - Pure Chinese OR Pure English OR Pure other language
3. Maintain the original meaning and intent
4. Optimize for YouTube thumbnail readability
5. SMART LINE-BREAKING: Use \n to create optimal line breaks for thumbnail display

LANGUAGE-SPECIFIC REQUIREMENTS:
- CHINESE/CJK: 10-18 characters total, max 2 lines, 6-9 characters per line
- ENGLISH/LATIN: 7-15 words total, max 3 lines, 2-6 words per line
- Use \n for line breaks and natural pause points

LANGUAGE DECISION RULES:
- If >60% Chinese characters: Convert to pure Chinese
- If >60% English words: Convert to pure English  
- Otherwise: Choose the dominant language and convert entirely

FORMATTING RULES:
- Remove unnecessary punctuation for thumbnails
- Use title case for English
- No quotation marks, brackets, or special symbols
- Make it catchy and clickable
```

### 📝 Customizing the System Prompt

To customize the AI behavior, edit the `TITLE_OPTIMIZATION_SYSTEM_PROMPT` variable in `title_optimizer.py`:

```python
# File: title_optimizer.py
TITLE_OPTIMIZATION_SYSTEM_PROMPT = """
Your custom prompt here...
Add your specific rules and preferences...
"""
```

### ⚙️ How It Works

1. **Detection**: Checks if title contains mixed languages (20-80% Chinese characters)
2. **API Call**: Sends title to Google Gemini with optimization prompt
3. **Validation**: Ensures response is valid and non-empty
4. **Fallback**: Uses original title if optimization fails
5. **Logging**: Shows whether title was optimized or unchanged

### 📊 Example Optimizations with Smart Line-breaking

```python
generator = create_generator(google_api_key="your_key")

# Mixed Chinese/English with smart line-breaking
result = generator.generate_final_thumbnail(
    title="AI技术指南 Complete Tutorial 2024",  # Mixed language
    output_path="test.jpg"
)
# Console: Title optimized by Gemini: 'AI技术指南 Complete Tutorial 2024' -> 'AI技术完整\n指南教程'

# Long English title with intelligent line breaks
result = generator.generate_final_thumbnail(
    title="How to Build React Applications from Scratch",  # Long English
    output_path="test2.jpg"
)
# Console: Title optimized by Gemini: 'How to Build React Applications from Scratch' -> 'Build React Apps\nFrom Scratch\nFull Guide'

# Pre-formatted titles are bypassed
result = generator.generate_final_thumbnail(
    title="Already Formatted\nTitle Test",  # Pre-formatted
    output_path="test3.jpg"  
)
# Console: Title unchanged by Gemini: 'Already Formatted\nTitle Test' (bypassed)
```

### 🔧 Requirements

To use title optimization, install the Google Generative AI package:

```bash
pip install google-generativeai
```

**Get your Google API key**: https://aistudio.google.com/app/apikey

## 🎨 Enhanced Chinese Font Bold Rendering (New!)

### Perfect Bold Effect for Both Dark and Light Themes

We've completely redesigned the Chinese font rendering system to provide professional Bold effects that look perfect on both dark and light backgrounds.

#### 🔧 Key Improvements

1. **STHeiti Medium Priority**: Upgraded font selection to prioritize STHeiti Medium.ttc for naturally bolder Chinese characters
2. **Smart Stroke Colors**: Intelligent stroke color selection based on text brightness:
   - **White text** (Dark theme) → Medium gray stroke `RGB(128,128,128)`
   - **Black text** (Light theme) → Light gray stroke `RGB(192,192,192)`
3. **Auto-Enable Stroke**: Chinese fonts ≥30px automatically enable stroke effects
4. **Enhanced Stroke Width**: Chinese text uses 8% stroke width (vs 5% for English) for stronger Bold effect

#### ⚡ Automatic Optimization

```python
generator = FinalThumbnailGenerator()

# Chinese text automatically gets Bold enhancement
result = generator.generate_final_thumbnail(
    title="AI智能视频生成技术",  # Chinese text auto-enables stroke
    theme="dark"  # White text with medium gray stroke
)

result = generator.generate_final_thumbnail(  
    title="AI智能视频生成技术",  # Chinese text auto-enables stroke
    theme="light"  # Black text with light gray stroke
)
```

#### 🎯 Visual Results

- **Dark Theme**: White Chinese text now has clearly visible medium-gray outline, creating perfect Bold effect
- **Light Theme**: Black Chinese text has light-gray outline that contrasts beautifully against white background
- **No More Fusion**: Stroke colors are carefully calibrated to avoid blending with text or background colors

#### 📝 Technical Details

```python
# Smart stroke color algorithm
def get_smart_stroke_color(text_color):
    brightness = (r * 0.299 + g * 0.587 + b * 0.114)
    
    if brightness > 127:  # Light text (white/light gray) - usually on dark background
        return (128, 128, 128)  # Medium gray stroke - visible but not too dark
    else:  # Dark text (black/dark gray) - usually on light background  
        return (192, 192, 192)  # Light gray stroke - contrasts with black text
```

This enhancement ensures Chinese text always appears Bold and professional, regardless of the theme background!

## 🎲 Random Template Generation

### One-Click Thumbnail Creation with 12 Random Combinations

Sometimes you just want a great-looking thumbnail without choosing specific template settings. The random template generator automatically selects from **12 possible combinations**:

**Template Combinations:**
- **Theme**: Dark (black background) or Light (white background) - 2 options
- **Triangle**: Enabled or Disabled - 2 options
- **Layout**: Standard (logo/text left, image right) or Flip (image left, logo/text right) - 2 options  
- **Triangle Direction**: Top (upward ▲) or Bottom (downward ▼) - when triangle enabled

**Breakdown:**
- **With Triangle**: 2 themes × 2 directions × 2 layouts = 8 combinations
- **Without Triangle**: 2 themes × 2 layouts = 4 combinations
- **Total**: 8 + 4 = **12 unique combinations**

### 🚀 Simple Usage

```python
from youtube_thumbnail_generator import generate_random_thumbnail

# Minimal usage - just title and author
result = generate_random_thumbnail(
    title="AI技术指南 Complete Tutorial",
    author="TechChannel"
)

# With custom images
result = generate_random_thumbnail(
    title="Learn Python Programming", 
    author="CodeMaster",
    logo_path="/path/to/logo.png",
    right_image_path="/path/to/image.jpg", 
    output_path="my_random_thumbnail.jpg"
)

# With AI optimization
result = generate_random_thumbnail(
    title="数据科学与机器学习完整教程",
    author="AI学院",
    google_api_key="your_google_api_key_here"
)
```

### 📊 Example Output

Each call produces different random combinations:

```bash
🎲 Random Template Configuration:
   Theme: light
   Triangle: Enabled (bottom direction)
   Layout: Standard
   📁 Output: thumbnail1.jpg

🎲 Random Template Configuration:
   Theme: dark
   Triangle: Disabled
   Layout: Flip
   📁 Output: thumbnail2.jpg

🎲 Random Template Configuration:
   Theme: light  
   Triangle: Enabled (top direction)
   Layout: Flip
   📁 Output: thumbnail3.jpg
```

### 🚨 Important Notes

- **Optional Feature**: Works without API key, just skips optimization
- **Smart Line-breaking**: AI creates optimal line breaks for thumbnail readability
- **Pre-formatted Bypass**: Titles with existing \n line breaks are not re-optimized
- **Rate Limits**: Google API has rate limits - consider for high-volume usage
- **Cost**: Google Gemini API has usage costs - check Google's pricing
- **Privacy**: Titles are sent to Google's servers for processing
- **Fallback**: Always falls back to original manual line-breaking if AI fails

## 🧠 Intelligent Text System

### Core Technology: PNG Overlay + Triangle Integration
Instead of drawing text directly on template:
1. **Independent Rendering**: Generate transparent PNG text images first
2. **Smart Adjustment**: Dynamically adjust PNG size based on text length
3. **Triangle Integration**: Paste triangle to right-side image first, then paste combined image to template
4. **Text Overlay**: PNG text pasted last, ensuring it's always on the top layer

### Chinese/English Differentiated Processing
#### Chinese Optimization
- **Font Enlargement**: 30% larger than English (54px vs 42px title)
- **Smart Line-breaking**: 
  - Title: Break after 9 characters, divide by 2, odd characters go to second line
- **Line Spacing**: Title 16px

#### English Processing
- **Space-based Line-breaking**: Natural word boundary wrapping
- **3-line Limit**: Title max 3 lines, auto-truncate with ellipsis
- **Standard Font**: Lexend Bold
- **Standard Line Spacing**: 8px

## 📝 Input Parameter Details

### Required Parameters
**`title`** (str) - Main title
```python
title="The Ultimate Complete Guide to Advanced AI Technology"
```
- **Smart Line-breaking**: Auto-calculate optimal line-break positions
- **Dynamic Height**: Adjust PNG height based on line count (55px/line + line spacing)
- **Dynamic Font Scaling**: Auto font size based on character count (1-17 chars)
- **Effects**: Clean bold font with theme-based colors
- **Position**: Starting at (55, 330), dynamically centered

### Optional Parameters

**`author`** (str) - Author name
```python
author="Leo Wang"  # Auto-converts to "LEO WANG"
```
- **Format**: Auto-convert to uppercase
- **Position**: Fixed bottom (55, 800)
- **Font**: 36px Lexend Bold, theme-based color

**`logo_path`** (str) - Logo file path
```python
logo_path="logos/your_logo.png"
```
- **Position**: Top-left corner (20, 20), left margin = top margin
- **Target Size**: 100x100 pixels (automatically processed)
- **Format**: Supports PNG/JPG, auto-handle transparency
- **⚠️ Important**: For best results, provide a **square logo** (1:1 aspect ratio). Non-square logos will be center-cropped, which may cut off important parts

**`right_image_path`** (str) - Right-side image path
```python
right_image_path="assets/your_image.jpg"
```
- **Smart Cropping**: Auto-convert to square (center crop)
- **Fill Method**: Scale to 900x900 pixels to fill right side
- **Position**: Right area starting at (700, 0)

### Theme & Color Parameters

**`theme`** (str) - Theme mode: "dark", "light", "custom"
```python
theme="dark"     # Default: Black bg + white text + black triangle
theme="light"    # White bg + black text + white triangle  
theme="custom"   # User-provided template + custom colors
```

**`custom_template`** (str) - Custom template path (required for custom theme)
```python
custom_template="path/to/your_template.png"  # Must be 1600x900 PNG
```

**`title_color`** (str) - Title text color in hex format
```python
title_color="#FFFFFF"  # White (dark theme default)
title_color="#000000"  # Black (light theme default)
title_color="#FF0000"  # Red (custom example)
```

**`author_color`** (str) - Author text color in hex format  
```python
author_color="#CCCCCC"  # Light gray (dark theme default)
author_color="#666666"  # Dark gray (light theme default)
author_color="#0000FF"  # Blue (custom example)
```

**`enable_triangle`** (bool) - Enable/disable triangle overlay
```python
enable_triangle=True   # Default for dark/light themes
enable_triangle=False  # Default for custom theme
```

**`triangle_direction`** (str) - Triangle direction when enabled  
```python
triangle_direction="bottom"  # Default: downward triangle ▼ (trapezoid)
triangle_direction="top"     # Upward triangle ▲ (inverted trapezoid)
```

**`flip`** (bool) - Mirror the entire layout
```python
flip=False  # Default: logo/text left, image right
flip=True   # Mirror: image left, logo/text right
```

**`youtube_ready`** (bool) - Optimize for YouTube API v3 compliance
```python
youtube_ready=True     # Default: Generate 1280x720 YouTube-compliant thumbnail (2MB max, JPEG, sRGB)
youtube_ready=False    # Generate 1600x900 high-resolution thumbnail
```

## 📦 Installation

The package is officially available on PyPI and can be installed worldwide:

### Quick Install (Recommended)
```bash
pip install youtube-thumbnail-generator
```

### With API Service Support
```bash
pip install "youtube-thumbnail-generator[api]"
```

### Alternative Installation Methods

| Method | Command | Use Case |
|--------|---------|----------|
| **PyPI (Stable)** | `pip install youtube-thumbnail-generator` | Production use, stable releases |
| **PyPI with API** | `pip install "youtube-thumbnail-generator[api]"` | Include Flask API dependencies |
| **GitHub (Latest)** | `pip install git+https://github.com/preangelleo/youtube-thumbnail-generator.git` | Latest development features |
| **Development** | `git clone ... && pip install -e .` | Local development and testing |

### Package Information
- **PyPI Page**: https://pypi.org/project/youtube-thumbnail-generator/
- **Current Version**: 2.2.0
- **License**: MIT
- **Python Support**: 3.7+
- **Dependencies**: Pillow (required), Flask+CORS (optional for API)

### 📦 What's Included Automatically
When you install via PyPI or GitHub, you get everything you need:
- ✅ **All Templates**: Dark, Light, and Custom background templates
- ✅ **Triangle Assets**: Black and white triangle overlays  
- ✅ **Professional Template**: 1600x900 high-quality base template
- ✅ **Font Assets**: Chinese/English optimized fonts
- ✅ **Sample Assets**: Testing logo and image files
- ✅ **Auto Template Creation**: If templates are missing, they're automatically generated in your project directory

**Smart Fallback System**: If bundled templates can't be found (rare edge case), the system automatically creates default templates in your current directory.

**No additional downloads needed** - start generating thumbnails immediately after installation!

## 🚀 Usage Methods

### 0. Interactive Testing Tool (New!)

Before diving into programmatic usage, try our interactive testing tool to quickly validate all features:

#### **initial_test.py** - Comprehensive Feature Validator

```bash
# Run interactive test (included with the package)
python initial_test.py
```

**What it does:**
- **Interactive Input**: Prompts you to enter any title you want to test
- **Complete Coverage**: Tests all 10 possible configurations automatically:
  - Dark theme: 4 variations (standard/flip × bottom/top triangle)
  - Light theme: 4 variations (standard/flip × bottom/top triangle)  
  - Custom theme: 2 variations (standard/flip layouts)
- **Real Results**: Generates actual thumbnail files you can inspect
- **Feature Validation**: Tests title positioning, logo placement, flip layouts, triangle overlays

**Example Session:**
```
============================================================
🎨 YouTube Thumbnail Generator - Interactive Test
============================================================

请输入要测试的标题 (Enter title to test): Complete AI Technology Guide

测试配置 (Test configurations):
- Dark theme: 4 variations (2 flip × 2 triangle)
- Light theme: 4 variations (2 flip × 2 triangle)
- Custom theme: 2 variations (2 flip only)
Total: 10 configurations

使用标题: 'Complete AI Technology Guide'

[1/10] 生成: dark_std_bottom
  ✅ 成功: Outputs/interactive_test/test_dark_std_bottom.jpg (182.4 KB)

[2/10] 生成: dark_std_top
  ✅ 成功: Outputs/interactive_test/test_dark_std_top.jpg (181.0 KB)

...

🎉 测试完成 (Test completed)!
生成文件: 10/10
输出目录: Outputs/interactive_test
```

**Output Files:**
- `test_dark_std_bottom.jpg` - Dark theme, standard layout, bottom triangle
- `test_dark_std_top.jpg` - Dark theme, standard layout, top triangle
- `test_dark_flip_bottom.jpg` - Dark theme, flipped layout, bottom triangle
- `test_dark_flip_top.jpg` - Dark theme, flipped layout, top triangle
- `test_light_std_bottom.jpg` - Light theme, standard layout, bottom triangle
- `test_light_std_top.jpg` - Light theme, standard layout, top triangle
- `test_light_flip_bottom.jpg` - Light theme, flipped layout, bottom triangle
- `test_light_flip_top.jpg` - Light theme, flipped layout, top triangle
- `test_custom_std.jpg` - Custom theme, standard layout
- `test_custom_flip.jpg` - Custom theme, flipped layout

**Why Use initial_test.py:**
- ✅ **Quick Validation**: Test all features with one command
- ✅ **Visual Results**: See exactly how your titles will look
- ✅ **Layout Comparison**: Compare standard vs flipped layouts
- ✅ **Triangle Preview**: See both triangle directions
- ✅ **Zero Setup**: Uses default templates and assets
- ✅ **Development Tool**: Perfect for testing during integration

### 1. Use as Python Library

#### Dark Theme (Default - YouTube Ready)
```python
from youtube_thumbnail_generator import FinalThumbnailGenerator, get_default_template

# Initialize generator with bundled template
generator = FinalThumbnailGenerator(get_default_template())

# Generate YouTube-ready thumbnail (1280x720, <2MB, optimized for API upload)
result = generator.generate_final_thumbnail(
    title="Complete AI Technology Guide",  # 5 words - will be enlarged
    author="Leo Wang",
    logo_path="logos/your_logo.png",
    right_image_path="assets/your_image.jpg",
    output_path="outputs/dark_theme_youtube.jpg",
    theme="dark"  # Default theme, youtube_ready=True by default
)
```

#### Light Theme (YouTube Ready)
```python
# Generate Light theme YouTube-ready thumbnail  
result = generator.generate_final_thumbnail(
    title="AI技术指南完整教程",  # 10 Chinese characters - optimal
    author="Leo Wang",
    logo_path="logos/your_logo.png", 
    right_image_path="assets/your_image.jpg",
    output_path="outputs/light_theme_youtube.jpg",
    theme="light",
    title_color="#000000",  # Black text for white background
    author_color="#666666"  # Dark gray author
    # youtube_ready=True by default - 1280x720 YouTube API ready
)
```

#### Custom Theme (YouTube Ready)
```python
# Generate Custom theme YouTube-ready thumbnail
result = generator.generate_final_thumbnail(
    title="Custom Background Demo",  # 4 words - will be enlarged
    author="Your Name",
    logo_path="logos/your_logo.png",
    right_image_path=None,  # No right image needed
    output_path="outputs/custom_theme_youtube.jpg",
    theme="custom",
    custom_template="your_background_1600x900.png",  # Your custom background
    title_color="#FFFFFF",  # White text  
    author_color="#CCCCCC",  # Light gray author
    enable_triangle=False  # No triangle overlay
    # youtube_ready=True by default - optimized for YouTube API
)
```

### 2. Command Line API Service
Launch API directly after installation:

```bash
# Start API service directly
youtube-thumbnail-api

# Or use Python module method
python -m youtube_thumbnail_generator.api_server
```

### 3. YouTube API v3 Ready Thumbnails

Generate thumbnails that are fully compliant with YouTube API v3 upload requirements:

```python
from youtube_thumbnail_generator import FinalThumbnailGenerator, get_default_template

generator = FinalThumbnailGenerator(get_default_template())

# Generate YouTube API v3 compliant thumbnail (default behavior)
result = generator.generate_final_thumbnail(
    title="My YouTube Video Title",
    author="Channel Name", 
    logo_path="my_logo.png",
    right_image_path="video_frame.jpg",
    output_path="my_video_thumbnail.jpg",
    theme="dark"
    # youtube_ready=True by default - outputs 1280x720 JPEG, sRGB, <2MB
)
# Output: Ready for direct YouTube API upload!
```

#### Manual YouTube Optimization
```python
from youtube_thumbnail_generator import optimize_for_youtube_api

# Optimize existing thumbnail for YouTube API
youtube_ready_path = optimize_for_youtube_api(
    input_path="my_large_thumbnail.jpg",
    output_path="my_thumbnail_youtube_ready.jpg"  # Optional
)
# Automatically converts to 1280x720 JPEG, ensures <2MB size
```

#### YouTube API v3 Compliance Features
- **✅ Perfect Dimensions**: 1280x720 pixels (16:9 aspect ratio)
- **✅ Optimal Format**: JPEG with baseline encoding
- **✅ File Size Control**: Automatic compression to stay under 2MB limit
- **✅ Color Space**: sRGB color profile for consistent display
- **✅ Smart Cropping**: Maintains aspect ratio with center cropping
- **✅ Quality Optimization**: Multi-level quality testing (95→90→85→80→75→70)

### 4. Use in Other Python Projects
```python
# In your Python projects
from youtube_thumbnail_generator import FinalThumbnailGenerator, get_default_template, create_text_png

# Quick YouTube-ready thumbnail generation with bundled template
generator = FinalThumbnailGenerator(get_default_template())
result = generator.generate_final_thumbnail(
    title="Your Video Title",
    output_path="output/thumbnail_youtube.jpg"
    # Outputs 1280x720 YouTube API compliant thumbnail by default
)

# Or generate text PNG only
success, text_img, height = create_text_png(
    text="Test Text",
    width=600,
    height=200,
    language="chinese"
)
```

### 5. API Service Calls

#### Generate Thumbnail
```bash
curl -X POST http://localhost:5002/api/generate/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Tech Reviews 2025",
    "author": "Leo Wang",
    "logo_path": "logos/animagent_logo.png",
    "right_image_path": "assets/testing_image.jpeg"
  }'
```

#### Response Example
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "processing",
  "message": "Thumbnail generation task started"
}
```

#### Check Task Status
```bash
curl http://localhost:5002/api/status/abc123-def456-ghi789
```

#### Download Result
```bash
curl -O http://localhost:5002/api/download/final_test.jpg
```

### 6. Python API Client Example
```python
import requests
import time
import json

def generate_thumbnail_api(title, author=None, logo_path=None, image_path=None):
    """Generate thumbnail using API"""
    
    # 1. Send generation request
    response = requests.post('http://localhost:5002/api/generate/enhanced', 
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "title": title,
            "author": author,
            "logo_path": logo_path,
            "right_image_path": image_path
        })
    )
    
    task_data = response.json()
    task_id = task_data['task_id']
    print(f"Task created: {task_id}")
    
    # 2. Poll status until complete
    while True:
        status_response = requests.get(f'http://localhost:5002/api/status/{task_id}')
        status_data = status_response.json()
        
        print(f"Status: {status_data['status']}")
        
        if status_data['status'] == 'completed':
            print(f"Generation complete! Download: {status_data['download_url']}")
            return status_data['download_url']
        elif status_data['status'] == 'failed':
            print(f"Generation failed: {status_data['error']}")
            return None
        
        time.sleep(1)

# Usage example
download_url = generate_thumbnail_api(
    title="My Amazing YouTube Video Title That Is Really Long",
    author="Your Name",
    logo_path="logos/my_logo.png",
    image_path="assets/thumbnail_image.jpg"
)
```

## 🎯 Complete API Endpoint Guide

### Thumbnail Generation
`POST /api/generate/enhanced`

**Request Body**:
```json
{
  "title": "Required - Main title text",
  "author": "Optional - Author name",
  "logo_path": "Optional - Logo file path",
  "right_image_path": "Optional - Right-side image path"
}
```

### Chapter Image Generation  
`POST /api/generate/chapter`

**Request Body**:
```json
{
  "text": "Required - Text to display",
  "language": "Optional - english/chinese",
  "font_size": "Optional - Font size",
  "width": "Optional - Image width, default 1600", 
  "height": "Optional - Image height, default 900"
}
```

### Other Endpoints
- `GET /api/status/<task_id>` - Check task status
- `GET /api/download/<filename>` - Download generated file
- `GET /api/health` - Health check
- `GET /api/templates` - Get available templates
- `GET /api/assets` - Get resource list

## 📊 Smart Layout Examples

### Short Title Effect
```
Title: "Tech News 2025" 
→ 1 line, centered layout, clean appearance
```

### Long Title Effect  
```
Title: "The Ultimate Complete Guide to Advanced AI Technology..."
→ Multiple lines with smart line-breaking
Auto-adjust positions for perfect fit
```

### Overlong Content Handling
```
Title exceeds 3 lines → Auto-truncate with ellipsis
Ensure stable layout, prevent content overflow
```

## 🔧 Advanced Configuration

### Manual Template Creation
If you need to manually create templates in your project directory:

```python
from youtube_thumbnail_generator import init_templates

# This creates a 'templates/' directory with all required files:
# - professional_template.jpg (1600x900 black background)
# - light_template.png (1600x900 white background) 
# - triangle_black.png (200x900 opaque black triangle)
# - triangle_white.png (200x900 opaque white triangle)
init_templates()
```

### Advanced Triangle Customization
For advanced users who want custom triangle effects:

```python
from youtube_thumbnail_generator import generate_triangle_template

# Generate 4 different triangle variants:
generate_triangle_template("black", "bottom")    # Default: point at bottom-left
generate_triangle_template("black", "top")       # Point at top-left  
generate_triangle_template("white", "bottom")    # White, point at bottom-left
generate_triangle_template("white", "top")       # White, point at top-left

# Custom colors and sizes:
generate_triangle_template("#FF0000", "bottom", "red_triangle.png", 300, 900)
generate_triangle_template("#00FF00", "top", "green_triangle_top.png")
```

#### Triangle Options:
- **Colors**: `"black"`, `"white"`, or hex colors like `"#FF0000"`
- **Directions**: `"bottom"` (point at bottom-left), `"top"` (point at top-left)
- **Custom sizes**: width and height in pixels
- **Custom paths**: specify your own output filename

### File Path Rules
- **Relative Paths**: Relative to project root directory
- **Logo Directory**: `logos/` - Store all logo files
- **Assets Directory**: `assets/` - Store background images
- **Output Directory**: `outputs/` - Generated results storage
- **Template Directory**: `templates/` - Template file storage (auto-created if needed)

### Supported Image Formats
- **Input**: PNG, JPG, JPEG (supports transparency)
- **Output**: JPG (high quality, 95% quality)
- **Processing**: Auto color mode conversion

### Font Priority
```
English Fonts:
1. Helvetica (Mac system)
2. Lexend Bold (if installed)
3. Ubuntu Bold (Linux)
4. System default font

Chinese Fonts:
1. Noto Sans CJK Bold
2. Source Han Sans
3. WenQuanYi fonts
```

## 📁 Project Structure
```
youtube_thumbnail_generator/
├── __init__.py                       # Package initialization
├── final_thumbnail_generator.py      # Core generator engine
├── text_png_generator.py             # PNG text renderer with Chinese/English optimization
├── api_server.py                     # Flask API service
├── function_add_chapter.py           # Chapter functionality  
├── youtube_standards.py              # YouTube API compliance utilities
├── initial_test.py                   # Interactive testing tool (NEW!)
├── title_optimizer.py                # AI title optimization with Google Gemini (NEW!)
├── assets/
│   ├── animagent_logo.png           # Default testing logo
│   └── testing_image.jpeg           # Default testing image
├── fonts/                           # Built-in font assets (auto-downloaded)
│   ├── Ubuntu-B.ttf                # Ubuntu Bold font
│   └── NotoSansCJK-Bold.ttc        # Noto Sans CJK Bold font
├── templates/                       # Auto-generated templates
│   ├── professional_template.jpg    # 1600x900 dark theme template
│   ├── light_template.png          # 1600x900 light theme template
│   ├── triangle_black.png          # Black triangle overlay (bottom)
│   ├── triangle_white.png          # White triangle overlay (bottom)
│   ├── triangle_black_top.png      # Black triangle overlay (top)
│   ├── triangle_white_top.png      # White triangle overlay (top)
│   ├── triangle_black_bottom.png   # Black triangle overlay (bottom variant)
│   └── triangle_white_bottom.png   # White triangle overlay (bottom variant)
├── Outputs/                         # Generated thumbnails output
│   └── interactive_test/           # initial_test.py outputs
├── setup.py                         # Package setup
├── pyproject.toml                   # Modern Python packaging
├── CHANGELOG.md                     # Version history and updates
└── README.md                        # Complete project documentation
```

### Key File Descriptions

**Core Engine Files:**
- `final_thumbnail_generator.py` - Main thumbnail generation engine with theme support, flip layouts, and text positioning
- `text_png_generator.py` - Advanced text rendering with Chinese/English optimization, smart line-breaking, and font scaling
- `youtube_standards.py` - YouTube API v3 compliance utilities and image optimization
- `title_optimizer.py` - AI-powered title optimization using Google Gemini API (optional)

**User Tools:**
- `initial_test.py` - **Interactive testing tool** - Run to test all 10 configurations with any title
- `api_server.py` - RESTful API service for web integration

**Auto-Generated Assets:**
- `templates/` - All theme templates auto-created if missing
- `fonts/` - Built-in fonts downloaded on first use
- `assets/` - Default logos and images for testing

**Testing and Development:**
- `Outputs/interactive_test/` - Results from initial_test.py runs
- `CHANGELOG.md` - Detailed version history and feature updates

## 📈 Version History

### v2.4.3 (Current) - Intelligent Image Processing & CDN Examples
- 🧠 **Smart Image Processing**: Intelligent image resize and center-crop algorithm for perfect 900x900 thumbnails
  - Auto scale-up when min dimension < 900px  
  - Center crop for both horizontal and vertical images
  - Preserves aspect ratio during scaling
- 📏 **Configurable Logo Size**: Logo size now controlled by LOGO_SIZE constant (100x100px)
  - Easy customization for different logo requirements
  - Consistent 100x100px output with smart center-cropping
- 🌐 **CDN-Hosted Examples**: All example images now hosted on public CDN
  - Dramatically reduced package size (no bundled images)
  - Fast worldwide loading from CDN
  - Always up-to-date examples
- 📖 **Simplified Documentation**: Removed duplicate guides, streamlined user experience
- ⚠️ **Logo Recommendations**: Clear guidance for square logo usage to prevent cropping issues

### v2.4.2 - Enhanced Stroke Effects & Examples Gallery
- 🎨 **Enhanced Examples Gallery**: Complete EXAMPLES.md with all 12 template combinations using v2.4.2 stroke effects
- 📸 **New Sample Generation**: All examples regenerated with enhanced Chinese bold rendering
- 📖 **Simplified README**: Streamlined examples section with direct link to comprehensive gallery
- 🔗 **Better Navigation**: Clear link structure between README and detailed examples
- ✨ **v2.4.2 Branding**: Updated version references and sample file organization

### v2.4.1 - Complete API Integration & Enhanced Features
- 🚀 **Complete API Support**: New `/api/generate/random` endpoint for 12 random template combinations
- 🔧 **Enhanced API Parameters**: Full support for `triangle_direction`, `flip`, `google_api_key`, `youtube_ready` in `/api/generate/enhanced`
- 📖 **Comprehensive API Documentation**: Detailed parameter descriptions and 12-combination reference table
- ✅ **API Testing Verified**: All endpoints tested with curl and confirmed working
- 🎲 **Random API Integration**: Seamless integration with existing random thumbnail generation function

### v2.4.0 - AI-Powered Title Optimization with Smart Line-breaking  
- 🆕 **AI Title Optimization**: Google Gemini 2.0 Flash API integration for mixed-language title fixing
- 🆕 **Smart Line-breaking**: AI creates optimal line breaks (Chinese: 2 lines, English: 3 lines)
- 🆕 **Pre-formatted Bypass**: Titles with existing \n line breaks skip AI optimization
- 🆕 **Language-specific Rules**: Character-based for CJK, word-based for Latin scripts
- 🆕 **Configurable System Prompt**: Customizable AI optimization behavior in title_optimizer.py
- 🆕 **AI-first Architecture**: Smart optimization with fallback to manual line-breaking
- ✅ **Environment Variable Support**: `GOOGLE_API_KEY` auto-detection
- ✅ **Enhanced API**: `google_api_key` parameter in all generator functions
- 🎨 **Perfect Chinese Bold**: STHeiti Medium font priority + intelligent stroke effects for professional Bold rendering
- 🧠 **Smart Stroke Colors**: RGB(128,128,128) for white text, RGB(192,192,192) for black text based on brightness detection
- 🔤 **Auto-Enable Stroke**: Chinese fonts ≥30px automatically enable stroke effects for Enhanced Bold appearance
- 🎮 **Enhanced Interactive Testing**: Enter-to-continue experience with intelligent defaults (title-only input required)
- 🎲 **12 Template Combinations**: Updated random generation with triangle enable/disable combinations
- ✅ **Default Flow Optimization**: Users can press Enter through entire flow except title input
- 🚀 **Quick Start Guide**: Added comprehensive one-click experience documentation
- 🆕 **Configurable System Prompt**: Customizable AI optimization behavior in title_optimizer.py
- 🆕 **AI-first Architecture**: Smart optimization with fallback to manual line-breaking
- ✅ **Environment Variable Support**: `GOOGLE_API_KEY` auto-detection
- ✅ **Enhanced API**: `google_api_key` parameter in all generator functions
- ✅ **Comprehensive Logging**: Clear feedback on optimization success/failure

### v2.3.0 - Advanced Layout & Text Engine  
- ✅ **Interactive Testing Tool**: New `initial_test.py` for comprehensive feature validation
- ✅ **Flip Layout System**: Mirror layouts with precise positioning for creative variety
- ✅ **Advanced Text Engine**: 
  - Chinese: 18-character limit with "..." truncation, 9-character per line smart breaking
  - English: 3-line limit with ellipsis truncation, word-boundary wrapping
- ✅ **Logo Position Control**: Configurable logo margins (20px default) with flip support
- ✅ **Triangle Direction Control**: Top and bottom triangle variants for all themes
- ✅ **Right-Aligned Text**: PNG internal right-alignment for flip layouts
- ✅ **Built-in Font System**: Ubuntu and Noto Sans CJK fonts auto-downloaded
- ✅ **Refined Positioning**: Precise margin calculations for professional alignment

### v2.2.2 - YouTube-Ready by Default  
- ✅ **Default YouTube Optimization**: All thumbnails are YouTube API compliant by default
- ✅ **Seamless User Experience**: No extra steps needed for YouTube uploads
- ✅ **Clean File Management**: Optimized files use original filenames
- ✅ **High-Resolution Option**: Use `youtube_ready=False` for 1600x900 images

### v2.2.1 - YouTube API Integration
- ✅ **YouTube API v3 Compliance**: Built-in optimization for YouTube thumbnail uploads
- ✅ **Smart Resource Management**: Package path resolution with automatic fallback template creation
- ✅ **Format Optimization**: 1280x720 JPEG, sRGB color space, <2MB file size control
- ✅ **Quality Control**: Multi-level compression testing for optimal file size
- ✅ **Cross-Platform**: Improved compatibility across Python 3.7+ environments

### v2.2.0 - Three Theme Architecture Revolution
- ✅ **Complete Theme System**: Dark, Light, and Custom modes with full parameterization
- ✅ **Color Customization**: Hex color support for titles and authors
- ✅ **Triangle Control**: Configurable overlay effects per theme
- ✅ **Custom Backgrounds**: User-provided template support

### v2.1 - Smart Layout Revolution
- ✅ **PNG Overlay Technology**: Text rendering separated from template, perfect control
- ✅ **Smart Height Adjustment**: Dynamically adjust layout based on content length
- ✅ **Line Spacing Optimization**: 8px line spacing, improved reading experience
- ✅ **Triangle Transition**: 200x900 diagonal separation, professional visual effects
- ✅ **Truncation Mechanism**: Smart truncation for overlong content, stable layout
- ✅ **Dual API Support**: Thumbnail + Chapter dual-function API
- ✅ **Python Package**: Installable as pip package, use in any Python project

### v1.0 - Basic Functionality
- ✅ Professional template layout design
- ✅ Auto square image conversion  
- ✅ 5-parameter input system
- ✅ Smart font selection
- ✅ Complete text effects
- ✅ Flask API integration

## 🏆 Project Status

### PyPI Distribution
- **📦 Live on PyPI**: https://pypi.org/project/youtube-thumbnail-generator/
- **🌍 Global Install**: `pip install youtube-thumbnail-generator`  
- **📊 Download Stats**: Available on [PyPI Stats](https://pepy.tech/project/youtube-thumbnail-generator)
- **🔖 Latest Version**: 2.2.2
- **📅 Published**: August 2025

### Community & Support
- **⭐ GitHub Stars**: https://github.com/preangelleo/youtube-thumbnail-generator
- **🐛 Issue Tracking**: https://github.com/preangelleo/youtube-thumbnail-generator/issues
- **📖 Documentation**: Complete README and API docs
- **🌐 International**: Full English documentation for global users

## 🎯 Best Practices

### Title Text Suggestions
- **Language Purity**: Use single language only - avoid mixing Chinese and English for best formatting
- **Length**: Recommend 50-100 characters, system auto-optimizes display
- **Content**: Clearly express video theme, attract viewer clicks
- **Keywords**: Front-load important keywords, improve search results
- **Examples**:
  - ✅ Good: "AI技术指南完整教程" (Pure Chinese)
  - ✅ Good: "Complete AI Technology Guide" (Pure English)  
  - ❌ Avoid: "AI技术 Complete Guide" (Mixed languages)


### Image Selection Principles
- **Size**: Any size, system auto-converts to square
- **Content**: Choose visually impactful images
- **Quality**: Recommend high resolution, ensure clarity after scaling

## 🚨 Troubleshooting & Important Notes

### 🔧 Common Issues & Solutions

#### Mixed Language Text Formatting Issues
**Problem**: Text appears broken, words split incorrectly, or unexpected line breaks.

**Root Cause**: Our system uses different text processing for Chinese vs English:
- **Chinese Mode**: Splits text by character count (9 chars/line), may break English words
- **English Mode**: Splits by word boundaries, may not handle Chinese characters properly

**Solutions**:
1. **Use Pure Chinese**: `"AI技术指南完整教程"` ✅
2. **Use Pure English**: `"Complete AI Technology Guide"` ✅
3. **Avoid Mixed**: `"AI技术 Guide"` ❌ `"Learn Python编程"` ❌

**Language Detection**: The system auto-detects based on character ratio:
- ≥30% Chinese characters → Chinese mode (9-char line breaking)
- <30% Chinese characters → English mode (word-boundary breaking)

#### Template Files Not Found
If you encounter `FileNotFoundError` for template files:

**Problem**: Templates missing after PyPI installation or in development.

**Solutions** (try in order):
1. **Automatic Resolution** - The system will automatically create missing templates
2. **Manual Creation**:
   ```python
   from youtube_thumbnail_generator import init_templates
   init_templates()  # Creates all required templates
   ```
3. **Resource Path Check**:
   ```python
   from youtube_thumbnail_generator import get_resource_path
   print(get_resource_path("templates/professional_template.jpg"))
   ```

#### Custom Triangle Effects Not Working
**Problem**: Default triangles don't match your design needs.

**Solution**: Generate custom triangles:
```python
from youtube_thumbnail_generator import generate_triangle_template

# 4 basic variants:
generate_triangle_template("black", "bottom")  # Standard
generate_triangle_template("black", "top")     # Inverted
generate_triangle_template("white", "bottom")  # Light theme
generate_triangle_template("white", "top")     # Light inverted

# Custom colors:
generate_triangle_template("#FF6B35", "bottom", "custom_orange.png")
```

#### YouTube API Upload Failures
**Problem**: Generated thumbnails rejected by YouTube API.

**Check**: Ensure you're using the YouTube-optimized version:
```python
result = generator.generate_final_thumbnail(
    title="Your Title",
    youtube_ready=True  # This is now default - ensures 1280x720, <2MB, sRGB
)

# Or manually optimize existing thumbnails:
from youtube_thumbnail_generator import optimize_for_youtube_api
youtube_path = optimize_for_youtube_api("your_thumbnail.jpg")
```

### 📋 System Requirements & Notes

1. **File Paths**: All paths are automatically resolved with smart fallbacks
2. **Font Dependencies**: System will auto-downgrade to available fonts  
3. **Template Management**: Missing templates are auto-created in your project directory
4. **Output Format**: Default YouTube-ready (1280x720 JPEG), use `youtube_ready=False` for high-res
5. **API Processing**: API uses async processing, poll status for completion
6. **Memory Usage**: Large image processing may use significant memory
7. **Cross-Platform**: Full compatibility across macOS, Linux, and Windows

---

## 🚀 Instant Start (New!)

### 🎆 Zero Setup Way (Recommended)
```python
from youtube_thumbnail_generator import create_generator

# Create generator with default template - no setup needed!
generator = create_generator()

# Generate a thumbnail
result = generator.generate_final_thumbnail(
    title="How to Build Amazing Apps",
    author="TECH GURU",
    youtube_ready=True  # Ensures 1280x720, <2MB, sRGB compliance
)

print(f"Thumbnail saved: {result}")
```

### 📝 Alternative Ways
```python
from youtube_thumbnail_generator import FinalThumbnailGenerator

# Method 1: Use default template (auto-created if missing)
generator = FinalThumbnailGenerator()  # No template path needed!

# Method 2: Use custom template (must be exactly 1600x900)
generator = FinalThumbnailGenerator("my_custom_template.jpg")
```

🎆 **NEW**: No template path required! Auto-creates when missing.  
⚠️ **Custom templates**: Must be exactly 1600x900 pixels.

## 💡 Quick Start

1. **Install Package**: `pip install youtube-thumbnail-generator`
2. **Prepare Assets**: Put logos and images in corresponding directories
3. **Direct Test**: 
   ```python
   from youtube_thumbnail_generator import FinalThumbnailGenerator, get_default_template
   generator = FinalThumbnailGenerator(get_default_template())
   generator.generate_final_thumbnail(title="Test Title", output_path="test_youtube.jpg")
   # Generates 1280x720 YouTube-ready thumbnail by default
   ```
4. **API Service**: `youtube-thumbnail-api`
5. **Check Result**: Look at generated file

Start creating professional YouTube thumbnails now! 🎬✨