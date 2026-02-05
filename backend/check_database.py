import sqlite3
import config

# 连接数据库
conn = sqlite3.connect(config.DATABASE_PATH)
cursor = conn.cursor()

# 查询接口信息
cursor.execute('SELECT id, name, path, method FROM interfaces WHERE id = 418')
interface = cursor.fetchone()

if interface:
    print(f"接口ID: {interface[0]}")
    print(f"接口名称: {interface[1]}")
    print(f"接口路径: {interface[2]}")
    print(f"请求方式: {interface[3]}")
else:
    print("接口不存在")

# 关闭连接
conn.close()