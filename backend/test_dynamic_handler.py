import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from async_parser import DynamicInterfaceHandler

def test_process_response():
    """测试处理响应方法"""
    handler = DynamicInterfaceHandler()
    
    # 测试列表响应
    list_response = [
        {"id": 1, "name": "项目1"},
        {"id": 2, "name": "项目2"}
    ]
    result1 = handler.process_response(list_response)
    print(f"处理列表响应: {result1}")
    assert result1["code"] == "0"
    assert result1["message"] == "success"
    assert isinstance(result1["data"], list)
    assert len(result1["data"]) == 2
    
    # 测试字典响应
    dict_response = {
        "code": "0",
        "message": "success",
        "data": {"id": 1, "name": "项目1"}
    }
    result2 = handler.process_response(dict_response)
    print(f"处理字典响应: {result2}")
    assert result2["code"] == "0"
    assert result2["message"] == "success"
    assert isinstance(result2["data"], list)
    assert len(result2["data"]) == 1
    
    # 测试字符串响应
    string_response = '{"code": "0", "data": {"id": 1, "name": "项目1"}}'
    result3 = handler.process_response(string_response)
    print(f"处理字符串响应: {result3}")
    assert result3["code"] == "0"
    assert isinstance(result3["data"], list)
    
    # 测试其他类型响应
    other_response = 123
    result4 = handler.process_response(other_response)
    print(f"处理其他类型响应: {result4}")
    assert result4["code"] == "-1"

def test_extract_data():
    """测试数据提取方法"""
    handler = DynamicInterfaceHandler()
    
    # 测试复杂响应
    complex_response = {
        "code": "0",
        "data": [
            {
                "id": 1,
                "name": "项目1",
                "details": [{"value": "A"}, {"value": "B"}]
            }
        ]
    }
    
    # 测试点分路径
    value1 = handler.extract_data(complex_response, "data.0.name")
    print(f"提取点分路径值: {value1}")
    assert value1 == "项目1"
    
    # 测试方括号路径
    value2 = handler.extract_data(complex_response, "data[0].details[0].value")
    print(f"提取方括号路径值: {value2}")
    assert value2 == "A"
    
    # 测试不存在的路径
    value3 = handler.extract_data(complex_response, "data.0.nonexistent")
    print(f"提取不存在路径值: {value3}")
    assert value3 is None

if __name__ == "__main__":
    print("测试 DynamicInterfaceHandler 类...")
    test_process_response()
    test_extract_data()
    print("所有测试通过!")
