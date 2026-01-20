#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_start.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def start_server():
    logger.info("准备启动后端服务...")
    
    # 定义启动命令
    import os
    # 获取脚本所在目录的父目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    simple_app_path = os.path.join(base_dir, 'backend', 'simple_app.py')
    
    command = [
        sys.executable,
        simple_app_path,
        '--port', '8000',
        '--host', '127.0.0.1',
        '--no-browser'
    ]
    
    logger.info(f"执行命令: {' '.join(command)}")
    
    try:
        # 启动进程
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        logger.info(f"服务已启动，PID: {process.pid}")
        
        # 实时输出日志
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logger.info(output.strip())
        
        # 获取错误输出
        stderr = process.stderr.read()
        if stderr:
            logger.error(f"服务错误输出: {stderr}")
        
        # 获取返回码
        return_code = process.poll()
        logger.info(f"服务已退出，返回码: {return_code}")
        
        return return_code
    except Exception as e:
        logger.error(f"启动服务时出错: {e}")
        return 1

if __name__ == '__main__':
    start_server()