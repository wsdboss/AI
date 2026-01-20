# 动态接口生成工具

一款功能强大的动态接口生成工具，支持多种文件格式解析，自动生成Mock接口服务。

## 🚀 功能特性

### 🔹 多文件类型支持
- ✅ JSON规范文件
- ✅ Markdown文档
- ✅ 纯文本文件
- ✅ Word文档（.docx）
- ✅ Excel表格（.xlsx）
- ✅ PDF文档
- ✅ 图片文件（PNG/JPG/JPEG）

### 🔹 核心功能
- 📁 **文件上传管理**：支持多文件上传，自动解析内容
- 🔍 **智能接口提取**：从文件中自动提取接口定义
- 📋 **接口管理**：直观的接口列表和详情展示
- 🎯 **Mock服务生成**：一键生成可配置的Mock接口
- 📊 **解析结果统计**：详细的接口、参数统计信息
- 👁️ **文件预览**：现代化的文件预览和解析结果展示
- 🔄 **实时刷新**：参数变化时自动更新界面
- 📱 **响应式设计**：适配不同设备和屏幕尺寸

### 🔹 技术优势
- ⚡ 高性能：优化的文件解析和数据库操作
- 🛡️ 安全可靠：完善的错误处理和数据验证
- 📖 清晰的文档：详细的项目结构和使用说明
- 🔧 易于扩展：模块化设计，支持新功能扩展
- 🖥️ 友好的UI：现代化的用户界面设计

## 📋 快速开始

### 环境要求

- **Python**: 3.7+
- **Node.js**: 14+ (仅用于前端开发)

### 安装方法

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/interface-generator.git
cd interface-generator
```

#### 2. 虚拟环境配置

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 安装依赖
pip install -r backend/simple_requirements.txt
```

#### 3. 启动应用

##### 方法1：直接运行后端服务

```bash
python backend/simple_app.py
```

##### 方法2：使用命令行工具

```bash
python backend/cli.py start
```

##### 方法3：使用图形界面

```bash
python backend/gui.py
```

#### 4. 访问应用

服务启动后，在浏览器中访问：
```
http://localhost:8000
```

## 📖 使用指南

### 1. 文件上传

1. 点击左侧面板的"上传文档"按钮
2. 选择要上传的文件（支持多种格式）
3. 等待文件上传和解析完成
4. 在左侧文件列表中查看上传的文件

### 2. 接口管理

1. 点击文件查看解析到的接口
2. 点击接口卡片查看接口详情
3. 在右侧面板中配置Mock服务
4. 使用接口调试功能测试接口

### 3. Mock服务配置

1. 在接口详情页，点击"Mock服务配置"
2. 启用/禁用Mock服务
3. 设置默认返回数据条数
4. 配置请求参数和响应格式

### 4. 文件预览

1. 点击文件列表中的预览按钮
2. 查看文件详情和解析结果
3. 可以选择下载文件
4. 查看解析统计信息

## 📦 打包部署

### 使用PyInstaller打包

```bash
# 进入后端目录
cd backend

# 打包应用
pyinstaller simple_app.spec
```

### 打包后运行

1. 进入`dist`目录
2. 双击运行`InterfaceGenerator.exe`（Windows）
3. 或使用命令行运行：`./InterfaceGenerator`（Linux/macOS）

## 🛠️ 技术栈

| 类别 | 技术/框架 | 用途 |
|------|-----------|------|
| 后端 | Flask | Web框架 |
| 后端 | SQLite | 数据库 |
| 后端 | python-docx | DOCX文件解析 |
| 后端 | openpyxl | XLSX文件解析 |
| 后端 | PyPDF2 | PDF文件解析 |
| 后端 | Pillow | 图像处理 |
| 后端 | pytesseract | OCR文字识别 |
| 前端 | HTML5 + CSS3 + JavaScript | 前端界面 |
| 前端 | Vue.js | 前端框架 |
| 前端 | Element UI | UI组件库 |

## 📁 项目结构

```
interface-generator/
├── backend/             # 后端代码
│   ├── simple_app.py    # 主应用入口
│   ├── cli.py           # 命令行工具
│   ├── gui.py           # 图形界面
│   ├── config.py        # 配置文件
│   ├── init_db.py       # 数据库初始化
│   └── uploads/         # 文件上传目录
├── frontend/            # 前端代码
│   ├── dist/            # 构建后的前端资源
│   ├── src/             # 源代码
│   └── index.html       # 入口HTML
├── CHANGELOG.md         # 版本更新记录
├── PROJECT_STRUCTURE.md # 项目结构说明
└── README.md            # 项目说明文档
```

## 🎯 命令行工具

### 基本命令

```bash
# 查看版本
python backend/cli.py --version

# 启动服务器
python backend/cli.py start

# 启动服务器（不自动打开浏览器）
python backend/cli.py start --no-browser

# 指定端口启动
python backend/cli.py start --port 5000

# 初始化数据库
python backend/cli.py init-db

# 处理单个文件
python backend/cli.py process your-file.json --format yaml
```

### 配置命令

```bash
# 列出所有配置项
python backend/cli.py config --list

# 设置配置项
python backend/cli.py config HOST 0.0.0.0
```

## 🖥️ 图形界面

### 主要功能

1. **服务器配置**：主机、端口、调试模式设置
2. **启动控制**：一键启动/停止服务器
3. **状态监控**：实时显示服务器状态和日志
4. **快捷操作**：打开Web界面、初始化数据库
5. **日志查看**：实时查看服务器运行日志

## 🔧 配置文件

### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| HOST | 127.0.0.1 | 服务器主机地址 |
| PORT | 5000 | 服务器端口 |
| DEBUG | False | 是否启用调试模式 |
| UPLOAD_FOLDER | uploads | 文件上传目录 |
| MAX_CONTENT_LENGTH | 50MB | 最大文件大小 |
| DATABASE_PATH | api_generator.db | 数据库路径 |

### 自定义配置

创建`backend/config_custom.py`文件，覆盖默认配置：

```python
# 示例：自定义配置
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False
```

## 📋 开发说明

### 前端开发

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve

# 构建生产版本
npm run build
```

### 后端开发

```bash
# 安装开发依赖
pip install -r backend/requirements.txt

# 运行后端服务
python backend/simple_app.py
```

## 🧪 测试

### 运行测试

```bash
# 运行文件上传测试
python test_upload.py

# 运行Markdown文件测试
python test_markdown_upload.py

# 运行JSON文件测试
python test_json_upload.py
```

### 测试文件

测试文件位于`test_files/`目录：
- `test_interface.md`：Markdown格式接口文档
- `test_swagger.json`：Swagger 2.0规范
- `test_openapi3.json`：OpenAPI 3.0规范

## 📝 版本更新

详细版本更新记录请查看 [CHANGELOG.md](CHANGELOG.md)

## 🏗️ 项目结构

详细项目结构说明请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

- 📧 邮箱：your-email@example.com
- 📱 项目地址：https://github.com/yourusername/interface-generator

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**动态接口生成工具** - 让接口开发更简单！ 🚀
