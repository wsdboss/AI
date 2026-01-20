#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time

# 启动命令
cmd = ['python', 'backend/simple_app.py', '--port', '8000', '--host', '127.0.0.1', '--no-browser']

# 启动进程
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# 实时输出
print("启动服务...")
time.sleep(1)

# 读取输出
for line in process.stdout:
    print(line.strip())

# 等待进程结束
process.wait()
print(f"服务退出，返回码: {process.returncode}")