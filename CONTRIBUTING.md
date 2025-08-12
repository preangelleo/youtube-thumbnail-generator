# Contributing to YouTube Thumbnail Generator

Thank you for your interest in contributing! We welcome contributions from everyone.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/youtube-thumbnail-generator.git
cd youtube-thumbnail-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep line length under 120 characters

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Pull Request Guidelines

- Update documentation if needed
- Add tests for new functionality
- Update CHANGELOG.md
- Ensure CI/CD passes

## Reporting Issues

- Use the issue tracker
- Include Python version and OS
- Provide minimal reproducible example
- Include error messages and stack traces

## License

By contributing, you agree that your contributions will be licensed under the MIT License.