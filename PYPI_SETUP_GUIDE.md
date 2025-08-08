# PyPI Upload Setup Guide

This guide helps you upload the YouTube Thumbnail Generator to PyPI so users worldwide can install it with `pip install youtube-thumbnail-generator`.

## Step 1: Create PyPI Accounts

### 1.1 Create TestPyPI Account (for testing)
1. Go to https://test.pypi.org/account/register/
2. Fill in your details and create account
3. Verify your email address

### 1.2 Create PyPI Account (for production)
1. Go to https://pypi.org/account/register/
2. Fill in your details and create account  
3. Verify your email address

## Step 2: Generate API Tokens

### 2.1 TestPyPI API Token
1. Login to https://test.pypi.org
2. Go to Account settings → API tokens
3. Click "Add API token"
4. Name: "youtube-thumbnail-generator"
5. Scope: "Entire account" (since it's your first project)
6. **SAVE THE TOKEN** - you won't see it again!

### 2.2 PyPI API Token
1. Login to https://pypi.org
2. Go to Account settings → API tokens
3. Click "Add API token" 
4. Name: "youtube-thumbnail-generator"
5. Scope: "Entire account"
6. **SAVE THE TOKEN** - you won't see it again!

## Step 3: Configure Twine with Tokens

Create or update your `~/.pypirc` file:

```ini
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-api-token>

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <your-pypi-api-token>
```

Replace `<your-testpypi-api-token>` and `<your-pypi-api-token>` with the actual tokens you generated.

## Step 4: Upload to PyPI

### Option A: Use the Upload Script (Recommended)
```bash
./upload_to_pypi.sh
```

Follow the interactive prompts to upload to TestPyPI first, then PyPI.

### Option B: Manual Upload Commands

#### Upload to TestPyPI first (recommended)
```bash
twine upload --repository testpypi dist/*
```

Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ youtube-thumbnail-generator
```

#### Upload to PyPI (production)
```bash
twine upload dist/*
```

## Step 5: Verify Upload

### TestPyPI
- Visit: https://test.pypi.org/project/youtube-thumbnail-generator/
- Test install: `pip install --index-url https://test.pypi.org/simple/ youtube-thumbnail-generator`

### PyPI  
- Visit: https://pypi.org/project/youtube-thumbnail-generator/
- Install: `pip install youtube-thumbnail-generator`

## Troubleshooting

### Common Issues

1. **403 Forbidden**: Check your API token is correct in ~/.pypirc
2. **Package already exists**: Increment version number in setup.py and pyproject.toml
3. **Invalid authentication**: Regenerate API tokens and update ~/.pypirc

### Version Updates

To release a new version:
1. Update version in `setup.py` and `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload: `twine upload dist/*`

## Security Notes

- Keep your API tokens secret and secure
- Never commit ~/.pypirc to version control
- Use project-scoped tokens when possible
- Rotate tokens periodically

## Success!

Once uploaded to PyPI, anyone in the world can install your package:

```bash
pip install youtube-thumbnail-generator
```

Your package will be available at:
- https://pypi.org/project/youtube-thumbnail-generator/
- Searchable in PyPI search
- Installable on any system with pip

Congratulations on your first PyPI package! 🎉