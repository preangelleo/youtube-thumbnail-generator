# YouTube Thumbnail Generator 🎨

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-green)](https://www.docker.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-Optional-purple)](https://ai.google.dev/)

A powerful YouTube thumbnail generator with optional AI text optimization and multi-language support. Create eye-catching thumbnails with customizable backgrounds, fonts, and AI-enhanced text.

## ✨ Features

- **Customizable Backgrounds**: Solid colors, gradients, or image backgrounds
- **Multiple Font Support**: Various fonts and styles
- **AI Text Optimization**: Optional Gemini AI integration for better text
- **Multi-Language Support**: Automatic language detection or manual specification
- **Flexible Layouts**: Multiple text positions and sizes
- **High Quality Output**: 1280x720 HD thumbnails
- **Docker Support**: Easy deployment with Docker

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/preangelleo/youtube-thumbnail-generator.git
cd youtube-thumbnail-generator

# Install dependencies
pip install -r requirements.txt

# Or install from PyPI
pip install youtube-thumbnail-generator
```

### Basic Usage

#### Python Library

```python
from src.thumbnail_generator import ThumbnailGenerator

# Create generator instance
generator = ThumbnailGenerator()

# Generate a simple thumbnail
thumbnail = generator.generate(
    text="Amazing Python Tutorial",
    output_path="thumbnail.png"
)
```

#### CLI Usage

```bash
# Basic thumbnail
youtube-thumbnail "Amazing Python Tutorial" -o thumbnail.png

# With AI optimization
youtube-thumbnail "Python Tutorial" --enable-ai --language en

# Custom styling
youtube-thumbnail "Tutorial" --font-size 100 --bg-color1 "#FF0000"
```

#### REST API

```bash
# Start the API server
python -m src.api

# Generate thumbnail via API
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing Tutorial",
    "enable_ai_optimization": true,
    "target_language": "en"
  }'
```

### With AI Optimization

```python
# Enable AI optimization with explicit control
generator = ThumbnailGenerator(
    gemini_api_key="your-api-key",
    enable_ai_optimization=True  # Explicit toggle
)

# Generate with forced language
thumbnail = generator.generate(
    text="Python Tutorial for Beginners",
    target_language="en",  # Force English
    enable_ai_optimization=True,  # Override default
    output_path="ai_thumbnail.png"
)
```

## 📚 Documentation

For detailed documentation, see [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)

For usage examples, see [examples/example_usage.py](examples/example_usage.py)

## 🐳 Docker

```bash
# Pull from Docker Hub
docker pull preangelleo/youtube-thumbnail-generator:latest

# Run the API server
docker run -p 5000:5000 \
  -e GEMINI_API_KEY=your-key \
  -e ENABLE_AI_OPTIMIZATION=true \
  preangelleo/youtube-thumbnail-generator

# Or build locally
docker build -t youtube-thumbnail-generator .
docker run -p 5000:5000 youtube-thumbnail-generator
```

## 🌐 API Endpoints

### POST /generate
Generate a single thumbnail with full parameter control.

```json
{
  "text": "Amazing Tutorial",
  "enable_ai_optimization": true,
  "target_language": "en",
  "background_type": "gradient",
  "font_size": 80
}
```

### POST /batch
Generate multiple thumbnails in one request.

```json
{
  "texts": ["Tutorial 1", "Tutorial 2"],
  "enable_ai_optimization": false,
  "target_language": "zh"
}
```

### POST /optimize-text
Optimize text using AI (requires API key).

```json
{
  "text": "Basic Python Tutorial",
  "target_language": "en",
  "style": "engaging"
}
```

### POST /detect-language
Detect the language of text.

```json
{
  "text": "Python编程教程"
}
```

## 🔧 Configuration

Create a `.env` file:

```env
# Optional: Gemini AI API Key
GEMINI_API_KEY=your-api-key-here

# Optional: Enable AI by default
ENABLE_AI_OPTIMIZATION=true

# Optional: Default language
DEFAULT_LANGUAGE=en
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📧 Support

For issues and questions, please use the [GitHub Issues](https://github.com/preangelleo/youtube-thumbnail-generator/issues) page.