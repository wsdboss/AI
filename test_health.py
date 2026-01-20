#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time


def test_health():
    """测试健康检查端点"""
    url = "http://127.0.0.1:8000/health"
    
    print(f"正在测试健康检查端点: {url}")
    
    try:
        # 设置超时时间为5秒
        response = requests.get(url, timeout=5)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("健康检查通过!")
            return True
        else:
            print(f"健康检查失败，状态码: {response.status_code}")
            return False
    except requests.ConnectionError as e:
        print(f"连接错误: {e}")
        return False
    except requests.Timeout as e:
        print(f"请求超时: {e}")
        return False
    except Exception as e:
        print(f"其他错误: {e}")
        return False


if __name__ == '__main__':
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(3)
    
    # 测试健康检查
    test_health()