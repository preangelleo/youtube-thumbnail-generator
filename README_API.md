# YouTube Thumbnail Generator v2.4.3 - API Documentation

**Author**: Leo Wang (https://leowang.net)

## 🚀 Quick Start

### Start Service
```bash
python api_server.py
```
Service will start at `http://localhost:5002`

## 📡 API Endpoints

### 1. Generate Enhanced Thumbnail
**Endpoint**: `POST /api/generate/enhanced`

**Function**: Generate fully customizable YouTube thumbnails with all v2.3.0 features including enhanced Chinese Bold fonts and AI optimization

### 2. Generate Random Thumbnail (New!)
**Endpoint**: `POST /api/generate/random`

**Function**: Generate thumbnails with random selection from 12 template combinations (Dark/Light × Triangle/NoTriangle × Standard/Flip × Direction)

### 3. Generate Chapter Image
**Endpoint**: `POST /api/generate/chapter`

**Function**: Generate text-overlaid Chapter images, supports Chinese/English

#### Request Parameters (Enhanced Thumbnail)
```json
{
    // Required Parameters
    "title": "AI智能视频生成技术",                    // Required: Main title (supports Chinese/English)
    
    // Basic Parameters
    "author": "leowang.net",                     // Optional: Author name
    "logo_path": "logos/my_logo.png",            // Optional: Logo file path
    "right_image_path": "assets/video_frame.jpg", // Optional: Right-side image path
    
    // Theme & Layout Parameters
    "theme": "dark",                             // Optional: "dark", "light", or "custom" (default: "dark")
    "custom_template": "my_background.png",      // Optional: Custom background (when theme="custom")
    "flip": false,                               // Optional: Flip layout (default: false)
    
    // Triangle Parameters
    "enable_triangle": true,                     // Optional: Enable triangle overlay (default: true)
    "triangle_direction": "top",                 // Optional: "top" or "bottom" (default: "top")
    
    // Color Parameters
    "title_color": "#FFFFFF",                    // Optional: Title text color (hex format)
    "author_color": "#CCCCCC",                   // Optional: Author text color (hex format)
    
    // AI & Output Parameters
    "google_api_key": "your_gemini_api_key",     // Optional: Google Gemini API key for title optimization
    "youtube_ready": true                        // Optional: YouTube API compliance (default: true)
}
```

#### Request Parameters (Random Thumbnail)
```json
{
    // Required Parameters
    "title": "AI智能视频生成技术",                    // Required: Main title
    
    // Basic Parameters (same as enhanced)
    "author": "leowang.net",                     // Optional: Author name
    "logo_path": "logos/my_logo.png",            // Optional: Logo file path
    "right_image_path": "assets/video_frame.jpg", // Optional: Right-side image path
    "google_api_key": "your_gemini_api_key",     // Optional: Google Gemini API key for title optimization
    "youtube_ready": true                        // Optional: YouTube API compliance (default: true)
    
    // Note: theme, flip, enable_triangle, triangle_direction are randomly selected from 12 combinations
}
```

#### v2.3.0 Smart Features
- 🎨 **Enhanced Chinese Bold Rendering**: STHeiti Medium priority + intelligent stroke effects for perfect Bold display
- 🧠 **Smart Stroke Colors**: RGB(128,128,128) for white text, RGB(192,192,192) for black text based on brightness detection
- 🔤 **Auto-Enable Stroke**: Chinese fonts ≥30px automatically enable stroke effects
- 🤖 **AI Title Optimization**: Google Gemini-powered mixed-language title optimization with smart line-breaking
- 🎲 **12 Template Combinations**: Dark/Light × Triangle(On/Off) × Direction(Top/Bottom) × Layout(Standard/Flip)
- 🎯 **Intelligent Text Processing**: Auto Chinese/English detection with optimized fonts and processing
- 📐 **Smart Line-breaking**: AI-driven or rule-based line-breaking for optimal readability
- 🎨 **Triangle Effects**: Integrated overlays with customizable direction and colors
- 📱 **YouTube API Ready**: Automatic optimization for YouTube thumbnail upload compliance
- 🔧 **Unique Filenames**: Each task generates independent files to avoid conflicts

#### Response Example (Enhanced)
```json
{
    "task_id": "377f7bc3-b896-44ca-a501-b79308cc059d",
    "status": "processing", 
    "message": "缩略图生成任务已启动"
}
```

#### Response Example (Random)  
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "processing",
    "message": "随机缩略图生成任务已启动，将从12种组合中随机选择"
}
```

#### Request Parameters (Chapter)
```json
{
    "text": "This is an important quote",                    // Required: Text to add
    "image_path": "assets/background.jpg",       // Optional: Background image path
    "font_size": 86,                            // Optional: Font size
    "language": "chinese",                      // Optional: Language (chinese/english)
    "width": 1600,                              // Optional: Image width, default 1600
    "height": 900                               // Optional: Image height, default 900
}
```

#### Response Example (Chapter)
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "processing",
    "message": "Chapter图片生成任务已启动"
}
```

## 📋 12 Random Template Combinations

When using `/api/generate/random`, the system randomly selects from these combinations:

| ID | Theme | Triangle | Direction | Layout | Description |
|----|--------|----------|-----------|---------|-------------|
| 1  | Dark   | ON       | Top ▲     | Standard | Dark + Triangle ON (top ▲) + Standard |
| 2  | Dark   | ON       | Top ▲     | Flip     | Dark + Triangle ON (top ▲) + Flip |
| 3  | Dark   | ON       | Bottom ▼  | Standard | Dark + Triangle ON (bottom ▼) + Standard |
| 4  | Dark   | ON       | Bottom ▼  | Flip     | Dark + Triangle ON (bottom ▼) + Flip |
| 5  | Light  | ON       | Top ▲     | Standard | Light + Triangle ON (top ▲) + Standard |
| 6  | Light  | ON       | Top ▲     | Flip     | Light + Triangle ON (top ▲) + Flip |
| 7  | Light  | ON       | Bottom ▼  | Standard | Light + Triangle ON (bottom ▼) + Standard |
| 8  | Light  | ON       | Bottom ▼  | Flip     | Light + Triangle ON (bottom ▼) + Flip |
| 9  | Dark   | OFF      | -         | Standard | Dark + Triangle OFF + Standard |
| 10 | Dark   | OFF      | -         | Flip     | Dark + Triangle OFF + Flip |
| 11 | Light  | OFF      | -         | Standard | Light + Triangle OFF + Standard |
| 12 | Light  | OFF      | -         | Flip     | Light + Triangle OFF + Flip |

### 2. Check Task Status
**Endpoint**: `GET /api/status/<task_id>`

#### Response Example - Processing
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "processing",
    "progress": "Generating..."
}
```

#### Response Example - Completed
```json
{
    "task_id": "377f7bc3-b896-44ca-a501-b79308cc059d",
    "status": "completed",
    "result_file": "thumbnail_377f7bc3.jpg",
    "download_url": "/api/download/thumbnail_377f7bc3.jpg",
    "generation_time": "0.12s"
}
```

#### Response Example - Failed
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "failed",
    "error": "Template file not found: templates/professional_template.jpg"
}
```

### 3. Download Generated File
**Endpoint**: `GET /api/download/<filename>`

Directly download the generated thumbnail file.

### 4. Health Check
**Endpoint**: `GET /api/health`

#### Response Example
```json
{
    "status": "healthy",
    "timestamp": "2025-08-08T17:30:00Z",
    "version": "1.0"
}
```

### 5. Get Template List
**Endpoint**: `GET /api/templates`

#### Response Example
```json
{
    "templates": [
        {
            "name": "professional_template.jpg",
            "size": "1600x900",
            "description": "Professional template"
        }
    ]
}
```

### 6. Get Asset List  
**Endpoint**: `GET /api/assets`

#### Response Example
```json
{
    "logos": ["animagent_logo.png"],
    "images": ["testing_image.jpeg"]
}
```

## 🔧 Usage Examples

### Python Example

#### Generate Thumbnail (Complete Example)
```python
import requests
import time
import json

# 1. Send Chinese thumbnail generation request (demonstrate smart line-breaking)
response = requests.post('http://localhost:5002/api/generate/enhanced', 
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "title": "Ultimate Complete Guide to AI Technology Revolution",        # 14 chars, triggers 9-char line-break
        "subtitle": None,                            # null triggers title centering
        "author": "Leo Wang",
        "logo_path": "logos/animagent_logo.png",
        "right_image_path": "assets/testing_image.jpeg"
    })
)

task_data = response.json()
task_id = task_data['task_id']

# 2. Poll task status
while True:
    status_response = requests.get(f'http://localhost:5002/api/status/{task_id}')
    status_data = status_response.json()
    
    if status_data['status'] == 'completed':
        print(f"Generation complete! Download link: {status_data['download_url']}")
        break
    elif status_data['status'] == 'failed':
        print(f"Generation failed: {status_data['error']}")
        break
    else:
        print("Generating...")
        time.sleep(1)

# 3. Download file
if status_data['status'] == 'completed':
    file_response = requests.get(f"http://localhost:5002{status_data['download_url']}")
    with open('downloaded_thumbnail.jpg', 'wb') as f:
        f.write(file_response.content)
    print(f"File downloaded: downloaded_thumbnail.jpg")
```

### cURL Examples

#### Quick Test Thumbnail Generation
```bash
# 1. Start service
python api_server.py &

# 2. Test health status
curl http://localhost:5002/api/health

# 3. Send generation request (Chinese smart line-breaking example)
curl -X POST http://localhost:5002/api/generate/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ultimate Complete Guide to AI Technology Revolution",
    "subtitle": null,
    "author": "Leo Wang",
    "logo_path": "logos/animagent_logo.png",
    "right_image_path": "assets/testing_image.jpeg"
  }'

# 4. Check task status (use returned task_id)
curl http://localhost:5002/api/status/377f7bc3-b896-44ca-a501-b79308cc059d

# 5. Download result file
curl -O http://localhost:5002/api/download/thumbnail_377f7bc3.jpg
```

#### Generate Chapter Image
```python
import requests
import json

# Generate Chapter image
response = requests.post('http://localhost:5002/api/generate/chapter',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "text": "AI Will Change the World",
        "language": "english",
        "font_size": 86,
        "width": 1600,
        "height": 900
    })
)

task_data = response.json()
print(f"Chapter task ID: {task_data['task_id']}")
```

## 🎯 v2.1 Update Highlights

### Parameter Compatibility Optimization
- **Unique Filenames**: `thumbnail_{task_id}.jpg` format, avoid inter-task conflicts
- **Smart Subtitle Handling**: Empty strings auto-convert to null, trigger title centering
- **Complete Error Handling**: Detailed task status and error information

### Performance Improvements  
- **Fast Generation**: Average 0.12s generation time
- **Concurrent Support**: Multi-task parallel processing
- **Memory Optimization**: Efficient image processing pipeline

## 🔍 Troubleshooting

### Common Issues
1. **Port Occupied**: `lsof -ti:5002 | xargs kill -9` to clear port
2. **File Not Found**: Ensure logo and image paths are correct
3. **Task Failed**: Check `/api/status/{task_id}` error field

### Technical Support
- Check `example_usage.py` for direct function call methods
- Check `README.md` for complete feature description

# Generate English Chapter
curl -X POST http://localhost:5002/api/generate/chapter \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The Future of Technology",
    "language": "english",
    "image_path": "assets/testing_image.jpeg"
  }'
```

## ⚠️ Important Notes

### File Path Rules
- All paths are relative to API service root directory
- Logo files go in `logos/` directory
- Image files go in `assets/` directory  
- Generated results saved in `outputs/` directory

### Output File Naming
- Current version uses unique naming: `thumbnail_{task_id}.jpg` or `chapter_{task_id}.jpg`
- This prevents conflicts between concurrent tasks
- Files are kept until manually deleted

### Processing Logic
1. **Auto Image Processing**: Right-side images auto-convert to square and scale to 900x900
2. **Auto Font Selection**: Automatically choose optimal fonts based on text language
3. **Auto Text Wrapping**: Auto line-break when text exceeds width limits
4. **Auto Logo Scaling**: Maintain aspect ratio to fit logo area

## 🚨 Error Code Reference

| Status Code | Meaning | Suggested Action |
|--------|------|----------|
| 200 | Success | - |
| 400 | Parameter Error | Check request JSON format and required parameters |
| 404 | File Not Found | Check if file paths are correct |
| 500 | Internal Server Error | Check service logs, possibly font or template file issues |