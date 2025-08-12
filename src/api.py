#!/usr/bin/env python3
"""
Flask API for YouTube Thumbnail Generator
"""

import os
import base64
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import io
from PIL import Image

from .thumbnail_generator import ThumbnailGenerator

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize generator
generator = None

def init_generator():
    """Initialize the thumbnail generator."""
    global generator
    if generator is None:
        generator = ThumbnailGenerator(
            gemini_api_key=os.getenv('GEMINI_API_KEY'),
            enable_ai_optimization=os.getenv('ENABLE_AI_OPTIMIZATION', 'false').lower() == 'true',
            default_language=os.getenv('DEFAULT_LANGUAGE', 'auto')
        )
    return generator

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'ai_enabled': bool(os.getenv('GEMINI_API_KEY'))
    })

@app.route('/generate', methods=['POST'])
def generate_thumbnail():
    """Generate a thumbnail with all parameters.
    
    Request JSON:
    {
        "text": "Thumbnail text",
        "background_type": "gradient",
        "background_config": {
            "color1": "#667eea",
            "color2": "#764ba2",
            "direction": "diagonal"
        },
        "font_name": null,
        "font_size": 72,
        "font_color": "#FFFFFF",
        "text_position": "center",
        "enable_ai_optimization": true,
        "source_language": null,  // null = auto-detect, "en" or "zh" to skip detection
        "target_language": "en",  // For translation (only used if different from source)
        "custom_prompt": null,
        "quality": 95,
        "format": "png",
        "return_base64": true
    }
    """
    try:
        gen = init_generator()
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        # Extract parameters with defaults
        text = data.get('text', '')
        background_type = data.get('background_type', 'gradient')
        background_config = data.get('background_config', {})
        font_name = data.get('font_name')
        font_size = data.get('font_size', 72)
        font_color = data.get('font_color', '#FFFFFF')
        text_position = data.get('text_position', 'center')
        enable_ai = data.get('enable_ai_optimization')
        source_language = data.get('source_language')  # User-specified input language
        target_language = data.get('target_language')  # For translation
        custom_prompt = data.get('custom_prompt')
        quality = data.get('quality', 95)
        output_format = data.get('format', 'png').lower()
        return_base64 = data.get('return_base64', True)
        
        # Handle custom position
        if isinstance(text_position, list) and len(text_position) == 2:
            text_position = tuple(text_position)
        
        # Generate thumbnail
        with tempfile.NamedTemporaryFile(
            suffix=f'.{output_format}',
            delete=False
        ) as tmp_file:
            output_path = gen.generate(
                text=text,
                output_path=tmp_file.name,
                background_type=background_type,
                background_config=background_config,
                font_name=font_name,
                font_size=font_size,
                font_color=font_color,
                text_position=text_position,
                enable_ai_optimization=enable_ai,
                source_language=source_language,
                target_language=target_language,
                custom_prompt=custom_prompt,
                quality=quality
            )
            
            if return_base64:
                # Return as base64
                with open(output_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                os.unlink(output_path)
                
                return jsonify({
                    'success': True,
                    'image': f'data:image/{output_format};base64,{image_data}',
                    'format': output_format
                })
            else:
                # Return as file
                return send_file(
                    output_path,
                    mimetype=f'image/{output_format}',
                    as_attachment=True,
                    download_name=f'thumbnail.{output_format}'
                )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/batch', methods=['POST'])
def batch_generate():
    """Generate multiple thumbnails.
    
    Request JSON:
    {
        "texts": ["Text 1", "Text 2", "Text 3"],
        "background_type": "gradient",
        "background_config": {...},
        "enable_ai_optimization": true,
        "target_language": "en",
        ...
    }
    """
    try:
        gen = init_generator()
        data = request.json
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'Texts array is required'}), 400
        
        texts = data.get('texts', [])
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'Texts must be a non-empty array'}), 400
        
        # Common parameters
        params = {k: v for k, v in data.items() if k != 'texts'}
        
        results = []
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = gen.batch_generate(
                texts=texts,
                output_dir=tmpdir,
                **params
            )
            
            for i, path in enumerate(paths):
                with open(path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                    results.append({
                        'text': texts[i],
                        'image': f'data:image/png;base64,{image_data}'
                    })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'thumbnails': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/fonts', methods=['GET'])
def list_fonts():
    """List available fonts."""
    try:
        gen = init_generator()
        fonts = gen.font_manager.list_available_fonts()
        
        return jsonify({
            'success': True,
            'fonts': fonts
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/detect-language', methods=['POST'])
def detect_language():
    """Detect language of text.
    
    Request JSON:
    {
        "text": "Text to analyze"
    }
    """
    try:
        from .utils import detect_language as detect_lang
        
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data.get('text', '')
        language = detect_lang(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'language': language,
            'language_name': 'English' if language == 'en' else 'Chinese'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/optimize-text', methods=['POST'])
def optimize_text():
    """Optimize text using AI (requires API key).
    
    Request JSON:
    {
        "text": "Original text",
        "source_language": "zh",  // Optional: specify input language
        "target_language": "en",  // Translate to English
        "style": "engaging",
        "max_length": 50,
        "custom_prompt": null
    }
    """
    try:
        gen = init_generator()
        
        if not gen.text_optimizer:
            return jsonify({
                'success': False,
                'error': 'AI optimization not available (no API key)'
            }), 400
        
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data.get('text', '')
        source_language = data.get('source_language')  # Optional
        target_language = data.get('target_language', 'en')
        style = data.get('style', 'engaging')
        max_length = data.get('max_length', 50)
        custom_prompt = data.get('custom_prompt')
        
        # Auto-detect source if not provided
        if not source_language:
            from .utils import detect_language
            source_language = detect_language(text)
        
        optimized = gen.text_optimizer.optimize(
            text=text,
            source_language=source_language,
            target_language=target_language,
            custom_prompt=custom_prompt,
            max_length=max_length,
            style=style
        )
        
        return jsonify({
            'success': True,
            'original': text,
            'optimized': optimized,
            'language': target_language
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB'
    }), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )