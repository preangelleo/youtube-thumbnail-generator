# API Documentation

## Base URL

```
http://localhost:5000
```

When running in Docker:
```
http://localhost:5000
```

## Authentication

No authentication required for basic endpoints. AI features require `GEMINI_API_KEY` environment variable.

## Endpoints

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ai_enabled": true
}
```

---

### Generate Thumbnail

**POST** `/generate`

Generate a single thumbnail with all customizable parameters.

**Request Body:**
```json
{
  "text": "Amazing Python Tutorial",
  "background_type": "gradient",
  "background_config": {
    "color1": "#667eea",
    "color2": "#764ba2",
    "direction": "diagonal"
  },
  "font_name": null,
  "font_size": 72,
  "font_color": "#FFFFFF",
  "text_position": "center",
  "enable_ai_optimization": true,
  "target_language": "en",
  "custom_prompt": null,
  "quality": 95,
  "format": "png",
  "return_base64": true
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Text to display on thumbnail |
| `background_type` | string | `"gradient"` | Type: `solid`, `gradient`, `image`, `pattern` |
| `background_config` | object | `{}` | Background configuration |
| `font_name` | string | `null` | Font name or path |
| `font_size` | integer | `72` | Font size in pixels |
| `font_color` | string | `"#FFFFFF"` | Text color (hex, rgb, or name) |
| `text_position` | string/array | `"center"` | Position: `center`, `top`, `bottom`, or `[x, y]` |
| `enable_ai_optimization` | boolean | `null` | Enable/disable AI optimization |
| `target_language` | string | `null` | Force language: `en`, `zh`, or `auto` |
| `custom_prompt` | string | `null` | Custom AI optimization prompt |
| `quality` | integer | `95` | Output quality (1-100) |
| `format` | string | `"png"` | Output format: `png` or `jpg` |
| `return_base64` | boolean | `true` | Return as base64 or file download |

**Response (base64):**
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "format": "png"
}
```

**Response (file):**
Binary image file with appropriate MIME type.

---

### Batch Generate

**POST** `/batch`

Generate multiple thumbnails with the same settings.

**Request Body:**
```json
{
  "texts": [
    "Tutorial Part 1",
    "Tutorial Part 2",
    "Tutorial Part 3"
  ],
  "background_type": "gradient",
  "enable_ai_optimization": false,
  "target_language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "thumbnails": [
    {
      "text": "Tutorial Part 1",
      "image": "data:image/png;base64,..."
    },
    {
      "text": "Tutorial Part 2",
      "image": "data:image/png;base64,..."
    },
    {
      "text": "Tutorial Part 3",
      "image": "data:image/png;base64,..."
    }
  ]
}
```

---

### Optimize Text

**POST** `/optimize-text`

Optimize text using AI (requires API key).

**Request Body:**
```json
{
  "text": "Python programming tutorial for beginners",
  "target_language": "en",
  "style": "engaging",
  "max_length": 50,
  "custom_prompt": null
}
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Original text to optimize |
| `target_language` | string | `"en"` | Target language: `en` or `zh` |
| `style` | string | `"engaging"` | Style: `engaging`, `professional`, `casual`, `dramatic` |
| `max_length` | integer | `50` | Maximum character length |
| `custom_prompt` | string | `null` | Custom optimization prompt |

**Response:**
```json
{
  "success": true,
  "original": "Python programming tutorial for beginners",
  "optimized": "Master Python NOW! 🚀 Beginner's Guide",
  "language": "en"
}
```

---

### Detect Language

**POST** `/detect-language`

Detect the language of text.

**Request Body:**
```json
{
  "text": "This is English text with some 中文 characters"
}
```

**Response:**
```json
{
  "success": true,
  "text": "This is English text with some 中文 characters",
  "language": "en",
  "language_name": "English"
}
```

---

### List Fonts

**GET** `/fonts`

List all available system fonts.

**Response:**
```json
{
  "success": true,
  "fonts": [
    "arial",
    "helvetica",
    "impact",
    "roboto",
    "montserrat"
  ]
}
```

## Background Configuration

### Solid Background
```json
{
  "background_type": "solid",
  "background_config": {
    "color": "#FF6B6B"
  }
}
```

### Gradient Background
```json
{
  "background_type": "gradient",
  "background_config": {
    "color1": "#667eea",
    "color2": "#764ba2",
    "direction": "diagonal"  // vertical, horizontal, diagonal
  }
}
```

### Image Background
```json
{
  "background_type": "image",
  "background_config": {
    "image_path": "/path/to/image.jpg",
    "blur": 5,
    "overlay_color": "#000000",
    "overlay_opacity": 0.3
  }
}
```

### Pattern Background
```json
{
  "background_type": "pattern",
  "background_config": {
    "pattern": "dots",  // dots, lines, grid, waves
    "color1": "#667eea",
    "color2": "#764ba2",
    "spacing": 50,
    "radius": 10  // for dots
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

### Common Error Codes

- `400` - Bad Request (missing or invalid parameters)
- `413` - File too large (max 16MB)
- `404` - Endpoint not found
- `500` - Internal server error

## Examples

### cURL Examples

**Basic thumbnail:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing Tutorial"}'
```

**With AI optimization:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python Tutorial",
    "enable_ai_optimization": true,
    "target_language": "en"
  }'
```

**Batch generation:**
```bash
curl -X POST http://localhost:5000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Part 1", "Part 2", "Part 3"],
    "background_type": "gradient"
  }'
```

### Python Examples

```python
import requests
import json

# Generate thumbnail
response = requests.post(
    "http://localhost:5000/generate",
    json={
        "text": "Amazing Python Tutorial",
        "enable_ai_optimization": True,
        "target_language": "en",
        "font_size": 80
    }
)

data = response.json()
if data["success"]:
    # Save base64 image
    import base64
    image_data = data["image"].split(",")[1]
    with open("thumbnail.png", "wb") as f:
        f.write(base64.b64decode(image_data))
```

### JavaScript Examples

```javascript
// Generate thumbnail
fetch('http://localhost:5000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Amazing Tutorial',
    enable_ai_optimization: true,
    target_language: 'en'
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    // Display image
    const img = document.createElement('img');
    img.src = data.image;
    document.body.appendChild(img);
  }
});
```

## Rate Limiting

When using AI features:
- Gemini API has rate limits
- Add delays between requests for batch processing
- Consider caching optimized text

## Docker Deployment

```bash
# Run with environment variables
docker run -p 5000:5000 \
  -e GEMINI_API_KEY=your-api-key \
  -e ENABLE_AI_OPTIMIZATION=true \
  -e DEFAULT_LANGUAGE=en \
  preangelleo/youtube-thumbnail-generator
```