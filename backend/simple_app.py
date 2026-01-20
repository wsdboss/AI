import sys
import os
import time
import logging

# 导入配置
import config

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# 移除对flask_executor的依赖
# from flask_executor import Executor
import sqlite3
import uuid
import re
from datetime import datetime
import json
import signal

# 配置日志 - 添加日志轮转
import logging.handlers

# 确保日志目录存在
LOG_DIR = os.path.dirname(config.LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

# 配置日志轮转处理器
log_handler = logging.handlers.RotatingFileHandler(
    config.LOG_FILE,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,          # 保留5个备份
    encoding='utf-8'
)

# 配置日志格式，使用UTF-8编码
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
log_handler.setFormatter(log_formatter)

# 配置控制台日志
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# 获取根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(getattr(logging, config.LOG_LEVEL))

# 清除默认处理器
root_logger.handlers.clear()

# 添加自定义处理器
root_logger.addHandler(log_handler)
root_logger.addHandler(console_handler)

# 创建应用日志记录器
logger = logging.getLogger(__name__)
logger.info("日志系统初始化完成")

# 导入异步解析函数
from async_parser import parse_file_async

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 移除Executor初始化
# executor = Executor(app)

# 确保JSON响应使用UTF-8编码
app.config['JSON_AS_ASCII'] = False

# 确保响应头包含正确的编码信息
from flask import make_response
@app.after_request
def add_encoding_header(response):
    if response.mimetype == 'application/json':
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# 数据库配置
DATABASE = config.DATABASE_PATH
UPLOAD_DIR = config.UPLOAD_FOLDER

# 添加配置
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH  # 文件大小限制
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# 请求超时处理
class RequestTimeout(Exception):
    pass

# 请求超时处理 - 仅在支持signal.SIGALRM的系统上启用
if hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm'):
    def timeout_handler(signum, frame):
        raise RequestTimeout("请求处理超时")

    @app.before_request
    def before_request():
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30秒超时
    @app.after_request
    def after_request(response):
        signal.alarm(0)  # 取消超时
        return response
else:
    # Windows系统不支持SIGALRM，跳过超时设置
    pass

# 前端资源目录处理
# 硬编码前端资源目录路径，确保使用恢复的v1.0.0版本
import os
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend'))
# 打印日志，确认前端目录
logger.info(f"使用前端资源目录: {FRONTEND_DIR}")
logger.info(f"前端目录是否存在: {os.path.exists(FRONTEND_DIR)}")
logger.info(f"index.html是否存在: {os.path.exists(os.path.join(FRONTEND_DIR, 'index.html'))}")
# 确保目录存在
os.makedirs(FRONTEND_DIR, exist_ok=True)

# 确保前端目录存在
if not os.path.exists(FRONTEND_DIR):
    # 尝试创建空目录
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    logger.warning(f"前端目录不存在，已创建空目录: {FRONTEND_DIR}")

# 验证前端目录中是否有index.html
INDEX_PATH = os.path.join(FRONTEND_DIR, 'index.html')
if not os.path.exists(INDEX_PATH):
    logger.warning(f"前端index.html文件不存在: {INDEX_PATH}")
    logger.info(f"当前BASE_DIR: {config.BASE_DIR}")
    logger.info(f"当前FRONTEND_DIR: {FRONTEND_DIR}")
    logger.info(f"目录内容: {os.listdir(config.BASE_DIR)}")

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 创建文件表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interface_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            size INTEGER NOT NULL,
            uploaded_at TEXT NOT NULL,
            parsed INTEGER DEFAULT 0
        )
    ''')
    
    # 添加新字段（如果不存在）
    try:
        cursor.execute('ALTER TABLE interface_files ADD COLUMN parsed_interfaces INTEGER DEFAULT 0')
        cursor.execute('ALTER TABLE interface_files ADD COLUMN parsed_params INTEGER DEFAULT 0')
        cursor.execute('ALTER TABLE interface_files ADD COLUMN parsed_responses INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        # 字段已经存在，跳过
        pass
    
    # 创建接口表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interfaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            method TEXT NOT NULL,
            description TEXT,
            file_id INTEGER NOT NULL,
            FOREIGN KEY (file_id) REFERENCES interface_files (id)
        )
    ''')
    
    # 创建参数表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interface_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            param_type TEXT NOT NULL,
            required INTEGER DEFAULT 1,
            description TEXT,
            example TEXT,
            interface_id INTEGER NOT NULL,
            FOREIGN KEY (interface_id) REFERENCES interfaces (id)
        )
    ''')
    
    # 创建响应字段表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interface_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            response_type TEXT NOT NULL,
            description TEXT,
            example TEXT,
            interface_id INTEGER NOT NULL,
            FOREIGN KEY (interface_id) REFERENCES interfaces (id)
        )
    ''')
    
    # 创建Mock配置表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mock_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interface_id INTEGER NOT NULL,
            enabled INTEGER DEFAULT 1,
            default_count INTEGER DEFAULT 10,
            FOREIGN KEY (interface_id) REFERENCES interfaces (id)
        )
    ''')
    
    # 创建请求日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interface_id INTEGER NOT NULL,
            method TEXT NOT NULL,
            path TEXT NOT NULL,
            params TEXT,
            headers TEXT,
            response_status INTEGER NOT NULL,
            response_body TEXT,
            execution_time REAL,
            request_time TEXT NOT NULL,
            FOREIGN KEY (interface_id) REFERENCES interfaces (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
logger.info("初始化数据库...")
try:
    init_db()
    logger.info("数据库初始化成功")
except Exception as e:
    logger.error(f"数据库初始化失败: {e}")
    sys.exit(1)

# 辅助函数：生成随机数据
def generate_mock_value(field_type):
    import random
    import string
    
    if field_type in ['java.lang.String', 'string', 'java.lang.Object']:
        return ''.join(random.choices(string.ascii_letters, k=10))
    elif field_type in ['java.lang.Integer', 'int', 'java.lang.Long', 'long']:
        return random.randint(0, 1000)
    elif field_type in ['java.lang.Boolean', 'boolean']:
        return random.choice([True, False])
    elif field_type in ['java.lang.Double', 'double', 'java.lang.Float', 'float', 'java.math.BigDecimal', 'decimal']:
        return round(random.uniform(0, 1000), 2)
    elif field_type in ['java.util.Date', 'date', 'java.time.LocalDate']:
        return datetime.now().strftime('%Y-%m-%d')
    elif field_type in ['java.util.List', 'list', 'java.util.ArrayList']:
        return [generate_mock_value('string') for _ in range(random.randint(1, 5))]
    elif field_type in ['java.util.Map', 'map', 'java.util.HashMap']:
        return {generate_mock_value('string'): generate_mock_value('string') for _ in range(random.randint(1, 3))}
    else:
        return 'mock_value'

# API路由：文件上传
@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    logger.info("收到文件上传请求")
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            logger.warning("文件上传请求中没有文件部分")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("没有选择要上传的文件")
            return jsonify({'error': 'No selected file'}), 400
        
        logger.info(f"开始上传文件: {file.filename}")
        
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # 保存文件
        file.save(file_path)
        logger.info(f"文件保存成功: {file_path}")
        
        # 创建文件记录到数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 创建文件记录
        uploaded_at = datetime.now().isoformat()
        
        # 根据文件类型设置解析状态
        file_ext = os.path.splitext(file.filename)[1].lower()
        supported_types = ['.json', '.md', '.txt', '.docx', '.xlsx', '.pdf', '.png', '.jpg', '.jpeg']
        parsed_status = 1 if file_ext in supported_types else 0
        
        logger.info(f"准备插入数据库，文件信息: filename={file.filename}, file_path={file_path}, file_type={file.content_type or 'application/octet-stream'}, size={os.path.getsize(file_path)}, uploaded_at={uploaded_at}, parsed={parsed_status}")
        
        # 先检查表结构
        cursor.execute("PRAGMA table_info(interface_files)")
        table_info = cursor.fetchall()
        logger.info(f"表结构: {table_info}")
        
        # 简化插入语句，只插入必要字段
        cursor.execute('''
            INSERT INTO interface_files (filename, file_path, file_type, size, uploaded_at, parsed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (file.filename, file_path, file.content_type or 'application/octet-stream', 
              os.path.getsize(file_path), uploaded_at, parsed_status))
        file_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        logger.info(f"文件记录已添加到数据库，文件ID: {file_id}")
        
        # 同步执行文件解析
        logger.info(f"准备执行文件解析，文件ID: {file_id}")
        # 执行文件解析
        parse_file_async(file_id, file_path, file.filename, file.content_type or 'application/octet-stream')
        logger.info(f"文件解析任务已执行，文件ID: {file_id}")
        
        # 立即返回成功响应，告知用户文件已上传，正在后台解析
        return jsonify({
            'id': file_id,
            'filename': file.filename,
            'file_path': file_path,
            'file_type': file.content_type or 'application/octet-stream', 
            'size': os.path.getsize(file_path),
            'uploaded_at': uploaded_at,
            'parsed': parsed_status,
            'parsed_interfaces': 0,
            'parsed_params': 0,
            'parsed_responses': 0,
            'message': f'文件上传成功，正在后台解析...'
        })
    except Exception as e:
        logger.error(f"文件上传处理失败: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        import traceback
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        # 清理资源
        try:
            if 'conn' in locals() and conn:
                conn.rollback()
                conn.close()
        except Exception as close_error:
            logger.error(f"关闭数据库连接失败: {close_error}")
        
        # 获取文件扩展名
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # 对于二进制文件，保留文件但标记为解析失败
        # 只删除文本文件的临时文件
        if 'file_path' in locals() and os.path.exists(file_path) and file_ext in ['.json', '.md', '.txt']:
            try:
                os.remove(file_path)
                logger.info(f"已删除临时文件: {file_path}")
            except Exception as remove_error:
                logger.error(f"删除临时文件失败: {remove_error}")
        
        # 根据文件类型生成不同的错误消息
        error_message = f'文件上传失败: {str(e)}'
        general_message = ''
        
        if file_ext in ['.docx', '.xlsx', '.pdf']:
            general_message = '文件上传失败。请检查文件是否损坏或格式是否正确。'
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            general_message = '文件上传失败。请检查图片质量或确保图片包含可识别的文本。'
        else:
            general_message = '文件上传失败。请检查文件格式是否正确。'
        
        return jsonify({
            'error': error_message,
            'message': general_message,
            'parsed': 0
        }), 500

# API路由：获取文件列表
@app.route('/api/files', methods=['GET'])
def get_files():
    file_id = request.args.get('file_id')
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='interface_files';")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            conn.close()
            logger.error("interface_files表不存在")
            return jsonify([])
        
        if file_id:
            cursor.execute('SELECT * FROM interface_files WHERE id = ?', (file_id,))
        else:
            cursor.execute('SELECT * FROM interface_files')
        
        files = cursor.fetchall()
        conn.close()
        
        result = []
        for file in files:
            result.append({
                'id': file[0],
                'filename': file[1],
                'file_path': file[2],
                'file_type': file[3],
                'size': file[4],
                'uploaded_at': file[5],
                'parsed': bool(file[6]),
                'parsed_interfaces': file[7],
                'parsed_params': file[8],
                'parsed_responses': file[9]
            })
        
        return jsonify(result)
    except Exception as e:
        # 记录错误日志
        logger.error(f"获取文件列表失败: {e}")
        # 返回空数组，避免前端显示无效数据
        return jsonify([])

# API路由：删除文件
@app.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 开始事务
    conn.execute('BEGIN TRANSACTION')
    
    try:
        # 获取文件路径，用于后续删除实际文件
        cursor.execute('SELECT file_path FROM interface_files WHERE id = ?', (file_id,))
        file = cursor.fetchone()
        if not file:
            conn.rollback()
            conn.close()
            return jsonify({'error': 'File not found'}), 404
        
        file_path = file[0]
        
        # 获取该文件关联的所有接口ID
        cursor.execute('SELECT id FROM interfaces WHERE file_id = ?', (file_id,))
        interface_ids = [row[0] for row in cursor.fetchall()]
        
        # 删除接口关联的数据
        if interface_ids:
            # 删除请求日志
            cursor.execute('DELETE FROM request_logs WHERE interface_id IN ({})'.format(','.join(['?'] * len(interface_ids))), interface_ids)
            # 删除Mock配置
            cursor.execute('DELETE FROM mock_configs WHERE interface_id IN ({})'.format(','.join(['?'] * len(interface_ids))), interface_ids)
            # 删除响应字段
            cursor.execute('DELETE FROM interface_responses WHERE interface_id IN ({})'.format(','.join(['?'] * len(interface_ids))), interface_ids)
            # 删除请求参数
            cursor.execute('DELETE FROM interface_params WHERE interface_id IN ({})'.format(','.join(['?'] * len(interface_ids))), interface_ids)
            # 删除接口
            cursor.execute('DELETE FROM interfaces WHERE file_id = ?', (file_id,))
        
        # 删除文件记录
        cursor.execute('DELETE FROM interface_files WHERE id = ?', (file_id,))
        
        # 提交事务
        conn.commit()
        conn.close()
        
        # 删除实际文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({'message': 'File deleted successfully', 'file_id': file_id})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

# API路由：下载文件
@app.route('/api/files/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 获取文件信息
    cursor.execute('SELECT filename, file_path FROM interface_files WHERE id = ?', (file_id,))
    file = cursor.fetchone()
    conn.close()
    
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    filename, file_path = file
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 404
    
    # 使用send_from_directory发送文件
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    return send_from_directory(directory, filename, as_attachment=True, download_name=file[0])

# API路由：获取上传目录的静态文件（用于图片预览）
@app.route('/uploads/<path:filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# API路由：获取接口列表
@app.route('/api/interfaces', methods=['GET'])
def get_interfaces():
    file_id = request.args.get('file_id')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 检查文件是否存在
        if file_id:
            cursor.execute('SELECT id FROM interface_files WHERE id = ?', (file_id,))
            file_exists = cursor.fetchone()
            if not file_exists:
                return jsonify([])
            
            # 调试信息
            print(f"获取文件 {file_id} 的接口列表")
            cursor.execute('SELECT * FROM interfaces WHERE file_id = ?', (file_id,))
        else:
            # 调试信息
            print("获取所有接口列表")
            cursor.execute('SELECT * FROM interfaces')
        
        interfaces = cursor.fetchall()
        
        # 调试信息
        print(f"查询到 {len(interfaces)} 个接口")
        
        result = []
        for interface in interfaces:
            result.append({
                'id': interface[0],
                'name': interface[1],
                'path': interface[2],
                'method': interface[3],
                'description': interface[4],
                'file_id': interface[5]
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"获取接口列表失败: {e}")
        return jsonify([])
    finally:
        conn.close()

# API路由：获取接口参数
@app.route('/api/interfaces/<int:interface_id>/params', methods=['GET'])
def get_interface_params(interface_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interface_params WHERE interface_id = ?', (interface_id,))
    params = cursor.fetchall()
    conn.close()
    
    result = []
    for param in params:
        result.append({
            'id': param[0],
            'name': param[1],
            'param_type': param[2],
            'required': bool(param[3]),
            'description': param[4],
            'example': param[5],
            'interface_id': param[6]
        })
    
    # 如果没有参数，返回默认参数
    if len(result) == 0:
        result = [
            {'id': 0, 'name': 'id', 'param_type': 'string', 'required': True, 'description': '唯一标识符', 'example': '123456', 'interface_id': interface_id},
            {'id': 0, 'name': 'page', 'param_type': 'int', 'required': False, 'description': '页码', 'example': '1', 'interface_id': interface_id},
            {'id': 0, 'name': 'page_size', 'param_type': 'int', 'required': False, 'description': '每页条数', 'example': '10', 'interface_id': interface_id}
        ]
    
    return jsonify(result)

# API路由：获取接口响应字段
@app.route('/api/interfaces/<int:interface_id>/responses', methods=['GET'])
def get_interface_responses(interface_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interface_responses WHERE interface_id = ?', (interface_id,))
    responses = cursor.fetchall()
    conn.close()
    
    result = []
    for response in responses:
        result.append({
            'id': response[0],
            'name': response[1],
            'response_type': response[2],
            'description': response[3],
            'example': response[4],
            'interface_id': response[5]
        })
    
    # 如果没有响应字段，返回默认响应字段
    if len(result) == 0:
        result = [
            {'id': 0, 'name': 'code', 'response_type': 'int', 'description': '响应码', 'example': '0', 'interface_id': interface_id},
            {'id': 0, 'name': 'message', 'response_type': 'string', 'description': '响应消息', 'example': 'success', 'interface_id': interface_id},
            {'id': 0, 'name': 'data', 'response_type': 'object', 'description': '响应数据', 'example': '{}', 'interface_id': interface_id},
            {'id': 0, 'name': 'timestamp', 'response_type': 'string', 'description': '时间戳', 'example': '2023-01-01 12:00:00', 'interface_id': interface_id}
        ]
    
    return jsonify(result)

# API路由：获取Mock配置
@app.route('/api/interfaces/<int:interface_id>/mock-config', methods=['GET'])
def get_mock_config(interface_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 查询Mock配置
    cursor.execute('SELECT * FROM mock_configs WHERE interface_id = ?', (interface_id,))
    mock_config = cursor.fetchone()
    
    conn.close()
    
    if mock_config:
        return jsonify({
            'enabled': bool(mock_config[2]),
            'default_count': mock_config[3]
        })
    else:
        # 返回默认配置
        return jsonify({
            'enabled': True,
            'default_count': 10
        })

# API路由：保存Mock配置
@app.route('/api/interfaces/<int:interface_id>/mock', methods=['POST'])
def save_mock_config(interface_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        data = request.get_json()
        enabled = 1 if data.get('enabled', True) else 0
        default_count = int(data.get('default_count', 10))
        
        # 检查Mock配置是否存在
        cursor.execute('SELECT * FROM mock_configs WHERE interface_id = ?', (interface_id,))
        mock_config = cursor.fetchone()
        
        if mock_config:
            # 更新现有配置
            cursor.execute('''
                UPDATE mock_configs 
                SET enabled = ?, default_count = ? 
                WHERE interface_id = ?
            ''', (enabled, default_count, interface_id))
        else:
            # 创建新配置
            cursor.execute('''
                INSERT INTO mock_configs (interface_id, enabled, default_count)
                VALUES (?, ?, ?)
            ''', (interface_id, enabled, default_count))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Mock配置保存成功',
            'mock_config': {
                'enabled': bool(enabled),
                'default_count': default_count
            }
        })
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

# API路由：更新Mock配置（PUT方法）
@app.route('/api/interfaces/<int:interface_id>/mock-config', methods=['PUT'])
def update_mock_config(interface_id):
    # 复用save_mock_config逻辑
    return save_mock_config(interface_id)

# API路由：生成接口服务
@app.route('/api/interfaces/generate/<int:interface_id>', methods=['POST'])
def generate_interface(interface_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 检查是否已经生成过Mock配置
    cursor.execute('SELECT * FROM mock_configs WHERE interface_id = ?', (interface_id,))
    mock_config = cursor.fetchone()
    
    if not mock_config:
        # 创建默认Mock配置
        cursor.execute('''
            INSERT INTO mock_configs (interface_id, enabled, default_count)
            VALUES (?, ?, ?)
        ''', (interface_id, 1, 10))
        conn.commit()
        # 重新查询获取刚刚插入的记录
        cursor.execute('SELECT * FROM mock_configs WHERE interface_id = ?', (interface_id,))
        mock_config = cursor.fetchone()
    
    # 获取接口信息
    cursor.execute('SELECT * FROM interfaces WHERE id = ?', (interface_id,))
    interface = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': '接口服务生成成功',
        'interface_id': interface_id,
        'interface_name': interface[1],
        'interface_path': interface[2],
        'interface_method': interface[3],
        'mock_config': {
            'enabled': bool(mock_config[2]),
            'default_count': mock_config[3]
        },
        'doc_generated': True
    })

# API路由：动态接口请求
@app.route('/api/dynamic/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def dynamic_interface(path):
    full_path = f"/{path}"
    method = request.method
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 查找匹配的接口
    cursor.execute('''
        SELECT * FROM interfaces WHERE path = ? AND method = ?
    ''', (full_path, method))
    interface = cursor.fetchone()
    
    if not interface:
        conn.close()
        return jsonify({
            'code': 404,
            'message': f'接口 {method} {full_path} 不存在',
            'data': None
        })
    
    # 获取Mock配置
    cursor.execute('SELECT * FROM mock_configs WHERE interface_id = ?', (interface[0],))
    mock_config = cursor.fetchone()
    
    if not mock_config or not mock_config[2]:
        conn.close()
        return jsonify({
            'code': 500,
            'message': '该接口的Mock服务未启用',
            'data': None
        })
    
    # 获取请求参数
    params = {}
    mock_count = mock_config[3]
    
    # 解析请求参数
    if method == 'GET':
        # 处理GET请求参数
        get_params = request.args.to_dict()
        
        # 提取并解析params
        if 'params' in get_params:
            try:
                params = json.loads(get_params['params'])
            except json.JSONDecodeError:
                params = {}
    else:
        # 处理非GET请求
        try:
            request_data = request.get_json() or {}
            params = request_data.get('params', {})
        except:
            params = {}
    
    # 获取响应字段
    cursor.execute('SELECT * FROM interface_responses WHERE interface_id = ?', (interface[0],))
    response_fields = cursor.fetchall()
    
    conn.close()
    
    # 生成Mock数据
    mock_data = []
    for _ in range(mock_count):
        data = {}
        if response_fields:
            for field in response_fields:
                data[field[1]] = generate_mock_value(field[2])
        else:
            # 如果没有响应字段，生成默认的mock数据
            data['id'] = str(uuid.uuid4())
            data['message'] = f'Success response from {full_path}'
            data['status'] = 'success'
            data['timestamp'] = datetime.now().isoformat()
            data['random_data'] = generate_mock_value('string')
            data['random_number'] = generate_mock_value('int')
            data['random_boolean'] = generate_mock_value('boolean')
        mock_data.append(data)
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': mock_data
    })

# 健康检查路由
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'app': '动态接口生成工具',
        'version': '1.0.0'
    })

# 调试端点
@app.route('/debug', methods=['GET'])
def debug_info():
    return jsonify({
        'base_dir': config.BASE_DIR,
        'frontend_dir': FRONTEND_DIR,
        'frontend_exists': os.path.exists(FRONTEND_DIR),
        'index_exists': os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')),
        'app_version': config.APP_VERSION
    })

# 前端资源路由
@app.route('/')
def index():
    """返回首页"""
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIR, 'index.html')
    else:
        return jsonify({
            'status': 'error',
            'message': '前端资源未找到，请确保已正确构建前端项目',
            'version': '1.0.0'
        })

# 静态文件路由
@app.route('/<path:filename>')
def static_files(filename):
    """返回静态文件，支持SPA路由"""
    file_path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, filename)
    # 对所有找不到的文件请求返回index.html，用于SPA路由
    # 这确保前端路由系统能接管处理所有路由
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIR, 'index.html')
    # 如果index.html也找不到，返回错误
    return jsonify({
        'status': 'error',
        'message': f'前端资源未找到，请确保已正确构建前端项目',
        'version': '1.0.0'
    })

# 命令行参数处理
import argparse

import webbrowser
import threading
import time

def open_browser(host, port):
    """自动打开浏览器"""
    try:
        # 将0.0.0.0转换为localhost，便于浏览器访问
        browser_host = host if host != '0.0.0.0' else 'localhost'
        url = f'http://{browser_host}:{port}'
        # 等待服务器启动（给3秒延迟）
        time.sleep(3)
        # 使用默认浏览器打开
        webbrowser.open(url)
        logger.info(f"已自动打开浏览器，访问地址: {url}")
    except Exception as e:
        logger.error(f"自动打开浏览器失败: {e}")
        # 提示信息也使用转换后的地址
        browser_host = host if host != '0.0.0.0' else 'localhost'
        print(f"自动打开浏览器失败，请手动访问 http://{browser_host}:{port}")

# 端口可用性检测函数
def is_port_available(port, host='0.0.0.0'):
    """
    检测指定端口是否可用
    :param port: 要检测的端口
    :param host: 要检测的主机，默认0.0.0.0
    :return: 端口是否可用，可用返回True，否则返回False
    """
    import socket
    try:
        # 创建socket对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 设置超时时间为1秒
            s.settimeout(1)
            # 尝试绑定端口
            s.bind((host, port))
            return True
    except (socket.error, OSError):
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='动态接口生成工具')
    parser.add_argument('--port', type=int, default=config.MOCK_SERVER_PORT, help='服务器端口，默认8000')
    parser.add_argument('--host', type=str, default=config.MOCK_SERVER_HOST, help='服务器主机，默认0.0.0.0')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    args = parser.parse_args()
    
    # 检测指定端口是否可用，如果不可用，自动寻找下一个可用端口
    original_port = args.port
    max_attempts = 100  # 最多尝试100个端口
    for attempt in range(max_attempts):
        if is_port_available(args.port, args.host):
            # 端口可用，使用该端口
            break
        else:
            # 端口不可用，尝试下一个端口
            logger.warning(f"端口 {args.port} 已被占用，尝试下一个可用端口")
            print(f"端口 {args.port} 已被占用，尝试下一个可用端口...")
            args.port += 1
    
    # 如果尝试了max_attempts个端口都不可用，退出应用
    if attempt >= max_attempts - 1 and not is_port_available(args.port, args.host):
        logger.error(f"无法找到可用端口，已尝试从 {original_port} 到 {args.port} 共 {max_attempts} 个端口")
        print(f"无法找到可用端口，已尝试从 {original_port} 到 {args.port} 共 {max_attempts} 个端口")
        sys.exit(1)
    
    # 如果使用了不同的端口，打印提示信息
    if args.port != original_port:
        logger.info(f"已切换到可用端口 {args.port}")
        print(f"已切换到可用端口 {args.port}\n")
    
    # 启动应用前先打印访问地址
    access_url = f'http://{args.host}:{args.port}'
    logger.info(f"应用即将启动，访问地址: {access_url}")
    print(f"\n应用即将启动...")
    print(f"访问地址: {access_url}")
    print(f"按 Ctrl+C 停止应用\n")
    
    # 自动打开浏览器（使用线程，避免阻塞）
    if not args.no_browser:
        # 使用线程打开浏览器，在服务器启动后3秒打开
        browser_thread = threading.Thread(target=open_browser, args=(args.host, args.port))
        browser_thread.daemon = True  # 设置为守护线程，随主线程退出而退出
        browser_thread.start()
    
    # 启动应用，确保使用正确的参数
    print(f"启动应用，监听 {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False, use_reloader=False, threaded=True, use_debugger=False)
