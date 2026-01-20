# API接口文档

## 接口1 获取用户信息
**GET** /api/users/{id}

**参数：**
```json
{
    "id": 123, // 用户ID
    "name": "test" // 用户名
}
```

**响应体说明：**
| 字段名 | 类型 | 描述 |
| ------ | ---- | ---- |
| id | int | 用户ID |
| name | string | 用户名 |
| email | string | 邮箱 |
