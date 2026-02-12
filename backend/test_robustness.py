import unittest
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_app import (
    safe_get,
    safe_set,
    ensure_type,
    standardize_response,
    normalize_data_structure,
    generate_mock_value
)

class TestRobustness(unittest.TestCase):
    """测试代码健壮性"""
    
    def test_safe_get(self):
        """测试安全获取嵌套数据"""
        # 测试正常情况
        data = {
            'user': {
                'id': 1,
                'name': 'test',
                'addresses': [
                    {'street': 'Main St'},
                    {'street': 'Second St'}
                ]
            }
        }
        
        # 测试正常路径
        self.assertEqual(safe_get(data, ['user', 'id']), 1)
        self.assertEqual(safe_get(data, ['user', 'name']), 'test')
        self.assertEqual(safe_get(data, ['user', 'addresses', 0, 'street']), 'Main St')
        
        # 测试不存在的路径
        self.assertEqual(safe_get(data, ['user', 'nonexistent']), None)
        self.assertEqual(safe_get(data, ['user', 'addresses', 5]), None)
        self.assertEqual(safe_get(data, ['nonexistent', 'id']), None)
        
        # 测试默认值
        self.assertEqual(safe_get(data, ['user', 'nonexistent'], 'default'), 'default')
        
        # 测试错误类型
        self.assertEqual(safe_get(None, ['user', 'id']), None)
        self.assertEqual(safe_get('string', ['user', 'id']), None)
    
    def test_safe_set(self):
        """测试安全设置嵌套数据"""
        # 测试正常情况
        data = {}
        
        # 测试设置简单路径
        self.assertTrue(safe_set(data, ['user', 'id'], 1))
        self.assertEqual(data['user']['id'], 1)
        
        # 测试设置嵌套路径
        self.assertTrue(safe_set(data, ['user', 'addresses', 0, 'street'], 'Main St'))
        self.assertEqual(data['user']['addresses'][0]['street'], 'Main St')
        
        # 测试设置列表元素
        self.assertTrue(safe_set(data, ['user', 'addresses', 1, 'street'], 'Second St'))
        self.assertEqual(data['user']['addresses'][1]['street'], 'Second St')
        
        # 测试错误类型
        self.assertFalse(safe_set('string', ['user', 'id'], 1))
    
    def test_ensure_type(self):
        """测试类型确保函数"""
        # 测试正常情况
        self.assertEqual(ensure_type('123', int, 0), 123)
        self.assertEqual(ensure_type('true', bool, False), True)
        self.assertEqual(ensure_type('123.45', float, 0.0), 123.45)
        
        # 测试类型转换失败
        self.assertEqual(ensure_type('abc', int, 0), 0)
        self.assertEqual(ensure_type('abc', float, 0.0), 0.0)
        
        # 测试错误类型
        self.assertEqual(ensure_type(None, int, 0), 0)
        self.assertEqual(ensure_type(None, str, 'default'), 'default')
    
    def test_standardize_response(self):
        """测试响应标准化函数"""
        # 测试正常情况
        data = {'code': 0, 'data': {'id': 1, 'name': 'test'}}
        standardized = standardize_response(data)
        self.assertEqual(standardized['code'], 0)
        self.assertEqual(standardized['data']['id'], 1)
        
        # 测试缺少code字段
        data = {'data': {'id': 1, 'name': 'test'}}
        standardized = standardize_response(data)
        self.assertEqual(standardized['code'], 0)
        
        # 测试包含message字段
        data = {'code': 0, 'message': 'success', 'data': {'id': 1}}
        standardized = standardize_response(data)
        self.assertNotIn('message', standardized)
        
        # 测试错误类型
        standardized = standardize_response('string')
        self.assertEqual(standardized['code'], 0)
        self.assertEqual(standardized['data'], {})
    
    def test_normalize_data_structure(self):
        """测试数据结构标准化函数"""
        # 测试正常情况
        structure = {
            'id': int,
            'name': str,
            'address': {
                'street': str,
                'city': str
            },
            'phones': list
        }
        
        data = {'id': 1, 'name': 'test'}
        normalized = normalize_data_structure(data, structure)
        self.assertEqual(normalized['id'], 1)
        self.assertEqual(normalized['name'], 'test')
        self.assertEqual(normalized['address'], {})
        self.assertEqual(normalized['phones'], [])
        
        # 测试错误类型
        normalized = normalize_data_structure('string', structure)
        self.assertIsInstance(normalized, dict)
    
    def test_generate_mock_value(self):
        """测试生成模拟值函数"""
        # 测试各种类型
        string_value = generate_mock_value('string')
        self.assertIsInstance(string_value, str)
        
        int_value = generate_mock_value('int')
        self.assertIsInstance(int_value, int)
        
        bool_value = generate_mock_value('boolean')
        self.assertIsInstance(bool_value, bool)
        
        float_value = generate_mock_value('double')
        self.assertIsInstance(float_value, float)
        
        list_value = generate_mock_value('list')
        self.assertIsInstance(list_value, list)
        
        map_value = generate_mock_value('map')
        self.assertIsInstance(map_value, dict)
        
        # 测试错误类型
        default_value = generate_mock_value(None)
        self.assertEqual(default_value, 'mock_value')
        
        default_value = generate_mock_value('nonexistent')
        self.assertEqual(default_value, 'mock_value')

if __name__ == '__main__':
    unittest.main()
