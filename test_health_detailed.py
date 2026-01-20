#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import socket


def test_socket_connection():
    """测试socket连接"""
    print("测试socket连接...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = sock.connect_ex(('127.0.0.1', 8000))
        if result == 0:
            print("✓ Socket连接成功")
            return True
        else:
            print(f"✗ Socket连接失败，错误码: {result}")
            return False
    except Exception as e:
        print(f"✗ Socket连接出错: {e}")
        return False
    finally:
        sock.close()


def test_http_request():
    """测试HTTP请求"""
    print("\n测试HTTP请求...")
    url = "http://127.0.0.1:8000/health"
    
    try:
        # 设置超时时间为5秒
        response = requests.get(url, timeout=5)
        print(f"✓ HTTP请求成功，状态码: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
        print(f"  响应内容: {response.text}")
        return True
    except requests.ConnectionError as e:
        print(f"✗ 连接错误: {e}")
        return False
    except requests.Timeout as e:
        print(f"✗ 请求超时: {e}")
        return False
    except Exception as e:
        print(f"✗ 其他错误: {e}")
        return False


def test_get_files():
    """测试获取文件列表"""
    print("\n测试获取文件列表...")
    url = "http://127.0.0.1:8000/api/files"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ 获取文件列表成功，状态码: {response.status_code}")
        print(f"  响应内容: {response.text}")
        return True
    except Exception as e:
        print(f"✗ 获取文件列表失败: {e}")
        return False


if __name__ == '__main__':
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(3)
    
    # 测试socket连接
    socket_ok = test_socket_connection()
    
    # 测试HTTP请求
    http_ok = test_http_request()
    
    # 测试获取文件列表
    files_ok = test_get_files()
    
    # 总结
    print("\n=== 测试总结 ===")
    print(f"Socket连接: {'成功' if socket_ok else '失败'}")
    print(f"HTTP健康检查: {'成功' if http_ok else '失败'}")
    print(f"获取文件列表: {'成功' if files_ok else '失败'}")
    
    if socket_ok and http_ok and files_ok:
        print("\n✅ 所有测试通过，服务运行正常!")
    else:
        print("\n❌ 部分测试失败，服务可能存在问题!")