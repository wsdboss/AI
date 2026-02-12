import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from async_parser import standardize_response

# 测试用例
test_responses = [
    # 情况1：正常的字典响应
    {
        "code": "0",
        "message": "success",
        "data": [
            {"id": 1, "name": "产品A"},
            {"id": 2, "name": "产品B"}
        ]
    },
    
    # 情况2：data是单个字典
    {
        "code": "0",
        "message": "success",
        "data": {"id": 1, "name": "产品A"}
    },
    
    # 情况3：data是其他类型
    {
        "code": "0",
        "message": "success",
        "data": "这是一个字符串"
    },
    
    # 情况4：缺少data字段
    {
        "code": "0",
        "message": "success"
    },
    
    # 情况5：字符串响应
    '{"code": "0", "message": "success", "data": [{"id": 1, "name": "产品A"}]}',
    
    # 情况6：非字典响应
    "这是一个普通字符串",
    
    # 情况7：None值
    None
]

for i, response in enumerate(test_responses, 1):
    print(f"\n=== 测试用例 {i} ===")
    print(f"原始响应: {response}")
    result = standardize_response(response)
    print(f"标准化结果: {result}")
    print(f"data类型: {type(result['data'])}")
    print(f"data长度: {len(result['data'])}")
