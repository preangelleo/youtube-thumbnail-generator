# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.6] - 2025-08-09

### 🔧 Critical Font & Layout Fixes
- **Fixed Font Sizing**: Restored proper 45px base font size for titles (was too small with 9.6% ratio)
- **Fixed Left Alignment**: Restored 20px fixed left margin system (was incorrectly center-aligned)
- **Enhanced Chinese Fonts**: Restored 30% font size boost for Chinese text readability
- **Dynamic Font Scaling**: Added English dynamic scaling (<7 words get enlarged, like Chinese <9 chars)
- **Improved Font Priority**: English now uses Lexend Bold > Arial Bold > Helvetica fallback chain
- **Smart Line Breaking**: Restored complete intelligent line-breaking algorithms for both languages
- **3-Line Truncation**: Fixed English title truncation with smart ellipsis handling
- **Auto Font Scaling**: Restored automatic font scaling when text is too tall for container

### 🐛 Bug Fixes
- Fixed regression from commit 2af732b where universal font detection broke layout
- Fixed English fonts defaulting to small Helvetica instead of bold fonts
- Fixed missing Chinese font enlargement and dynamic scaling features
- Fixed text positioning from center-aligned back to professional left-aligned layout
- Added comprehensive debug logging for font loading troubleshooting

### ✅ Testing
- Comprehensive testing with 4 complete scenarios: Chinese 16 chars + English 7 words in dark/light themes
- All features tested with logo, right image, triangle effects, and YouTube API compliance
- Verified 1280x720 output, <2MB file size, sRGB color space compatibility

## [2.2.2] - 2025-08-08

### 🎯 User Experience Enhancement
- **YouTube-Ready by Default**: `youtube_ready=True` is now the default behavior
- **Seamless Output**: Users get YouTube API compliant thumbnails without extra steps
- **Clean File Naming**: Optimized thumbnails use the original filename (no `_youtube_ready` suffix)
- **Perfect Integration**: YouTube optimization happens transparently in the background

### 🔧 Technical Improvements
- Enhanced file handling for YouTube optimization process
- Improved temporary file management
- Streamlined user experience for direct YouTube API uploads

### 📚 Documentation Updates
- Updated all examples to reflect YouTube-ready defaults
- Clarified high-resolution mode usage (`youtube_ready=False`)
- Enhanced code examples with complete thumbnail generation

## [2.2.1] - 2025-08-08

### 🔧 Critical Fix
- **Package Resource Resolution**: Fixed template path resolution for PyPI installed packages
- **Smart Fallback System**: Auto-generate templates if bundled files cannot be found
- **Cross-Platform Compatibility**: Improved path resolution across different Python environments

### 🚀 YouTube API v3 Integration
- `optimize_for_youtube_api()`: Convert any thumbnail to YouTube API v3 compliant format
- `youtube_ready` parameter: Built-in YouTube optimization during generation
- **Perfect Compliance**: 1280x720 JPEG, sRGB, <2MB, baseline encoding
- **Smart Quality Control**: Multi-level compression testing (95→90→85→80→75→70)

### 🛠️ New Functions
- `init_templates()`: Manually create default templates in project directory
- `get_resource_path()`: Robust resource file path resolution with fallbacks
- **Automatic Template Creation**: Templates auto-generate in user's directory if missing

### 📚 Documentation Updates
- Added manual template creation guide
- Updated all code examples to use `get_default_template()`
- Enhanced installation instructions with fallback system explanation

## [2.2.0] - 2025-08-08

### 🎉 Major Features Added
- **Three Theme Architecture**: Complete theme system with Dark, Light, and Custom modes
- **Full Color Customization**: Added `title_color` and `author_color` parameters with hex color support
- **Triangle Control System**: New `enable_triangle` parameter to control overlay effects
- **Custom Background Support**: `custom_template` parameter for user-provided 1600x900 backgrounds
- **Dynamic Font Scaling**: Auto font size adjustment based on text length (1-17 characters)
- **Smart Theme Defaults**: Automatic color configuration per theme mode

### 🎨 Theme Modes
- **Dark Theme**: Black background + White text + Black triangle (default)
- **Light Theme**: White background + Black text + White triangle
- **Custom Theme**: User background + Custom colors + Optional triangle

### 📦 Template Assets Added
- 6 high-quality sample images (Chinese + English for each theme)
- White and black triangle templates
- Light background template (1600x900 white)
- Custom background template with warm gradient
- All templates automatically included in PyPI package

### 🔧 API Enhancements
- Extended from 4 to 9 configurable parameters
- Backward compatibility maintained
- Enhanced parameter validation
- Improved error handling

### 📚 Documentation Updates
- Complete README overhaul with three theme showcase
- Added optimal length recommendations (Chinese: 10-12 chars, English: 7 words)
- Interactive theme usage examples
- Public sample image URLs integrated
- "What's Included Automatically" section added

### 🎯 Optimizations
- Clean font rendering (removed stroke effects for pure text)
- Intelligent theme-based color selection
- Smart triangle enable/disable logic
- Enhanced text-background contrast
- Improved font loading priority

### 🌟 User Experience
- No additional downloads required - all templates included
- Immediate use after installation
- Professional-grade theme options
- Comprehensive usage examples

## [2.1.3] - 2025-01-XX

### 🔧 Improvements
- Enhanced font selection algorithm
- Improved Chinese text rendering
- Better error handling for missing fonts

## [2.1.2] - 2025-01-XX

### 🐛 Bug Fixes
- Fixed font loading issues on different platforms
- Improved template path resolution
- Enhanced cross-platform compatibility

## [2.1.0] - 2025-01-XX

### ✨ Features Added
- Professional template support
- Intelligent Chinese/English text processing
- Dynamic font scaling based on language
- Triangle overlay integration
- Smart line-breaking algorithms
- Multi-platform font support

### 🎨 Core Capabilities
- 1600x900 professional thumbnail generation
- Chinese fonts 30% larger for optimal readability
- English 3-line limit with intelligent wrapping
- PNG overlay technology
- Auto square conversion for right-side images
- Flask RESTful API support

### 📦 Initial Release
- PyPI package publication
- GitHub repository setup
- MIT license
- Basic documentation
- Example usage scripts

---

## 📋 Legend

- 🎉 **Major Features**: Significant new functionality
- ✨ **Features**: New features and enhancements
- 🔧 **Improvements**: Performance and usability improvements
- 🐛 **Bug Fixes**: Bug fixes and error corrections
- 📦 **Package**: Package and distribution changes
- 📚 **Documentation**: Documentation updates
- 🎨 **Design**: Visual and design improvements
- 🌟 **UX**: User experience enhancements
- 🎯 **Optimization**: Performance optimizations

---

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/youtube-thumbnail-generator/
- **GitHub Repository**: https://github.com/preangelleo/youtube-thumbnail-generator
- **Documentation**: https://github.com/preangelleo/youtube-thumbnail-generator#readme
- **Bug Reports**: https://github.com/preangelleo/youtube-thumbnail-generator/issues

---

**Author**: Leo Wang (https://leowang.net)  
**License**: MIT  
**Python Support**: 3.7+