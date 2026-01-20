import requests
import os
import json

# 测试文件上传功能
def test_markdown_upload():
    print("=== 测试Markdown文件上传 ===")
    
    # 测试文件路径
    test_file_path = "test_files/test_interface.md"
    
    # 确保测试文件存在
    if not os.path.exists(test_file_path):
        # 创建测试文件
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("# API接口文档\n\n")
            f.write("## 接口1 获取用户信息\n")
            f.write("**GET** /api/users/{id}\n\n")
            f.write("**参数：**\n")
            f.write("```json\n")
            f.write("{\n")
            f.write("    \"id\": 123, // 用户ID\n")
            f.write("    \"name\": \"test\" // 用户名\n")
            f.write("}\n")
            f.write("```\n\n")
            f.write("**响应体说明：**\n")
            f.write("| 字段名 | 类型 | 描述 |\n")
            f.write("| ------ | ---- | ---- |\n")
            f.write("| id | int | 用户ID |\n")
            f.write("| name | string | 用户名 |\n")
            f.write("| email | string | 邮箱 |\n")
    
    # 上传文件
    url = "http://localhost:8000/api/files/upload"
    files = {'file': open(test_file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Markdown文件上传成功")
        else:
            print("❌ Markdown文件上传失败")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        files['file'].close()

# 测试接口获取功能
def test_get_interfaces():
    print("\n=== 测试获取接口列表 ===")
    
    url = "http://localhost:8000/api/interfaces"
    
    try:
        response = requests.get(url)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 获取接口列表成功")
        else:
            print("❌ 获取接口列表失败")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

# 测试获取接口参数功能
def test_get_interface_params():
    print("\n=== 测试获取接口参数 ===")
    
    # 先获取接口列表
    url = "http://localhost:8000/api/interfaces"
    response = requests.get(url)
    interfaces = response.json()
    
    if interfaces:
        interface_id = interfaces[0]['id']
        url = f"http://localhost:8000/api/interfaces/{interface_id}/params"
        
        try:
            response = requests.get(url)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ 获取接口参数成功")
            else:
                print("❌ 获取接口参数失败")
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
    else:
        print("❌ 没有找到接口")

# 测试获取接口响应字段功能
def test_get_interface_responses():
    print("\n=== 测试获取接口响应字段 ===")
    
    # 先获取接口列表
    url = "http://localhost:8000/api/interfaces"
    response = requests.get(url)
    interfaces = response.json()
    
    if interfaces:
        interface_id = interfaces[0]['id']
        url = f"http://localhost:8000/api/interfaces/{interface_id}/responses"
        
        try:
            response = requests.get(url)
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ 获取接口响应字段成功")
            else:
                print("❌ 获取接口响应字段失败")
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
    else:
        print("❌ 没有找到接口")

if __name__ == "__main__":
    # 创建测试文件目录
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
    
    test_markdown_upload()
    test_get_interfaces()
    test_get_interface_params()
    test_get_interface_responses()
    print("\n=== 测试完成 ===")
