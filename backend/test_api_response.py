import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from async_parser import process_api_response

# 测试用例
test_responses = [
    # 情况1：正常的列表数据
    {
        "code": "0",
        "message": "success",
        "data": [
            {"id": 1, "name": "产品A", "detail": [{"name": "子产品1"}]},
            {"id": 2, "name": "产品B"}
        ]
    },
    
    # 情况2：正常的字典数据
    {
        "code": "0",
        "message": "success",
        "data": {
            "id": 1,
            "name": "产品A"
        }
    },
    
    # 情况3：缺少data字段
    {
        "code": "0",
        "message": "success"
    },
    
    # 情况4：data字段是其他类型
    {
        "code": "0",
        "message": "success",
        "data": "这是一个字符串"
    },
    
    # 情况5：字符串响应
    '{"code": "0", "message": "success", "data": [{"id": 1, "name": "产品A"}]}'
]

for i, response in enumerate(test_responses, 1):
    print(f"\n=== 测试用例 {i} ===")
    print(f"原始响应: {response}")
    result = process_api_response(response)
    print(f"处理结果: {result}")
