#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置文件
用于管理应用的各种配置参数
"""

import os
import sys
import json

# 应用基本信息
APP_NAME = "Interface Generator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "动态接口生成工具，支持多种文件格式解析"

# 获取当前目录
if getattr(sys, 'frozen', False):
    # 打包后运行
    BASE_DIR = os.path.dirname(sys.executable)
    # 确保必要目录存在
    for dir_name in ['uploads', 'backups', 'templates', 'i18n', 'plugins']:
        os.makedirs(os.path.join(BASE_DIR, dir_name), exist_ok=True)
else:
    # 开发模式运行
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE_PATH = os.path.join(BASE_DIR, 'api_generator.db')

# 文件上传配置
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# 支持的文件类型
SUPPORTED_TEXT_TYPES = ['.json', '.md', '.txt']
SUPPORTED_BINARY_TYPES = ['.docx', '.xlsx', '.pdf', '.png', '.jpg', '.jpeg']
SUPPORTED_FILE_TYPES = SUPPORTED_TEXT_TYPES + SUPPORTED_BINARY_TYPES

# 服务器配置
HOST = '127.0.0.1'
PORT = 5000
DEBUG = False  # 生产环境设置为False

# 前端配置
FRONTEND_FOLDER = os.path.join(BASE_DIR, 'frontend')

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(BASE_DIR, 'app.log')

# 确保日志目录存在
LOG_DIR = os.path.dirname(LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

# OCR配置（用于图片文字识别）
TESSERACT_CMD = None  # 自动检测，可手动指定路径

# 文件解析配置
MAX_PARSE_LINES = 10000  # 最大解析行数
MAX_PARSE_SIZE = 10 * 1024 * 1024  # 10MB

# Mock服务配置
MOCK_SERVER_PORT = 8000
MOCK_SERVER_HOST = '0.0.0.0'

# 生成接口配置
GENERATE_INTERFACE_TIMEOUT = 30  # 生成接口超时时间（秒）

# 安全配置
ALLOWED_ORIGINS = ['*']  # 允许的跨域来源
SECRET_KEY = 'your-secret-key-here'  # 用于会话管理和加密

# 自动备份配置
AUTO_BACKUP_ENABLED = False
BACKUP_INTERVAL = 24 * 60 * 60  # 24小时
BACKUP_FOLDER = os.path.join(BASE_DIR, 'backups')

# 清理配置
AUTO_CLEANUP_ENABLED = False
CLEANUP_INTERVAL = 7 * 24 * 60 * 60  # 7天
CLEANUP_OLDER_THAN = 30 * 24 * 60 * 60  # 30天

# 通知配置
NOTIFY_ENABLED = False
NOTIFY_EMAIL = None

# 语言配置
LANGUAGE = 'zh_CN'

# 主题配置
THEME = 'light'  # light, dark, auto

# 快捷键配置
KEYBOARD_SHORTCUTS = {
    'upload_file': 'Ctrl+U',
    'refresh_files': 'Ctrl+R',
    'generate_interfaces': 'Ctrl+G',
    'clear_all': 'Ctrl+Shift+C',
    'exit_app': 'Ctrl+Q',
}

# 性能优化配置
CACHE_ENABLED = True
CACHE_TIMEOUT = 3600  # 1小时

# 调试配置
DEBUG_MODE = False
DEBUG_LOG_ENABLED = False

# 自动更新配置
AUTO_UPDATE_ENABLED = False
UPDATE_CHECK_INTERVAL = 24 * 60 * 60  # 24小时

# 统计配置
STATISTICS_ENABLED = False
STATISTICS_SERVER = None

# 插件配置
PLUGINS_ENABLED = False
PLUGINS_FOLDER = os.path.join(BASE_DIR, 'plugins')

# 导出配置
EXPORT_FORMATS = ['json', 'yaml', 'markdown']

# 导入配置
IMPORT_FORMATS = ['json', 'yaml', 'openapi']

# 模板配置
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
DEFAULT_TEMPLATE = 'default'

# 验证配置
VALIDATION_ENABLED = True
VALIDATION_STRICTNESS = 'medium'  # low, medium, high

# 国际化配置
I18N_ENABLED = True
I18N_FOLDER = os.path.join(BASE_DIR, 'i18n')

# 帮助配置
HELP_URL = 'https://github.com/yourusername/interface-generator/wiki'
DOCS_URL = 'https://github.com/yourusername/interface-generator/blob/main/PROJECT_STRUCTURE.md'

# 反馈配置
FEEDBACK_URL = 'https://github.com/yourusername/interface-generator/issues'

# 关于配置
ABOUT_URL = 'https://github.com/yourusername/interface-generator'
LICENSE_URL = 'https://github.com/yourusername/interface-generator/blob/main/LICENSE'

# 版权配置
COPYRIGHT = f"© 2026 {APP_NAME}. All rights reserved."

# 依赖检查配置
DEPENDENCY_CHECK_ENABLED = True
DEPENDENCY_CHECK_URL = None

# 系统配置
SYSTEM_CONFIG = {
    'max_processes': 4,
    'max_threads': 8,
    'memory_limit': None,
    'cpu_limit': None,
}

# 自定义配置
CUSTOM_CONFIG = {}

# 加载自定义配置
def load_custom_config(config_path=None):
    """加载自定义配置"""
    global CUSTOM_CONFIG
    
    if config_path is None:
        config_path = os.path.join(BASE_DIR, 'config_custom.py')
    
    if os.path.exists(config_path):
        try:
            # 动态导入自定义配置
            import importlib.util
            spec = importlib.util.spec_from_file_location("config_custom", config_path)
            config_module = importlib.util.module_from_spec(spec)
            sys.modules["config_custom"] = config_module
            spec.loader.exec_module(config_module)
            
            # 更新全局配置
            for key in dir(config_module):
                if not key.startswith('_'):
                    globals()[key] = getattr(config_module, key)
                    CUSTOM_CONFIG[key] = getattr(config_module, key)
            
            print(f"自定义配置加载成功: {config_path}")
            return True
        except Exception as e:
            print(f"自定义配置加载失败: {e}")
            print(f"使用默认配置继续运行")
            return False
    return False

# 配置文件处理
# 支持多种配置文件格式
CONFIG_FORMATS = ['py', 'json']

# 保存配置
def save_config(config_data, config_path=None, config_format='py'):
    """保存配置到文件"""
    if config_path is None:
        config_path = os.path.join(BASE_DIR, f'config_custom.{config_format}')
    
    try:
        if config_format == 'py':
            # 保存为Python文件格式 - 简化格式，避免中文注释问题
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("# Configuration file for Interface Generator\n")
                f.write("# This file was automatically generated\n")
                f.write("\n")
                
                for key, value in config_data.items():
                    if key in globals() and not key.startswith('_'):
                        f.write(f"{key} = {repr(value)}\n")
        elif config_format == 'json':
            # 保存为JSON文件格式
            with open(config_path, 'w', encoding='utf-8') as f:
                # 只保存非私有配置项
                config_to_save = {}
                for key, value in config_data.items():
                    if key in globals() and not key.startswith('_'):
                        config_to_save[key] = value
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
        
        print(f"配置保存成功: {config_path}")
        return True
    except Exception as e:
        print(f"配置保存失败: {e}")
        return False

# 加载JSON配置文件
def load_json_config(config_path):
    """加载JSON格式的配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            
        # 更新全局配置
        for key, value in config_data.items():
            if key in globals() and not key.startswith('_'):
                globals()[key] = value
                CUSTOM_CONFIG[key] = value
        
        print(f"JSON配置加载成功: {config_path}")
        return True
    except Exception as e:
        print(f"JSON配置加载失败: {e}")
        return False

# 初始化配置
def init_config():
    """初始化配置"""
    # 确保必要的目录存在
    for folder in [UPLOAD_FOLDER, BACKUP_FOLDER, PLUGINS_FOLDER, TEMPLATE_FOLDER, I18N_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
    
    # 加载自定义配置 - 支持多种格式
    custom_config_loaded = False
    
    # 优先加载Python格式配置
    for fmt in CONFIG_FORMATS:
        config_path = os.path.join(BASE_DIR, f'config_custom.{fmt}')
        if os.path.exists(config_path):
            if fmt == 'py':
                custom_config_loaded = load_custom_config(config_path)
            elif fmt == 'json':
                custom_config_loaded = load_json_config(config_path)
            
            if custom_config_loaded:
                break
    
    # 如果没有加载到自定义配置，创建一个示例配置文件
    if not custom_config_loaded:
        example_config = {
            'HOST': HOST,
            'PORT': PORT,
            'MOCK_SERVER_HOST': MOCK_SERVER_HOST,
            'MOCK_SERVER_PORT': MOCK_SERVER_PORT,
            'LOG_LEVEL': LOG_LEVEL,
            'MAX_CONTENT_LENGTH': MAX_CONTENT_LENGTH
        }
        
        # 创建示例配置文件
        save_config(example_config, os.path.join(BASE_DIR, 'config_custom.py'), 'py')
        print("已创建示例配置文件: config_custom.py")

# 调用初始化函数
init_config()