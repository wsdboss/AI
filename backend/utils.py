import json

# 安全访问工具函数
def safe_get(data, keys, default=None):
    """安全地获取嵌套数据
    
    Args:
        data: 要访问的数据结构（字典或列表）
        keys: 键路径列表，如 ['data', 'items', 0, 'id']
        default: 当路径不存在时返回的默认值
        
    Returns:
        访问到的值或默认值
    """
    try:
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return default
        return current
    except (TypeError, IndexError, KeyError):
        return default

def safe_set(data, keys, value):
    """安全地设置嵌套数据
    
    Args:
        data: 要修改的数据结构（字典）
        keys: 键路径列表，如 ['data', 'items', 0, 'id']
        value: 要设置的值
        
    Returns:
        是否设置成功
    """
    try:
        current = data
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                # 最后一个键，直接设置值
                if isinstance(current, dict):
                    current[key] = value
                    return True
                elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                    current[key] = value
                    return True
                else:
                    return False
            else:
                # 中间键，确保存在且类型正确
                next_key = keys[i+1]
                if isinstance(current, dict):
                    if key not in current:
                        # 根据下一个键的类型初始化
                        if isinstance(next_key, int):
                            current[key] = []
                        else:
                            current[key] = {}
                    elif not isinstance(current[key], (dict, list)):
                        # 类型不正确，重新初始化
                        if isinstance(next_key, int):
                            current[key] = []
                        else:
                            current[key] = {}
                    current = current[key]
                elif isinstance(current, list) and isinstance(key, int):
                    if len(current) <= key:
                        # 列表长度不足，补充空元素
                        while len(current) <= key:
                            current.append({} if isinstance(next_key, str) else [])
                    elif not isinstance(current[key], (dict, list)):
                        # 类型不正确，重新初始化
                        current[key] = {} if isinstance(next_key, str) else []
                    current = current[key]
                else:
                    return False
        return True
    except (TypeError, IndexError):
        return False

def ensure_type(value, expected_type, default=None):
    """确保值的类型正确
    
    Args:
        value: 要检查的值
        expected_type: 期望的类型
        default: 类型不正确时返回的默认值
        
    Returns:
        类型正确的值或默认值
    """
    if value is None:
        return default
    
    if isinstance(value, expected_type):
        return value
    try:
        # 尝试类型转换
        if expected_type == int:
            return int(value)
        elif expected_type == float:
            return float(value)
        elif expected_type == bool:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'y')
            return bool(value)
        elif expected_type == str:
            return str(value)
        elif expected_type == list:
            return list(value)
        elif expected_type == dict:
            return dict(value)
    except (ValueError, TypeError):
        pass
    return default

# 模式1：安全处理列表/字典
def process_item(item):
    """安全处理列表/字典类型的数据
    
    Args:
        item: 要处理的数据项
        
    Returns:
        处理后的数据或None
    """
    if isinstance(item, dict):
        return item.get("key")
    return None

# 模式2：通用数据提取器
def extract_field(data, field_path):
    """支持点分路径的字段提取，自动处理类型
    
    Args:
        data: 要提取数据的对象
        field_path: 字段路径，支持点分表示法，如 "user.addresses.0.street"
        
    Returns:
        提取的字段值或None
    """
    keys = field_path.split(".")
    current = data
    
    for key in keys:
        if isinstance(current, list) and key.isdigit():
            try:
                index = int(key)
                current = current[index] if 0 <= index < len(current) else None
            except (ValueError, IndexError):
                return None
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None
        
        if current is None:
            break
    
    return current

# 数据标准化函数
def standardize_response(data):
    """标准化API响应数据
    
    Args:
        data: 原始响应数据
        
    Returns:
        标准化后的响应数据
    """
    try:
        # 确保data是字典
        if not isinstance(data, dict):
            data = {}
        
        # 确保包含code字段，默认为0
        if 'code' not in data:
            data['code'] = 0
        else:
            data['code'] = ensure_type(data['code'], int, 0)
        
        # 移除message字段，确保响应格式简洁
        if 'message' in data:
            del data['message']
        
        # 处理data字段，确保存在
        if 'data' not in data:
            data['data'] = {}
        else:
            data['data'] = ensure_type(data['data'], (dict, list), {})
        
        return data
    except Exception as e:
        # 处理异常情况
        return {
            'code': 500,
            'data': None
        }

def normalize_data_structure(data, structure=None):
    """标准化数据结构，确保符合预期格式
    
    Args:
        data: 要标准化的数据
        structure: 预期的数据结构模板
        
    Returns:
        标准化后的数据
    """
    try:
        if structure is None:
            return data
        
        if isinstance(structure, dict):
            if not isinstance(data, dict):
                data = {}
            
            for key, expected_type in structure.items():
                if key not in data:
                    # 为缺失字段提供默认值
                    if expected_type == list:
                        data[key] = []
                    elif expected_type == dict or isinstance(expected_type, dict):
                        data[key] = {}
                    elif expected_type == int:
                        data[key] = 0
                    elif expected_type == float:
                        data[key] = 0.0
                    elif expected_type == bool:
                        data[key] = False
                    elif expected_type == str:
                        data[key] = ""
                    else:
                        data[key] = None
                else:
                    # 递归标准化嵌套结构
                    if isinstance(expected_type, dict):
                        data[key] = normalize_data_structure(data[key], expected_type)
                    elif expected_type == list:
                        if not isinstance(data[key], list):
                            data[key] = []
            
        elif isinstance(structure, list):
            if not isinstance(data, list):
                data = []
            
            # 如果列表有模板元素，标准化每个元素
            if structure and isinstance(structure[0], dict):
                for i, item in enumerate(data):
                    data[i] = normalize_data_structure(item, structure[0])
        
        return data
    except Exception as e:
        # 处理异常情况
        return data

# 安全获取嵌套数据的辅助函数（支持可变长度的键路径）
def safe_get_varargs(data, *keys):
    """安全地获取嵌套数据，支持可变长度的键路径
    
    Args:
        data: 要访问的数据结构
        *keys: 键路径，如 safe_get_varargs(data, 'user', 'addresses', 0, 'street')
        
    Returns:
        访问到的值或None
    """
    current = data
    try:
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return None
        return current
    except (TypeError, IndexError, KeyError):
        return None
