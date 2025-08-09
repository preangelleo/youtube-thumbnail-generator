#!/usr/bin/env python3
"""
YouTube缩略图生成器 API 服务
提供RESTful API接口用于生成缩略图
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import threading
import time
import os
from datetime import datetime
try:
    # 当作为包安装时的导入方式
    from .final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path
    from .function_add_chapter import add_chapter_to_image
except ImportError:
    # 直接运行时的导入方式
    from final_thumbnail_generator import FinalThumbnailGenerator, get_resource_path
    from function_add_chapter import add_chapter_to_image

app = Flask(__name__)
CORS(app)

# 任务存储
tasks = {}

# 初始化生成器
template_path = get_resource_path("templates/professional_template.jpg")
if not os.path.exists(template_path):
    print(f"警告: 模板文件不存在 {template_path}")
    template_path = None

def background_generate(task_id, **kwargs):
    """后台生成缩略图任务"""
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = '初始化生成器...'
        
        if template_path is None:
            tasks[task_id]['status'] = 'failed'
            tasks[task_id]['error'] = '模板文件不存在'
            return
        
        # 支持Google API Key参数
        google_api_key = kwargs.get('google_api_key')
        generator = FinalThumbnailGenerator(template_path, google_api_key=google_api_key)
        
        tasks[task_id]['progress'] = '生成缩略图中...'
        
        # 为每个任务生成唯一的文件名，避免冲突
        output_filename = f"thumbnail_{task_id[:8]}.jpg"
        output_path = f"outputs/{output_filename}"
        
        result = generator.generate_final_thumbnail(
            title=kwargs.get('title', ''),
            author=kwargs.get('author'),
            logo_path=kwargs.get('logo_path'),
            right_image_path=kwargs.get('right_image_path'),
            output_path=output_path,
            theme=kwargs.get('theme', 'dark'),
            custom_template=kwargs.get('custom_template'),
            title_color=kwargs.get('title_color'),
            author_color=kwargs.get('author_color'),
            enable_triangle=kwargs.get('enable_triangle'),
            triangle_direction=kwargs.get('triangle_direction'),
            flip=kwargs.get('flip'),
            youtube_ready=kwargs.get('youtube_ready', True)
        )
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result_file'] = output_filename
        tasks[task_id]['download_url'] = f'/api/download/{output_filename}'
        tasks[task_id]['generation_time'] = f"{time.time() - tasks[task_id]['start_time']:.2f}s"
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
        print(f"缩略图生成任务失败 {task_id}: {e}")

def background_generate_chapter(task_id, **kwargs):
    """后台生成Chapter任务"""
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = '生成Chapter图片中...'
        
        # Chapter生成参数
        text = kwargs.get('text', '')
        image_path = kwargs.get('image_path')
        font_size = kwargs.get('font_size')
        language = kwargs.get('language', 'english')
        width = kwargs.get('width', 1600)
        height = kwargs.get('height', 900)
        
        # 为每个Chapter任务生成唯一的文件名，避免冲突
        output_filename = f"chapter_{task_id[:8]}.jpg"
        output_path = f"outputs/{output_filename}"
        
        success, result_path = add_chapter_to_image(
            text=text,
            image_path=image_path,
            output_path=output_path,
            font_size=font_size,
            language=language,
            width=width,
            height=height
        )
        
        if success:
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['result_file'] = output_filename
            tasks[task_id]['download_url'] = f'/api/download/{output_filename}'
            tasks[task_id]['generation_time'] = f"{time.time() - tasks[task_id]['start_time']:.2f}s"
        else:
            tasks[task_id]['status'] = 'failed'
            tasks[task_id]['error'] = 'Chapter图片生成失败'
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
        print(f"Chapter生成任务失败 {task_id}: {e}")

def background_generate_random(task_id, **kwargs):
    """后台生成随机缩略图任务"""
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = '初始化随机生成器...'
        
        # 导入随机生成函数
        try:
            from .final_thumbnail_generator import generate_random_thumbnail
        except ImportError:
            from final_thumbnail_generator import generate_random_thumbnail
        
        tasks[task_id]['progress'] = '生成随机缩略图中...'
        
        # 为每个任务生成唯一的文件名，避免冲突
        output_filename = f"random_{task_id[:8]}.jpg"
        output_path = f"outputs/{output_filename}"
        
        result = generate_random_thumbnail(
            title=kwargs.get('title', ''),
            author=kwargs.get('author'),
            logo_path=kwargs.get('logo_path'),
            right_image_path=kwargs.get('right_image_path'),
            output_path=output_path,
            google_api_key=kwargs.get('google_api_key'),
            youtube_ready=kwargs.get('youtube_ready', True)
        )
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result_file'] = output_filename
        tasks[task_id]['download_url'] = f'/api/download/{output_filename}'
        tasks[task_id]['generation_time'] = f"{time.time() - tasks[task_id]['start_time']:.2f}s"
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
        print(f"随机缩略图生成任务失败 {task_id}: {e}")

@app.route('/api/generate/enhanced', methods=['POST'])
def generate_enhanced():
    """生成最终版缩略图"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': '缺少必填参数: title'}), 400
        
        # 创建任务
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'created',
            'start_time': time.time(),
            'progress': '任务创建成功'
        }
        
        # 启动后台任务
        thread = threading.Thread(
            target=background_generate,
            args=(task_id,),
            kwargs=data
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'processing',
            'message': '缩略图生成任务已启动'
        })
        
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.route('/api/generate/chapter', methods=['POST'])
def generate_chapter():
    """生成Chapter图片"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': '缺少必填参数: text'}), 400
        
        # 创建任务
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'created',
            'start_time': time.time(),
            'progress': 'Chapter任务创建成功'
        }
        
        # 启动后台任务
        thread = threading.Thread(
            target=background_generate_chapter,
            args=(task_id,),
            kwargs=data
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'processing',
            'message': 'Chapter图片生成任务已启动'
        })
        
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.route('/api/generate/random', methods=['POST'])
def generate_random():
    """生成随机缩略图（12种组合中随机选择）"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': '缺少必填参数: title'}), 400
        
        # 创建任务
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'created',
            'start_time': time.time(),
            'progress': '随机缩略图任务创建成功'
        }
        
        # 启动后台任务
        thread = threading.Thread(
            target=background_generate_random,
            args=(task_id,),
            kwargs=data
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'processing',
            'message': '随机缩略图生成任务已启动，将从12种组合中随机选择'
        })
        
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """查看任务状态"""
    if task_id not in tasks:
        return jsonify({'error': '任务不存在'}), 404
    
    return jsonify(tasks[task_id])

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """下载生成的文件"""
    file_path = os.path.join('outputs', filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    
    return send_file(file_path, as_attachment=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """获取模板列表"""
    templates = []
    template_dir = 'templates'
    
    if os.path.exists(template_dir):
        for filename in os.listdir(template_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                templates.append({
                    'name': filename,
                    'size': '1600x900' if 'professional' in filename else '1280x720',
                    'description': '专业版模板' if 'professional' in filename else '标准模板'
                })
    
    return jsonify({'templates': templates})

@app.route('/api/assets', methods=['GET'])
def get_assets():
    """获取资源列表"""
    logos = []
    images = []
    
    if os.path.exists('logos'):
        logos = [f for f in os.listdir('logos') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if os.path.exists('assets'):
        images = [f for f in os.listdir('assets') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    return jsonify({
        'logos': logos,
        'images': images
    })

@app.route('/', methods=['GET'])
def index():
    """API首页"""
    return jsonify({
        'name': 'YouTube 缩略图生成器 API',
        'version': '1.0',
        'endpoints': {
            'POST /api/generate/enhanced': '生成定制缩略图（支持所有参数）',
            'POST /api/generate/random': '生成随机缩略图（12种组合随机选择）',
            'POST /api/generate/chapter': '生成Chapter图片',
            'GET /api/status/<task_id>': '查看任务状态',
            'GET /api/download/<filename>': '下载文件',
            'GET /api/health': '健康检查',
            'GET /api/templates': '获取模板列表',
            'GET /api/assets': '获取资源列表'
        }
    })

def main():
    """命令行入口函数"""
    # 确保必要的目录存在
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('logos', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("YouTube 缩略图生成器 API 启动中...")
    print("访问 http://localhost:5002 查看API信息")
    print("主要端点: POST /api/generate/enhanced")
    
    app.run(host='0.0.0.0', port=5002, debug=False)

if __name__ == '__main__':
    main()