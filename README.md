# YouTube Thumbnail Generator v2.4.4

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

### 1. Simple Python Usage
```python
from youtube_thumbnail_generator import FinalThumbnailGenerator

# Create generator with default template
generator = FinalThumbnailGenerator()

# Generate YouTube-ready thumbnail (1280x720, <2MB, optimized for API upload)
result = generator.generate_final_thumbnail(
    title="Complete AI Technology Guide",
    author="Leo Wang",
    logo_path="logos/your_logo.png",     # ⚠️ Use square logo (1:1 ratio) for best results
    right_image_path="assets/image.jpg", # Any size - auto-processed to 900x900
    output_path="outputs/thumbnail.jpg"
)
```

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

## 🤖 AI Title Optimization (Optional)

Fix mixed-language titles automatically with Google Gemini API:

```bash
# Set environment variable
export GOOGLE_API_KEY="your_google_api_key_here"

# Use normally - optimization happens automatically
python your_script.py
```

**Examples:**
- ❌ "AI技术指南 Complete Guide" → ✅ "AI技术完整\n指南教程" (clean Chinese)
- ❌ "Learn Python编程" → ✅ "Learn Python\nProgramming\nComplete Guide" (clean English)

## ✨ What's New in v2.4.4

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

**Generated with YouTube Thumbnail Generator v2.4.3** 🚀