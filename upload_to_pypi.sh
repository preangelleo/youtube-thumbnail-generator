#!/bin/bash

# YouTube Thumbnail Generator - PyPI Upload Script
# Author: Leo Wang (https://leowang.net)

echo "🚀 YouTube Thumbnail Generator v2.1 - PyPI Upload"
echo "================================================="
echo ""

# Check if packages exist
if [ ! -f "dist/youtube_thumbnail_generator-2.1.0-py3-none-any.whl" ]; then
    echo "❌ Wheel package not found. Please run: python -m build"
    exit 1
fi

if [ ! -f "dist/youtube_thumbnail_generator-2.1.0.tar.gz" ]; then
    echo "❌ Source package not found. Please run: python -m build"
    exit 1
fi

# Check packages
echo "🔍 Checking package quality..."
twine check dist/*

if [ $? -ne 0 ]; then
    echo "❌ Package quality check failed"
    exit 1
fi

echo "✅ Package quality check passed"
echo ""

# Ask user for upload target
echo "Choose upload target:"
echo "1) TestPyPI (recommended for first upload)"
echo "2) PyPI (production)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🧪 Uploading to TestPyPI..."
        echo "Note: You need an account at https://test.pypi.org"
        echo ""
        twine upload --repository testpypi dist/*
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 Upload to TestPyPI successful!"
            echo ""
            echo "Test installation with:"
            echo "pip install --index-url https://test.pypi.org/simple/ youtube-thumbnail-generator"
        fi
        ;;
    2)
        echo "🌍 Uploading to PyPI (production)..."
        echo "Note: You need an account at https://pypi.org"
        echo "⚠️  This will make the package available to everyone!"
        echo ""
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            twine upload dist/*
            if [ $? -eq 0 ]; then
                echo ""
                echo "🎉 Upload to PyPI successful!"
                echo ""
                echo "Your package is now available worldwide:"
                echo "pip install youtube-thumbnail-generator"
                echo ""
                echo "PyPI page: https://pypi.org/project/youtube-thumbnail-generator/"
            fi
        else
            echo "Upload cancelled"
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac