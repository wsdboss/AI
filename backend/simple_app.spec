# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 读取版本信息
import os
import sys
version = "1.0.0"

# 定义资源文件
added_files = [
    ('uploads', 'uploads'),
    ('frontend', 'frontend'),
    # 添加空目录，确保应用运行时能正常创建
    ('backups', 'backups'),
    ('templates', 'templates'),
    ('i18n', 'i18n'),
    ('plugins', 'plugins'),
]

# 定义隐藏导入
hidden_imports = [
    # 基础库
    'sqlite3',
    'uuid',
    're',
    'datetime',
    'json',
    'signal',
    'sys',
    'os',
    'time',
    'asyncio',
    'concurrent.futures',
    'logging',
    
    # Flask相关依赖
    'flask',
    'flask_cors',
    'flask_executor',
    'werkzeug',
    'jinja2',
    'markupsafe',
    'itsdangerous',
    'click',
    'colorama',
    'blinker',
    
    # 文件处理库
    'docx',
    'openpyxl',
    'PyPDF2',
    'PIL',
    'pytesseract',
    'markdown',
    'lxml',
    'et_xmlfile',
    'jdcal',
    
    # 其他必要依赖
    'requests',
    'pydantic',
    'typing_extensions',
    'packaging',
    'charset_normalizer',
    'certifi',
    'idna',
]

a = Analysis(
    ['simple_app.py', 'async_parser.py', 'config.py'],
    # 添加当前目录到搜索路径
    pathex=[os.getcwd()],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不必要的模块，减少打包体积
        'tkinter',
        'test',
        'unittest',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Windows 配置
if os.name == 'nt':
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='InterfaceGenerator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        # 禁用upx以避免兼容性问题
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,  # 修改为控制台模式，以便查看错误信息
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,
    )
# macOS 配置
elif os.name == 'posix' and 'darwin' in sys.platform:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='InterfaceGenerator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,
    )
    app = BUNDLE(
        exe,
        name='InterfaceGenerator.app',
        icon=None,
        bundle_identifier=None,
    )
# Linux 配置
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='interface-generator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
    )