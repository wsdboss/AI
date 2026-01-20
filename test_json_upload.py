import requests
import os
import json

# 测试Swagger/OpenAPI文件上传功能
def test_swagger_upload():
    print("=== 测试Swagger/OpenAPI文件上传 ===")
    
    # 测试文件路径
    test_file_path = "test_files/test_swagger.json"
    
    # 确保测试文件存在
    if not os.path.exists(test_file_path):
        # 创建测试Swagger文件
        swagger_data = {
            "swagger": "2.0",
            "info": {
                "title": "测试API",
                "version": "1.0.0"
            },
            "paths": {
                "/api/users": {
                    "get": {
                        "summary": "获取用户列表",
                        "parameters": [
                            {
                                "name": "page",
                                "in": "query",
                                "type": "integer",
                                "description": "页码",
                                "required": False,
                                "example": 1
                            },
                            {
                                "name": "page_size",
                                "in": "query",
                                "type": "integer",
                                "description": "每页条数",
                                "required": False,
                                "example": 10
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "成功响应",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "description": "响应码",
                                            "example": 0
                                        },
                                        "message": {
                                            "type": "string",
                                            "description": "响应消息",
                                            "example": "success"
                                        },
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {
                                                        "type": "integer",
                                                        "description": "用户ID",
                                                        "example": 1
                                                    },
                                                    "name": {
                                                        "type": "string",
                                                        "description": "用户名",
                                                        "example": "test"
                                                    },
                                                    "email": {
                                                        "type": "string",
                                                        "description": "邮箱",
                                                        "example": "test@example.com"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "创建用户",
                        "parameters": [
                            {
                                "name": "body",
                                "in": "body",
                                "description": "用户信息",
                                "required": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "用户名",
                                            "example": "new_user"
                                        },
                                        "email": {
                                            "type": "string",
                                            "description": "邮箱",
                                            "example": "new@example.com"
                                        }
                                    }
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "成功响应",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "code": {
                                            "type": "integer",
                                            "description": "响应码",
                                            "example": 0
                                        },
                                        "message": {
                                            "type": "string",
                                            "description": "响应消息",
                                            "example": "success"
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "description": "用户ID",
                                                    "example": 2
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            json.dump(swagger_data, f, indent=2)
    
    # 上传文件
    url = "http://localhost:8000/api/files/upload"
    files = {'file': open(test_file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Swagger文件上传成功")
        else:
            print("❌ Swagger文件上传失败")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        files['file'].close()

# 测试OpenAPI 3.0文件上传功能
def test_openapi3_upload():
    print("\n=== 测试OpenAPI 3.0文件上传 ===")
    
    # 测试文件路径
    test_file_path = "test_files/test_openapi3.json"
    
    # 确保测试文件存在
    if not os.path.exists(test_file_path):
        # 创建测试OpenAPI 3.0文件
        openapi_data = {
            "openapi": "3.0.0",
            "info": {
                "title": "测试API",
                "version": "1.0.0"
            },
            "paths": {
                "/api/products/{id}": {
                    "get": {
                        "summary": "获取产品详情",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "产品ID",
                                "example": 1
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "成功响应",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "code": {
                                                    "type": "integer",
                                                    "description": "响应码",
                                                    "example": 0
                                                },
                                                "message": {
                                                    "type": "string",
                                                    "description": "响应消息",
                                                    "example": "success"
                                                },
                                                "data": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "description": "产品ID",
                                                            "example": 1
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "description": "产品名称",
                                                            "example": "测试产品"
                                                        },
                                                        "price": {
                                                            "type": "number",
                                                            "description": "产品价格",
                                                            "example": 99.99
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "put": {
                        "summary": "更新产品",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "产品ID"
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "产品名称"
                                            },
                                            "price": {
                                                "type": "number",
                                                "description": "产品价格"
                                            }
                                        },
                                        "required": ["name"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "成功响应",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "code": {
                                                    "type": "integer",
                                                    "description": "响应码",
                                                    "example": 0
                                                },
                                                "message": {
                                                    "type": "string",
                                                    "description": "响应消息",
                                                    "example": "success"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            json.dump(openapi_data, f, indent=2)
    
    # 上传文件
    url = "http://localhost:8000/api/files/upload"
    files = {'file': open(test_file_path, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ OpenAPI 3.0文件上传成功")
        else:
            print("❌ OpenAPI 3.0文件上传失败")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        files['file'].close()

# 测试接口列表和参数获取
def test_interface_details():
    print("\n=== 测试接口详情获取 ===")
    
    # 获取文件列表
    files_url = "http://localhost:8000/api/files"
    files_response = requests.get(files_url)
    files = files_response.json()
    
    if files:
        # 获取接口列表
        interfaces_url = "http://localhost:8000/api/interfaces"
        interfaces_response = requests.get(interfaces_url)
        interfaces = interfaces_response.json()
        
        print(f"共找到 {len(interfaces)} 个接口")
        
        # 获取前2个接口的详细信息
        for i, interface in enumerate(interfaces[:2]):
            interface_id = interface['id']
            print(f"\n--- 接口 {i+1}：{interface['name']} {interface['method']} {interface['path']} ---")
            
            # 获取接口参数
            params_url = f"http://localhost:8000/api/interfaces/{interface_id}/params"
            params_response = requests.get(params_url)
            params = params_response.json()
            print(f"请求参数 ({len(params)} 个):")
            for param in params:
                print(f"  - {param['name']} ({param['param_type']}){' [必填]' if param['required'] else ''}: {param['description']} (示例: {param['example']})")
            
            # 获取接口响应字段
            responses_url = f"http://localhost:8000/api/interfaces/{interface_id}/responses"
            responses_response = requests.get(responses_url)
            responses = responses_response.json()
            print(f"响应字段 ({len(responses)} 个):")
            for response_field in responses:
                print(f"  - {response_field['name']} ({response_field['response_type']}): {response_field['description']} (示例: {response_field['example']})")
    else:
        print("❌ 没有找到上传的文件")

if __name__ == "__main__":
    # 创建测试文件目录
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
    
    test_swagger_upload()
    test_openapi3_upload()
    test_interface_details()
    print("\n=== 测试完成 ===")
