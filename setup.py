from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "Pillow>=10.0.0",
    "numpy>=1.24.0",
    "python-dotenv>=1.0.0",
    "Flask>=2.3.0",
    "flask-cors>=4.0.0",
    "google-generativeai>=0.3.0",
    "langdetect>=1.0.9",
]

setup(
    name="youtube-thumbnail-generator",
    version="1.1.0",
    author="preangelleo",
    author_email="",
    description="A powerful YouTube thumbnail generator with AI text optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/preangelleo/youtube-thumbnail-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "youtube-thumbnail=src.cli:main",
        ],
    },
    include_package_data=True,
    keywords="youtube thumbnail generator ai gemini image processing",
    project_urls={
        "Bug Reports": "https://github.com/preangelleo/youtube-thumbnail-generator/issues",
        "Source": "https://github.com/preangelleo/youtube-thumbnail-generator",
        "Documentation": "https://github.com/preangelleo/youtube-thumbnail-generator/docs",
    },
)