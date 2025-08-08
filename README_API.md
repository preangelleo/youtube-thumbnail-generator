# YouTube 缩略图生成器 v2.1 - API 文档

## 🚀 快速开始

### 启动服务
```bash
python api_server.py
```
服务将在 `http://localhost:5002` 启动

## 📡 API 端点

### 1. 生成智能缩略图
**端点**: `POST /api/generate/enhanced`

**功能**: 使用v2.1智能系统生成YouTube缩略图，支持中英文差异化处理

### 2. 生成Chapter图片
**端点**: `POST /api/generate/chapter`

**功能**: 生成带文字的Chapter图片，支持中英文

#### 请求参数 (缩略图)
```json
{
    "title": "终极人工智能技术革命完整指南",        // 必填：主标题（中文>9字自动换行）
    "subtitle": "所有你需要知道的现代科技",         // 可选：副标题（可为null，中文>20字换行）
    "author": "Leo Wang",                        // 可选：作者名（自动大写）
    "logo_path": "logos/animagent_logo.png",     // 可选：Logo文件路径
    "right_image_path": "assets/testing_image.jpeg" // 可选：右侧图片路径
}
```

#### v2.1 智能特性
- **中英文自动识别**: 根据内容自动选择最佳字体和处理方式
- **中文优化**: 字体增大30%，副标题高度增加20%
- **智能换行**: 中文标题9字限制，副标题20字限制
- **英文处理**: 3行限制，自动截断+省略号
- **布局调整**: 无副标题时标题自动居中（下移50px）
- **三角形效果**: 集成到右侧图片，文字始终显示在最上层
- **唯一文件名**: 每个任务生成独立文件，避免冲突
- **参数容错**: 空字符串自动转为null，触发智能布局

#### 响应示例
```json
{
    "task_id": "377f7bc3-b896-44ca-a501-b79308cc059d",
    "status": "processing", 
    "message": "缩略图生成任务已启动"
}
```

#### 请求参数 (Chapter)
```json
{
    "text": "这是一句重要的引言",                    // 必填：要添加的文字
    "image_path": "assets/background.jpg",       // 可选：背景图片路径
    "font_size": 86,                            // 可选：字体大小
    "language": "chinese",                      // 可选：语言 (chinese/english)
    "width": 1600,                              // 可选：图片宽度，默认1600
    "height": 900                               // 可选：图片高度，默认900
}
```

#### 响应示例
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "processing",
    "message": "缩略图生成任务已启动"
}
```

### 2. 查看任务状态
**端点**: `GET /api/status/<task_id>`

#### 响应示例 - 处理中
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "processing",
    "progress": "生成中..."
}
```

#### 响应示例 - 完成
```json
{
    "task_id": "377f7bc3-b896-44ca-a501-b79308cc059d",
    "status": "completed",
    "result_file": "thumbnail_377f7bc3.jpg",
    "download_url": "/api/download/thumbnail_377f7bc3.jpg",
    "generation_time": "0.12s"
}
```

#### 响应示例 - 失败
```json
{
    "task_id": "abc123-def456-ghi789",
    "status": "failed",
    "error": "模板文件不存在: templates/professional_template.jpg"
}
```

### 3. 下载生成文件
**端点**: `GET /api/download/<filename>`

直接下载生成的缩略图文件。

### 4. 健康检查
**端点**: `GET /api/health`

#### 响应示例
```json
{
    "status": "healthy",
    "timestamp": "2025-08-08T17:30:00Z",
    "version": "1.0"
}
```

### 5. 获取模板列表
**端点**: `GET /api/templates`

#### 响应示例
```json
{
    "templates": [
        {
            "name": "professional_template.jpg",
            "size": "1600x900",
            "description": "专业版模板"
        }
    ]
}
```

### 6. 获取资源列表  
**端点**: `GET /api/assets`

#### 响应示例
```json
{
    "logos": ["animagent_logo.png"],
    "images": ["testing_image.jpeg"]
}
```

## 🔧 使用示例

### Python 示例

#### 生成缩略图（完整示例）
```python
import requests
import time
import json

# 1. 发起中文缩略图生成请求（展示智能换行）
response = requests.post('http://localhost:5002/api/generate/enhanced', 
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "title": "终极人工智能技术革命完整指南",        # 14字，触发9字换行
        "subtitle": None,                            # null触发标题居中
        "author": "Leo Wang",
        "logo_path": "logos/animagent_logo.png",
        "right_image_path": "assets/testing_image.jpeg"
    })
)

task_data = response.json()
task_id = task_data['task_id']

# 2. 轮询任务状态
while True:
    status_response = requests.get(f'http://localhost:5002/api/status/{task_id}')
    status_data = status_response.json()
    
    if status_data['status'] == 'completed':
        print(f"生成完成！下载链接: {status_data['download_url']}")
        break
    elif status_data['status'] == 'failed':
        print(f"生成失败: {status_data['error']}")
        break
    else:
        print("生成中...")
        time.sleep(1)

# 3. 下载文件
if status_data['status'] == 'completed':
    file_response = requests.get(f"http://localhost:5002{status_data['download_url']}")
    with open('downloaded_thumbnail.jpg', 'wb') as f:
        f.write(file_response.content)
    print(f"文件已下载: downloaded_thumbnail.jpg")
```

### cURL 示例

#### 快速测试缩略图生成
```bash
# 1. 启动服务
python api_server.py &

# 2. 测试健康状态
curl http://localhost:5002/api/health

# 3. 发起生成请求（中文智能换行示例）
curl -X POST http://localhost:5002/api/generate/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "title": "终极人工智能技术革命完整指南",
    "subtitle": null,
    "author": "Leo Wang",
    "logo_path": "logos/animagent_logo.png",
    "right_image_path": "assets/testing_image.jpeg"
  }'

# 4. 查看任务状态（使用返回的task_id）
curl http://localhost:5002/api/status/377f7bc3-b896-44ca-a501-b79308cc059d

# 5. 下载结果文件
curl -O http://localhost:5002/api/download/thumbnail_377f7bc3.jpg
```

#### 生成Chapter图片
```python
import requests
import json

# 生成Chapter图片
response = requests.post('http://localhost:5002/api/generate/chapter',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "text": "人工智能将改变世界",
        "language": "chinese",
        "font_size": 86,
        "width": 1600,
        "height": 900
    })
)

task_data = response.json()
print(f"Chapter任务ID: {task_data['task_id']}")
```

## 🎯 v2.1 更新亮点

### 参数兼容性优化
- **唯一文件名**: `thumbnail_{task_id}.jpg` 格式，避免任务间冲突
- **智能subtitle处理**: 空字符串自动转为null，触发标题居中
- **完整错误处理**: 详细的任务状态和错误信息

### 性能改进  
- **快速生成**: 平均0.12秒生成时间
- **并发支持**: 多任务并行处理
- **内存优化**: 高效的图片处理流程

## 🔍 故障排除

### 常见问题
1. **端口占用**: `lsof -ti:5002 | xargs kill -9` 清理端口
2. **文件不存在**: 确保logo和图片路径正确
3. **任务失败**: 检查 `/api/status/{task_id}` 的error字段

### 技术支持
- 查看 `example_usage.py` 了解直接函数调用方式
- 查看 `README.md` 了解完整功能说明

# 生成英文Chapter
curl -X POST http://localhost:5002/api/generate/chapter \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The Future of Technology",
    "language": "english",
    "image_path": "assets/testing_image.jpeg"
  }'
```

## ⚠️ 重要说明

### 文件路径规则
- 所有路径都相对于API服务根目录
- Logo文件放在 `logos/` 目录
- 图片文件放在 `assets/` 目录  
- 生成结果保存在 `outputs/` 目录

### 输出文件命名
- 当前版本所有生成结果都会覆盖 `final_test.jpg`
- 这样便于快速查看最新生成效果
- 如需保留历史文件，请在生成后手动复制

### 处理逻辑
1. **图片自动处理**: 右侧图片会自动转换为正方形并缩放到900x900
2. **字体自动选择**: 根据文本语言自动选择最佳字体
3. **文字自动换行**: 超过620px宽度自动换行
4. **Logo自动缩放**: 保持宽高比适应Logo区域

## 🚨 错误码说明

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 参数错误 | 检查请求JSON格式和必填参数 |
| 404 | 文件不存在 | 检查文件路径是否正确 |
| 500 | 服务器内部错误 | 检查服务日志，可能是字体或模板文件问题 |