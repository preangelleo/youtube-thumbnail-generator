"""
Setup script for YouTube Thumbnail Generator
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A professional YouTube thumbnail generation library"

# Read requirements from requirements.txt
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['Pillow>=8.0.0', 'flask>=2.0.0', 'flask-cors>=3.0.0']

setup(
    name="youtube-thumbnail-generator",
    version="2.4.11",
    author="Leo Wang",
    author_email="me@leowang.net",
    description="Professional YouTube thumbnail generator with enhanced Chinese font bold rendering and intelligent text processing",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/preangelleo/youtube-thumbnail-generator",
    project_urls={
        "Bug Reports": "https://github.com/preangelleo/youtube-thumbnail-generator/issues",
        "Source": "https://github.com/preangelleo/youtube-thumbnail-generator",
        "Documentation": "https://github.com/preangelleo/youtube-thumbnail-generator#readme"
    },
    packages=['youtube_thumbnail_generator'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "api": ["flask>=2.0.0", "flask-cors>=3.0.0"],
        "dev": ["pytest>=6.0", "black", "flake8"],
    },
    include_package_data=True,
    package_data={
        'youtube_thumbnail_generator': [
            'templates/*.jpg',
            'templates/*.png',
            'fonts/*.ttf',
            'fonts/*.ttc'
        ],
    },
    entry_points={
        'console_scripts': [
            'youtube-thumbnail-api=youtube_thumbnail_generator.api_server:main',
        ],
    },
    keywords=[
        "youtube", "thumbnail", "generator", "ai", "chinese", "english", 
        "text-processing", "image-generation", "PIL", "graphics", "automation"
    ],
    zip_safe=False,
)