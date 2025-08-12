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
```

### Basic Usage

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

### With AI Optimization

```python
# Enable AI optimization
generator = ThumbnailGenerator(
    gemini_api_key="your-api-key",
    enable_ai_optimization=True
)

# Generate with AI-enhanced text
thumbnail = generator.generate(
    text="Python Tutorial for Beginners",
    target_language="en",  # Force English
    output_path="ai_thumbnail.png"
)
```

## 📚 Documentation

For detailed documentation, see [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)

For usage examples, see [examples/example_usage.py](examples/example_usage.py)

## 🐳 Docker

```bash
# Build the image
docker build -t youtube-thumbnail-generator .

# Run the container
docker run -v $(pwd)/output:/app/output youtube-thumbnail-generator
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