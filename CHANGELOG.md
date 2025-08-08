# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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