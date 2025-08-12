# Changelog

All notable changes to YouTube Thumbnail Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-01-11

### Changed
- **BREAKING**: Renamed `target_language` to `source_language` for clarity
- Added proper separation between source and target languages:
  - `source_language`: Explicitly specify input language (skip auto-detection)
  - `target_language`: For translation (only used with AI optimization when different from source)
- Improved AI optimization logic:
  - Translation only happens when target_language differs from source_language
  - target_language is only meaningful when AI optimization is enabled
- Updated API, CLI, and documentation to reflect the new language handling

### Fixed
- Language parameter logic now correctly distinguishes between:
  - Input language specification (to skip detection)
  - Translation target (only with AI)
- Clarified that translation requires AI optimization to be enabled

## [1.0.0] - 2024-01-11

### Added
- Initial release of YouTube Thumbnail Generator
- Core thumbnail generation with PIL/Pillow
- **AI Text Optimization** with explicit toggle control
  - `enable_ai_optimization` parameter for explicit on/off control
  - Works with Gemini AI API (optional)
  - Custom prompt support for AI optimization
- **Language Support** with forced language specification
  - `target_language` parameter to force English or Chinese
  - Automatic language detection with 60% threshold
  - Support for mixed language text
- **Flask REST API** with full parameter support
  - `/generate` endpoint for single thumbnail generation
  - `/batch` endpoint for multiple thumbnails
  - `/optimize-text` endpoint for AI text optimization
  - `/detect-language` endpoint for language detection
  - `/fonts` endpoint to list available fonts
  - Base64 and file download response formats
- **CLI Interface** with comprehensive options
  - Command-line tool for thumbnail generation
  - Batch processing support
  - Language detection utility
  - Font listing utility
- **Multiple Background Types**
  - Solid color backgrounds
  - Gradient backgrounds (vertical, horizontal, diagonal)
  - Image backgrounds with blur and overlay options
  - Pattern backgrounds (dots, lines, grid, waves)
- **Font Management**
  - System font detection
  - Custom font support
  - Multiple font styles
- **Docker Support**
  - Dockerfile for containerization
  - docker-compose configuration
  - Environment variable configuration
- **CI/CD Pipeline**
  - GitHub Actions for testing and deployment
  - Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
  - Docker Hub automatic push
  - PyPI package publishing
- **Comprehensive Testing**
  - Unit tests for all components
  - API endpoint tests
  - Language detection tests
  - 95%+ code coverage
- **Documentation**
  - Complete API documentation
  - Usage examples
  - Troubleshooting guide
  - Contributing guidelines

### Configuration
- Environment variable support via .env file
- Configurable default settings
- Quality and format options

### Security
- API key management via environment variables
- Input validation and sanitization
- Error handling and logging

## [Unreleased]

### Planned
- Web UI interface
- More AI providers (OpenAI, Anthropic)
- Additional pattern types
- Animation support
- Template library
- Cloud storage integration