# YouTube Thumbnail Generator v2.4.8

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
- ✅ **Intelligent Image Processing**: Auto square conversion + 900x900 filling with smart resize/crop
- ✅ **Multi-endpoint API Support**: Flask RESTful API + Chapter functionality
- ✅ **Smart Font Selection**: Chinese PingFang/Founder, English Lexend Bold
- ✅ **Three Theme Modes**: Dark (black bg), Light (white bg), Custom (user template)
- ✅ **Full Color Customization**: Title color, author color, triangle toggle - all parameterized
- ✅ **Dynamic Font Scaling**: Auto font size adjustment based on text length (1-17 characters)
- ✅ **YouTube API Ready**: Built-in optimization for YouTube API v3 thumbnail upload compliance
- 🆕 **AI Title Optimization**: Google Gemini-powered mixed-language title optimization (optional)
- 🎲 **Random Template Generation**: One-click thumbnail creation with 12 random template combinations
- 🤖 **AI Agent Documentation**: Built-in `readme()` and `readme_api()` methods for AI code assistants

## 🎨 Template Examples

### Professional Dark Theme with Triangle
**Perfect for**: Tech content, gaming, serious topics  
**Features**: Enhanced Chinese bold rendering with intelligent stroke effects

**Examples Available:**
- **English Example**: Professional dark theme with triangle overlay - perfect for tech content
- **Chinese Example**: Enhanced Chinese bold rendering with intelligent stroke effects

**[🎨 View Live Examples →](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/EXAMPLES.md)**

#### 📖 **[View Complete Examples Gallery →](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/EXAMPLES.md)**

**More Examples Available:**
- **12 Template Combinations**: Professional, Standard, Triangle themes × Dark/Light × With/Without triangle overlays
- **Mixed Language Support**: Chinese and English title examples 
- **Enhanced Stroke Effects**: Perfect bold rendering for both dark and light backgrounds
- **CDN-Hosted**: All examples hosted on fast public CDN for worldwide access

## 💡 Optimal Length Recommendations

### 🎯 Best Results Guidelines
For the most professional and visually appealing thumbnails:

#### ⚠️ **IMPORTANT: Single Language Only**
**Our system is optimized for single-language titles. Mixed languages may cause formatting issues.**

🚫 **Avoid Mixed Languages**:
- ❌ "AI技术指南 Complete Guide" - English words may be improperly split in Chinese mode
- ❌ "Complete AI 技术指南" - Chinese characters may break English word spacing

✅ **Use Single Languages**:
- ✅ "AI技术指南完整教程" - Pure Chinese
- ✅ "Complete AI Technology Guide" - Pure English

#### 🇨🇳 Chinese Titles
**Optimal Length: 10-12 characters**
- **10 characters**: Perfect balance, excellent readability
- **12 characters**: Maximum recommended, maintains clarity
- **Pure Chinese Only**: Avoid mixing English words for best results

#### 🇺🇸 English Titles  
**Optimal Length: 7 words**
- **7 words**: Perfect for 3-line layout without truncation
- **Pure English Only**: Avoid mixing Chinese characters for best results

## 📦 Installation

### Quick Install (Recommended)
```bash
pip install youtube-thumbnail-generator
```

### With API Service Support
```bash
pip install "youtube-thumbnail-generator[api]"
```

## 🚀 Quick Start

### 1. Simple Python Usage (Recommended)
```python
from youtube_thumbnail_generator import create_generator

# Create generator with zero configuration (recommended)
generator = create_generator()

# Generate YouTube-ready thumbnail (1280x720, <2MB, optimized for API upload)  
result = generator.generate_final_thumbnail(
    title="Complete AI Technology Guide",
    author="Leo Wang",
    logo_path="logos/your_logo.png",     # ⚠️ Use square logo (1:1 ratio) for best results
    right_image_path="assets/image.jpg", # Any size - auto-processed to 900x900
    output_path="outputs/thumbnail.jpg"
)
```

### 🎨 Color Customization

Customize text colors for any theme using hex color codes:

```python
# Example 1: Custom colors with dark theme
result = generator.generate_final_thumbnail(
    title="Your Title Here",
    author="Your Name",
    theme="dark",
    title_color="#FF6B35",    # Orange title
    author_color="#4ECDC4",   # Teal author name
    output_path="custom_colors.jpg"
)

# Example 2: Custom colors with light theme
result = generator.generate_final_thumbnail(
    title="Another Title",
    author="Creator Name",
    theme="light",
    title_color="#2E86AB",    # Blue title
    author_color="#A23B72",   # Purple author name
    output_path="light_custom.jpg"
)

# Example 3: Custom template with custom colors
result = generator.generate_final_thumbnail(
    title="Custom Everything",
    author="Your Brand",
    theme="custom",
    custom_template="my_template.jpg",
    title_color="#FFFFFF",    # White text
    author_color="#FFD93D",   # Yellow author
    enable_triangle=False,    # Disable triangle overlay
    output_path="fully_custom.jpg"
)
```

#### 🎨 Color Parameter Guide:
- **`title_color`**: Hex color code for the main title text (e.g., "#FF0000" for red)
- **`author_color`**: Hex color code for the author name text (e.g., "#00FF00" for green)
- **Format**: Must use hex format with # prefix (e.g., "#FFFFFF", "#000000")
- **Default Colors**:
  - Dark theme: White title (#FFFFFF), Light gray author (#CCCCCC)
  - Light theme: Black title (#000000), Dark gray author (#666666)
  - Custom theme: Uses provided colors or defaults to theme colors

### Alternative Usage (Advanced)
```python
from youtube_thumbnail_generator import FinalThumbnailGenerator

# Direct class instantiation (for advanced users)
generator = FinalThumbnailGenerator()
# ... same usage as above
```

## 🤖 AI Agent Support (New in v2.5.0)

Special methods designed for AI code assistants and LLMs to quickly understand the library:

```python
from youtube_thumbnail_generator import create_generator

generator = create_generator()

# Get complete usage documentation
docs = generator.readme()
print(docs)  # Full library documentation for AI agents

# Get API documentation
api_docs = generator.readme_api()
print(api_docs)  # Complete REST API documentation
```

**Perfect for**: 
- AI-powered development workflows
- Code generation assistants (GitHub Copilot, Cursor, etc.)
- LLM-based automation tools
- No need to search for external documentation

## 🎲 Random Template Generation

Generate thumbnails with random themes, triangle variations, and layouts for creative inspiration!

### Method 1: Using theme="random" (Recommended)
```python
from youtube_thumbnail_generator import create_generator

generator = create_generator()

# Generate with completely random settings
result = generator.generate_final_thumbnail(
    title="Your Amazing Title",
    author="Your Name",
    theme="random",  # ✨ Magic happens here!
    output_path="random_thumbnail.jpg"
)
```

### Method 2: Using theme=None
```python
# Omit theme parameter or set to None - same as theme="random"
result = generator.generate_final_thumbnail(
    title="Another Great Title",
    author="Creator Name",
    theme=None,  # Also triggers random generation
    output_path="another_random.jpg"
)
```

### Method 3: Direct Random Function
```python
from youtube_thumbnail_generator import generate_random_thumbnail

# Call random function directly (most flexible)
result = generate_random_thumbnail(
    title="Direct Random Call",
    author="Your Name",
    logo_path="logos/logo.png",
    right_image_path="images/image.jpg", 
    output_path="direct_random.jpg"
)
```

### 🎯 What Gets Randomized?
- **Theme**: Dark or Light background
- **Triangle**: Enabled/Disabled + Top/Bottom direction  
- **Layout**: Normal or Flipped layout
- **Result**: 12 possible combinations for endless variety!

### 2. Interactive Testing Tool
```bash
python initial_test.py
# Enter your title, then press Enter through the defaults for quick testing
```

### 3. API Service
```bash
youtube-thumbnail-api
# Starts service at http://localhost:5002
```

**📖 [Complete API Documentation →](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/README_API.md)**

## 📝 Key Parameters

### Logo Requirements
- **Target Size**: 100x100 pixels (automatically processed)
- **⚠️ Important**: For best results, provide a **square logo** (1:1 aspect ratio). Non-square logos will be center-cropped, which may cut off important parts

### Image Processing  
- **Input**: Any size image (PNG/JPG)
- **Processing**: Smart resize + center crop
- **Output**: Perfect 900x900 pixels
- **Algorithm**: If min dimension < 900px → scale up → center crop

### Theme Options
- **Dark Theme**: Black background + white text + black triangle (default)
- **Light Theme**: White background + black text + white triangle  
- **Custom Theme**: Your background + custom colors + optional triangle
- **Random Theme**: `theme="random"` or `theme=None` - automatically picks random combinations! 🎲

### Color Parameters
- **`title_color`** (optional): Hex color code for title text
  - Format: `"#RRGGBB"` (e.g., `"#FF6B35"` for orange)
  - Default: `"#FFFFFF"` (white) for dark theme, `"#000000"` (black) for light theme
- **`author_color`** (optional): Hex color code for author name text
  - Format: `"#RRGGBB"` (e.g., `"#4ECDC4"` for teal)
  - Default: `"#CCCCCC"` (light gray) for dark theme, `"#666666"` (dark gray) for light theme
- **Works with all themes**: Colors can be customized for dark, light, custom, or random themes

### Additional Parameters
- **`enable_triangle`** (optional): Control triangle overlay display
  - `True`: Force show triangle
  - `False`: Force hide triangle
  - `None`: Use theme default (default)

## 🤖 AI Title Optimization (Optional)

Fix mixed-language titles automatically with Google Gemini API:

```python
from youtube_thumbnail_generator import create_generator

# Method 1: Pass API key directly
generator = create_generator(gemini_api_key="your_gemini_api_key_here")

# Method 2: Set environment variable (recommended)
# export GEMINI_API_KEY="your_gemini_api_key_here"
generator = create_generator()  # Auto-detects from environment

# Optimization happens automatically during generation
result = generator.generate_final_thumbnail(title="Your title", ...)
```

**Examples:**
- ❌ "AI技术指南 Complete Guide" → ✅ "AI技术完整\n指南教程" (clean Chinese)
- ❌ "Learn Python编程" → ✅ "Learn Python\nProgramming\nComplete Guide" (clean English)

## ✨ What's New in v2.4.7

- 🚨 **CRITICAL BUG FIX**: Fixed AI title optimization import error
- 🤖 **AI Feature Working**: Google Gemini title optimization now properly detects installed packages
- ✅ **Correct Error Messages**: No more false "google-generativeai package not installed" warnings  
- 🔧 **Import Path Fixed**: Corrected relative import path for title_optimizer module

## What's New in v2.4.6

- 🎯 **Unified API Experience**: `create_generator()` now promoted as the recommended method
- 📚 **Improved Documentation**: Clear distinction between simple and advanced usage patterns
- 🚀 **Better User Experience**: Zero-configuration setup with `create_generator()` 
- 🔄 **Backward Compatibility**: `FinalThumbnailGenerator()` still available for advanced users

## What's New in v2.4.5

- 🚨 **CRITICAL FIX**: Fixed PyPI package structure - Python modules now properly included
- 📦 **Package Structure Fixed**: Users can now successfully import `from youtube_thumbnail_generator import FinalThumbnailGenerator`
- 🔧 **Proper Package Directory**: All Python files now correctly packaged in `youtube_thumbnail_generator/` directory
- ✅ **Import Issues Resolved**: Fixed the critical issue where users couldn't import the library after pip install

## What's New in v2.4.4

- 🔗 **Fixed PyPI Documentation Links**: All documentation links now work properly from both GitHub and PyPI
- 📖 **PyPI-Compatible README**: Removed external CDN images that caused broken image icons on PyPI
- 🎯 **Better User Navigation**: Clear links to GitHub-hosted documentation from any platform

## What's New in v2.4.3

- 🧠 **Smart Image Processing**: Intelligent resize and center-crop algorithm for perfect 900x900 thumbnails
- 📏 **Configurable Logo Size**: Logo size controlled by LOGO_SIZE constant (100x100px)  
- 🌐 **CDN-Hosted Examples**: All example images hosted on public CDN (dramatically reduced package size)
- 📖 **Simplified Documentation**: Removed duplicate guides, streamlined user experience
- ⚠️ **Logo Recommendations**: Clear guidance for square logo usage

**📋 [Complete Version History →](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/CHANGELOG.md)**

## 📖 Documentation

- **[Examples Gallery](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/EXAMPLES.md)** - All 24 template combinations with CDN-hosted examples
- **[API Documentation](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/README_API.md)** - Complete REST API reference  
- **[Version History](https://github.com/preangelleo/youtube-thumbnail-generator/blob/main/CHANGELOG.md)** - Detailed changelog and feature updates
- **[PyPI Package](https://pypi.org/project/youtube-thumbnail-generator/)** - Install via pip

## 🚨 Important Notes

### Logo Recommendations
- **Best Practice**: Provide square logos (1:1 aspect ratio) to prevent cropping
- **Processing**: All logos automatically converted to 100x100px
- **Non-square handling**: Center-cropped (may cut off important parts)

### Image Processing  
- **Any Input Size**: Accepts images of any dimensions
- **Smart Algorithm**: Auto scale-up if needed, then center-crop to 900x900
- **Quality**: High-quality Lanczos resampling for best results

### Language Support
- **Single Language Only**: Use either pure Chinese OR pure English titles
- **Mixed Language Issues**: May cause formatting problems due to different text processing rules

---

## 🎯 Best Practices

1. **Use square logos** (1:1 ratio) for optimal results
2. **Single language titles** for best formatting
3. **10-12 Chinese characters** or **7 English words** for optimal length
4. **High-resolution images** for better quality after processing

**Start creating professional YouTube thumbnails now!** 🎬✨

---

**Generated with YouTube Thumbnail Generator v2.4.8** 🚀