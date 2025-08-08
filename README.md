# YouTube Thumbnail Generator v2.1

Professional YouTube thumbnail automatic generation tool with intelligent Chinese/English text layout, logo, and precise image control with dynamic adaptation.

**Author**: Leo Wang (https://leowang.net)

## 📋 Core Features

- ✅ **Intelligent Chinese/English System**: PNG overlay technology, perfect Chinese/English text mixing
- ✅ **Smart Line-breaking Algorithm**: Chinese 9/20 character limits, English 3-line truncation  
- ✅ **Font Differentiation Optimization**: Chinese fonts 30% larger, subtitle height increased by 20%
- ✅ **Professional Visual Effects**: Triangle transition integrated into images, text always on top layer
- ✅ **Intelligent Image Processing**: Auto square conversion + 900x900 filling
- ✅ **Multi-endpoint API Support**: Flask RESTful API + Chapter functionality
- ✅ **Smart Font Selection**: Chinese PingFang/Founder, English Lexend Bold

## 🎨 Template Showcase

### Professional Template - Currently the Only Template

**Canvas Size**: 1600x900 pixels

**Effect Showcase**:

#### Chinese Sample
![Chinese Thumbnail Sample](template_samples/chinese_sample_template_1.jpg)

#### English Sample  
![English Thumbnail Sample](template_samples/english_sample_template_1.jpg)

**5 Supported Input Parameters**:
1. **title** - Main title text (required)
2. **subtitle** - Subtitle text (optional)  
3. **author** - Author name (optional, auto-capitalized)
4. **logo_path** - Logo file path (optional)
5. **right_image_path** - Right-side image path (optional)

**Color Configuration** (currently fixed, no custom colors yet):
- Title: White #FFFFFF
- Subtitle: Light yellow #FFEB9C  
- Author: Light gray #CCCCCC
- Background: Pure black #000000

**Layout Zones**:
- **Left Text Area**: 700x900 pixels - Black background, text display
- **Right Image Area**: 900x900 pixels - Square image filling  
- **Triangle Transition**: 200x900 pixels - Elegant diagonal separation effect

> **Future Plans**: We will add more template styles and custom color options!

## 🧠 Intelligent Text System

### Core Technology: PNG Overlay + Triangle Integration
Instead of drawing text directly on template:
1. **Independent Rendering**: Generate transparent PNG text images first
2. **Smart Adjustment**: Dynamically adjust PNG size based on text length
3. **Triangle Integration**: Paste triangle to right-side image first, then paste combined image to template
4. **Text Overlay**: PNG text pasted last, ensuring it's always on the top layer

### Chinese/English Differentiated Processing
#### Chinese Optimization
- **Font Enlargement**: 30% larger than English (54px vs 42px title, 26px vs 20px subtitle)
- **Subtitle Height Increase**: 20% taller than English (36px vs 30px)
- **Smart Line-breaking**: 
  - Title: Break after 9 characters, divide by 2, odd characters go to second line
  - Subtitle: Break after 20 characters, divide by 2
- **Line Spacing**: Title 16px, subtitle 8px

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
- **Font**: 45px Helvetica, white #FFFFFF
- **Effects**: Black stroke + shadow, professional visual
- **Position**: Starting at (50, 280), actual height dynamically adjusted

### Optional Parameters

**`subtitle`** (str) - Subtitle
```python
subtitle="Everything You Need to Know About Modern Technology"
```
- **Smart Adaptation**: 1 line=30px, 2 lines=68px, 3 lines=106px height
- **Font**: 20px Helvetica, light yellow #FFEB9C  
- **Position**: 20px spacing below title, auto-calculate Y coordinate
- **Truncation Rule**: Auto-add ellipsis if exceeds 3 lines

**`author`** (str) - Author name
```python
author="Leo Wang"  # Auto-converts to "LEO WANG"
```
- **Format**: Auto-convert to uppercase
- **Position**: Fixed bottom (50, 860)
- **Font**: 36px Lexend Bold, light gray #CCCCCC

**`logo_path`** (str) - Logo file path
```python
logo_path="logos/your_logo.png"
```
- **Position**: Top-left corner (50, 50), left margin = top margin
- **Area**: 240x150 pixels, auto aspect ratio scaling
- **Format**: Supports PNG/JPG, auto-handle transparency

**`right_image_path`** (str) - Right-side image path
```python
right_image_path="assets/your_image.jpg"
```
- **Smart Cropping**: Auto-convert to square (center crop)
- **Fill Method**: Scale to 900x900 pixels to fill right side
- **Position**: Right area starting at (700, 0)

## 📦 Installation Methods

### Method 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/preangelleo/youtube-thumbnail-generator.git
```

### Method 2: Local Development Install
```bash
git clone https://github.com/preangelleo/youtube-thumbnail-generator.git
cd youtube-thumbnail-generator
pip install -e .
```

### Method 3: Core Functions Only
```bash
pip install git+https://github.com/preangelleo/youtube-thumbnail-generator.git
```

### Method 4: Include API Service
```bash
pip install "git+https://github.com/preangelleo/youtube-thumbnail-generator.git[api]"
```

## 🚀 Usage Methods

### 1. Use as Python Library
```python
from youtube_thumbnail_generator import FinalThumbnailGenerator

# Initialize generator (using included template)
generator = FinalThumbnailGenerator("templates/professional_template.jpg")

# Generate thumbnail (all parameter example)
result = generator.generate_final_thumbnail(
    title="The Ultimate Complete Guide to Advanced AI Technology Revolution and Future Gaming Setup Reviews 2025",
    subtitle="Everything You Need to Know About Modern Technology and Future Developments",
    author="Leo Wang",
    logo_path="logos/animagent_logo.png",
    right_image_path="assets/testing_image.jpeg",
    output_path="outputs/final_test.jpg"
)

print(f"Generation complete: {result}")
```

### 2. Command Line API Service
Launch API directly after installation:

```bash
# Start API service directly
youtube-thumbnail-api

# Or use Python module method
python -m youtube_thumbnail_generator.api_server
```

### 3. Use in Other Python Projects
```python
# In your Python projects
from youtube_thumbnail_generator import FinalThumbnailGenerator, create_text_png

# Quick thumbnail generation
generator = FinalThumbnailGenerator("path/to/your/template.jpg")
result = generator.generate_final_thumbnail(
    title="Your Video Title",
    subtitle="Subtitle",
    output_path="output/thumbnail.jpg"
)

# Or generate text PNG only
success, text_img, height = create_text_png(
    text="Test Text",
    width=600,
    height=200,
    language="chinese"
)
```

### 4. API Service Calls

#### Generate Thumbnail
```bash
curl -X POST http://localhost:5002/api/generate/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Tech Reviews 2025",
    "subtitle": "The Future is Now",
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

### 3. Python API Client Example
```python
import requests
import time
import json

def generate_thumbnail_api(title, subtitle=None, author=None, logo_path=None, image_path=None):
    """Generate thumbnail using API"""
    
    # 1. Send generation request
    response = requests.post('http://localhost:5002/api/generate/enhanced', 
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "title": title,
            "subtitle": subtitle,
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
    subtitle="Quick Summary of the Content", 
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
  "subtitle": "Optional - Subtitle text", 
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
→ 1 line, 55px height
Subtitle: "Daily Updates"
→ 1 line, 30px height
Compact layout, professional appearance
```

### Long Title Effect  
```
Title: "The Ultimate Complete Guide to Advanced AI Technology..."
→ 5 lines, 307px height (5×55px + 4×8px line spacing)
Subtitle: "Everything You Need to Know About Modern Technology"  
→ 2 lines, 68px height (2×30px + 1×8px line spacing)
Auto-adjust positions, perfect fit
```

### Overlong Content Handling
```
Subtitle exceeds 3 lines → Auto-truncate to "Very long subtitle text that goes on and on..."
Ensure stable layout, prevent content overflow
```

## 🔧 Advanced Configuration

### File Path Rules
- **Relative Paths**: Relative to project root directory
- **Logo Directory**: `logos/` - Store all logo files
- **Assets Directory**: `assets/` - Store background images
- **Output Directory**: `outputs/` - Generated results storage
- **Template Directory**: `templates/` - Template file storage

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
├── youtube_thumbnail_generator/
│   ├── __init__.py                   # Package initialization
│   ├── final_thumbnail_generator.py  # Core generator
│   ├── text_png_generator.py         # PNG text renderer  
│   ├── api_server.py                 # Flask API service
│   └── function_add_chapter.py       # Chapter functionality
├── templates/
│   ├── professional_template.jpg     # 1600x900 professional template
│   └── triangle_template.png         # 200x900 triangle transition
├── template_samples/                 # Template showcase samples
├── setup.py                          # Package setup
├── pyproject.toml                    # Modern Python packaging
├── README.md                         # Project documentation
└── README_API.md                     # Detailed API documentation
```

## 📈 Version History

### v2.1 (Current) - Smart Layout Revolution
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

## 🎯 Best Practices

### Title Text Suggestions
- **Length**: Recommend 50-100 characters, system auto-optimizes display
- **Content**: Clearly express video theme, attract viewer clicks
- **Keywords**: Front-load important keywords, improve search results

### Subtitle Usage Tips
- **Positioning**: Supplementary explanation or emphasis points
- **Length**: Recommend 20-60 characters, auto-handle if exceeded
- **Style**: Create hierarchical contrast with main title

### Image Selection Principles
- **Size**: Any size, system auto-converts to square
- **Content**: Choose visually impactful images
- **Quality**: Recommend high resolution, ensure clarity after scaling

## 🚨 Important Notes

1. **File Paths**: Ensure all file paths are correct and files exist
2. **Font Dependencies**: System will auto-downgrade to available fonts
3. **Output Overwrite**: Default output `final_test.jpg`, will overwrite same-name files
4. **API Async**: API uses async processing, need to poll status
5. **Memory Usage**: Large image processing may use significant memory

---

## 💡 Quick Start

1. **Install Dependencies**: `pip install git+https://github.com/preangelleo/youtube-thumbnail-generator.git`
2. **Prepare Assets**: Put logos and images in corresponding directories
3. **Direct Test**: 
   ```python
   from youtube_thumbnail_generator import FinalThumbnailGenerator
   generator = FinalThumbnailGenerator("templates/professional_template.jpg")
   generator.generate_final_thumbnail(title="Test Title", output_path="test.jpg")
   ```
4. **API Service**: `youtube-thumbnail-api`
5. **Check Result**: Look at generated file

Start creating professional YouTube thumbnails now! 🎬✨