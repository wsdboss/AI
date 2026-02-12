import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from async_parser import process_item, extract_field

def test_process_item():
    """测试安全处理列表/字典函数"""
    # 测试字典输入
    dict_item = {"key": "value", "other": "data"}
    result1 = process_item(dict_item)
    print(f"处理字典输入: {result1}")
    assert result1 == "value"
    
    # 测试列表输入
    list_item = ["value1", "value2"]
    result2 = process_item(list_item)
    print(f"处理列表输入: {result2}")
    assert result2 is None
    
    # 测试其他类型输入
    other_item = "string"
    result3 = process_item(other_item)
    print(f"处理其他类型输入: {result3}")
    assert result3 is None

def test_extract_field():
    """测试通用数据提取器函数"""
    # 测试数据
    data = {
        "user": {
            "id": 1,
            "name": "test",
            "addresses": [
                {"street": "Main St", "city": "City1"},
                {"street": "Second St", "city": "City2"}
            ]
        }
    }
    
    # 测试正常路径
    result1 = extract_field(data, "user.id")
    print(f"提取 user.id: {result1}")
    assert result1 == 1
    
    # 测试嵌套路径
    result2 = extract_field(data, "user.addresses.0.street")
    print(f"提取 user.addresses.0.street: {result2}")
    assert result2 == "Main St"
    
    # 测试不存在的路径
    result3 = extract_field(data, "user.nonexistent")
    print(f"提取不存在的路径: {result3}")
    assert result3 is None
    
    # 测试错误的索引
    result4 = extract_field(data, "user.addresses.5.street")
    print(f"提取错误的索引: {result4}")
    assert result4 is None

if __name__ == "__main__":
    print("测试模式函数...")
    test_process_item()
    test_extract_field()
    print("所有测试通过!")
