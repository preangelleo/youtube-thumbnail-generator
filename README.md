# YouTube 缩略图生成器 v2.1

专业的YouTube缩略图自动生成工具，支持中英文智能文字布局、Logo、图片的精确控制和动态适配。

## 📋 核心特性

- ✅ **中英文智能系统**: PNG贴图技术，完美处理中英文混排
- ✅ **智能换行算法**: 中文9字/20字限制，英文3行截断
- ✅ **字体差异化优化**: 中文字体增大30%，副标题高度增加20%
- ✅ **专业视觉效果**: 三角形过渡集成到图片，文字始终最上层
- ✅ **图片智能处理**: 自动正方形转换 + 900x900填充
- ✅ **多端API支持**: Flask RESTful API + Chapter功能
- ✅ **字体智能选择**: 中文PingFang/方正黑体，英文Lexend Bold

## 🎨 模板规格

### 专业模板 (Professional Template)

**画布尺寸**: 1600x900 像素

**布局分区**:
- **左侧文字区域**: 700x900 像素 - 黑色背景，文字显示
- **右侧图片区域**: 900x900 像素 - 正方形图片填充  
- **三角形过渡**: 200x900 像素 - 优雅的斜线分割效果

## 🧠 智能文字系统

### 核心技术：PNG贴图 + 三角形集成
不再直接在模板上绘制文字，而是：
1. **独立渲染**: 先生成透明背景的PNG文字图片
2. **智能调整**: 根据文字长度动态调整PNG尺寸
3. **三角形集成**: 三角形先贴到右侧图片，再整体贴到模板
4. **文字覆盖**: PNG文字最后贴入，确保在最上层显示

### 中英文差异化处理
#### 中文优化
- **字体增大**: 比英文大30% (54px vs 42px标题，26px vs 20px副标题)
- **副标题增高**: 比英文高20% (36px vs 30px)
- **智能换行**: 
  - 标题：超过9字换行，除以2分配，奇数字符放第二行
  - 副标题：超过20字换行，除以2分配
- **行间距**: 标题16px，副标题8px

#### 英文处理
- **空格换行**: 按单词边界自然换行
- **3行限制**: 标题最多3行，超过自动截断+省略号
- **标准字体**: Lexend Bold
- **标准行间距**: 8px

## 📝 输入参数详解

### 必填参数
**`title`** (str) - 主标题
```python
title="The Ultimate Complete Guide to Advanced AI Technology"
```
- **智能换行**: 自动计算最优换行位置
- **动态高度**: 根据行数调整PNG高度(55px/行 + 行间距)
- **字体**: 45px Helvetica，白色 #FFFFFF
- **效果**: 黑色描边 + 阴影，专业视觉
- **位置**: (50, 280)起始，实际高度动态调整

### 可选参数

**`subtitle`** (str) - 副标题
```python
subtitle="Everything You Need to Know About Modern Technology"
```
- **智能适配**: 1行=30px，2行=68px，3行=106px高度
- **字体**: 20px Helvetica，淡黄色 #FFEB9C  
- **位置**: 标题下方20px间距，自动计算Y坐标
- **截断规则**: 超过3行自动添加省略号

**`author`** (str) - 作者名称
```python
author="Leo Wang"  # 自动转为 "LEO WANG"
```
- **格式**: 自动转换为全大写
- **位置**: 固定底部 (50, 860)
- **字体**: 36px Lexend Bold，浅灰色 #CCCCCC

**`logo_path`** (str) - Logo文件路径
```python
logo_path="logos/your_logo.png"
```
- **位置**: 左上角 (50, 50)，左边距=上边距
- **区域**: 240x150像素，自动等比缩放
- **格式**: 支持 PNG/JPG，自动处理透明度

**`right_image_path`** (str) - 右侧图片路径
```python
right_image_path="assets/your_image.jpg"
```
- **智能裁剪**: 自动转换为正方形（居中裁剪）
- **填充方式**: 缩放到900x900像素填满右侧
- **位置**: (700, 0)开始的右侧区域

## 🚀 使用方法

### 1. 直接Python调用
```python
from final_thumbnail_generator import FinalThumbnailGenerator

# 初始化生成器
generator = FinalThumbnailGenerator("templates/professional_template.jpg")

# 生成缩略图（所有参数示例）
result = generator.generate_final_thumbnail(
    title="The Ultimate Complete Guide to Advanced AI Technology Revolution and Future Gaming Setup Reviews 2025",
    subtitle="Everything You Need to Know About Modern Technology and Future Developments",
    author="Leo Wang",
    logo_path="logos/animagent_logo.png",
    right_image_path="assets/testing_image.jpeg",
    output_path="outputs/final_test.jpg"
)

print(f"生成完成: {result}")
```

### 2. API 服务调用

#### 启动服务
```bash
python api_server.py
# 服务运行在 http://localhost:5002
```

#### 生成缩略图
```bash
curl -X POST http://localhost:5002/api/generate/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing Tech Reviews 2025",
    "subtitle": "The Future is Now",
    "author": "Leo Wang",
    "logo_path": "logos/animagent_logo.png",
    "right_image_path": "assets/testing_image.jpeg"
  }'
```

#### 响应示例
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "processing",
  "message": "缩略图生成任务已启动"
}
```

#### 查看任务状态
```bash
curl http://localhost:5002/api/status/abc123-def456-ghi789
```

#### 下载结果
```bash
curl -O http://localhost:5002/api/download/final_test.jpg
```

### 3. Python API客户端示例
```python
import requests
import time
import json

def generate_thumbnail_api(title, subtitle=None, author=None, logo_path=None, image_path=None):
    """使用API生成缩略图"""
    
    # 1. 发起生成请求
    response = requests.post('http://localhost:5002/api/generate/enhanced', 
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "logo_path": logo_path,
            "right_image_path": image_path
        })
    )
    
    task_data = response.json()
    task_id = task_data['task_id']
    print(f"任务已创建: {task_id}")
    
    # 2. 轮询状态直到完成
    while True:
        status_response = requests.get(f'http://localhost:5002/api/status/{task_id}')
        status_data = status_response.json()
        
        print(f"状态: {status_data['status']}")
        
        if status_data['status'] == 'completed':
            print(f"生成完成! 下载: {status_data['download_url']}")
            return status_data['download_url']
        elif status_data['status'] == 'failed':
            print(f"生成失败: {status_data['error']}")
            return None
        
        time.sleep(1)

# 使用示例
download_url = generate_thumbnail_api(
    title="My Amazing YouTube Video Title That Is Really Long",
    subtitle="Quick Summary of the Content", 
    author="Your Name",
    logo_path="logos/my_logo.png",
    image_path="assets/thumbnail_image.jpg"
)
```

## 🎯 API 端点完整指南

### 缩略图生成
`POST /api/generate/enhanced`

**请求体**:
```json
{
  "title": "必填 - 主标题文字",
  "subtitle": "可选 - 副标题文字", 
  "author": "可选 - 作者名称",
  "logo_path": "可选 - Logo文件路径",
  "right_image_path": "可选 - 右侧图片路径"
}
```

### Chapter图片生成  
`POST /api/generate/chapter`

**请求体**:
```json
{
  "text": "必填 - 要显示的文字",
  "language": "可选 - english/chinese",
  "font_size": "可选 - 字体大小",
  "width": "可选 - 图片宽度，默认1600", 
  "height": "可选 - 图片高度，默认900"
}
```

### 其他端点
- `GET /api/status/<task_id>` - 查看任务状态
- `GET /api/download/<filename>` - 下载生成文件
- `GET /api/health` - 健康检查
- `GET /api/templates` - 获取可用模板
- `GET /api/assets` - 获取资源列表

## 📊 智能布局示例

### 短标题效果
```
标题: "Tech News 2025" 
→ 1行，55px高度
副标题: "Daily Updates"
→ 1行，30px高度
布局紧凑，专业美观
```

### 长标题效果  
```
标题: "The Ultimate Complete Guide to Advanced AI Technology..."
→ 5行，307px高度 (5×55px + 4×8px行间距)
副标题: "Everything You Need to Know About Modern Technology"  
→ 2行，68px高度 (2×30px + 1×8px行间距)
自动调整位置，完美适配
```

### 超长内容处理
```
副标题超过3行 → 自动截断为 "Very long subtitle text that goes on and on..."
保证布局稳定，避免内容溢出
```

## 🔧 高级配置

### 文件路径规则
- **相对路径**: 相对于项目根目录
- **Logo目录**: `logos/` - 存放所有Logo文件
- **素材目录**: `assets/` - 存放背景图片
- **输出目录**: `outputs/` - 生成结果存放
- **模板目录**: `templates/` - 模板文件存放

### 支持的图片格式
- **输入**: PNG, JPG, JPEG (支持透明度)
- **输出**: JPG (高质量，95%质量)
- **处理**: 自动色彩模式转换

### 字体优先级
```
英文字体:
1. Helvetica (Mac系统)
2. Lexend Bold (如已安装)
3. Ubuntu Bold (Linux)
4. 系统默认字体

中文字体:
1. Noto Sans CJK Bold
2. 思源黑体
3. 文泉驿字体
```

## 📁 项目结构
```
youtube_thumbnail_generator/
├── final_thumbnail_generator.py     # 核心生成器
├── text_png_generator.py           # PNG文字渲染器  
├── api_server.py                   # Flask API服务
├── function_add_chapter.py         # Chapter功能
├── create_triangle_template.py     # 三角形模板生成
├── templates/
│   ├── professional_template.jpg   # 1600x900专业模板
│   └── triangle_template.png       # 200x900三角形过渡
├── logos/                          # Logo文件目录
├── assets/                         # 图片素材目录  
├── outputs/                        # 生成结果目录
├── README.md                       # 项目文档
└── README_API.md                   # API详细文档
```

## 📈 版本历史

### v2.0 (当前版本) - 智能布局革命
- ✅ **PNG贴图技术**: 文字渲染与模板分离，完美控制
- ✅ **智能高度调整**: 根据内容长度动态调整布局
- ✅ **行间距优化**: 8px行间距，提升阅读体验
- ✅ **三角形过渡**: 200x900斜线分割，专业视觉效果
- ✅ **截断机制**: 超长内容智能截断，布局稳定
- ✅ **双API支持**: 缩略图 + Chapter 双功能API

### v1.0 - 基础功能
- ✅ 专业模板布局设计
- ✅ 自动图片正方形转换  
- ✅ 5参数输入系统
- ✅ 智能字体选择
- ✅ 完整的文字效果
- ✅ Flask API 集成

## 🎯 最佳实践

### 标题文字建议
- **长度**: 建议50-100字符，系统自动优化显示
- **内容**: 清晰表达视频主题，吸引观众点击
- **关键词**: 前置重要关键词，提升搜索效果

### 副标题使用技巧
- **定位**: 补充说明或强调要点
- **长度**: 建议20-60字符，超过自动处理
- **风格**: 与主标题形成层次对比

### 图片选择原则
- **尺寸**: 任意尺寸，系统自动转为正方形
- **内容**: 选择视觉冲击力强的图片
- **质量**: 建议高分辨率，确保缩放后清晰

## 🚨 注意事项

1. **文件路径**: 确保所有文件路径正确且文件存在
2. **字体依赖**: 系统会自动降级到可用字体
3. **输出覆盖**: 默认输出`final_test.jpg`，会覆盖同名文件
4. **API异步**: API采用异步处理，需要轮询状态
5. **内存使用**: 大图片处理可能占用较多内存

---

## 💡 快速开始

1. **安装依赖**: `pip install pillow flask flask-cors`
2. **准备素材**: 将Logo和图片放入对应目录
3. **直接测试**: `python final_thumbnail_generator.py`
4. **API服务**: `python api_server.py`
5. **查看结果**: 检查 `outputs/final_test.jpg`

现在就开始创建专业的YouTube缩略图吧！🎬✨