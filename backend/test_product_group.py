import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from async_parser import handle_product_group_response

# 测试用例
test_responses = [
    # 情况1：正常的列表数据
    {
        "code": "0",
        "message": "success",
        "data": [
            {
                "rid": "1001",
                "type": "1",
                "name": "产品组A",
                "isShow": "1",
                "detail": [{"name": "产品A"}, {"name": "产品B"}]
            }
        ]
    },
    
    # 情况2：错误的访问方式（模拟错误）
    {
        "code": "0",
        "message": "success",
        "data": "这应该是列表，不是字符串"  # 错误的数据类型
    },
    
    # 情况3：data是单个字典
    {
        "code": "0",
        "message": "success",
        "data": {
            "rid": "1002",
            "type": "2",
            "name": "产品组B",
            "isShow": "1",
            "detail": "[{\"name\": \"产品C\"}]"  # detail是字符串
        }
    },
    
    # 情况4：字符串响应
    '{"code": "0", "message": "success", "data": [{"rid": "1003", "name": "产品组C"}]}'
]

for i, response in enumerate(test_responses, 1):
    print(f"\n=== 测试用例 {i} ===")
    print(f"原始响应: {response}")
    result = handle_product_group_response(response)
    print(f"处理结果: {result}")
    print(f"数据长度: {result.get('count', 0)}")
