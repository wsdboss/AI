import sqlite3
import os

# 获取数据库路径
DB_PATH = os.path.join(os.getcwd(), 'api_generator.db')

print(f"检查数据库: {DB_PATH}")
print(f"数据库存在: {os.path.exists(DB_PATH)}")

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 查询文件表
print("\n=== 文件表记录 ===")
cursor.execute('SELECT * FROM interface_files')
files = cursor.fetchall()

print(f"共有 {len(files)} 条文件记录")
for file in files:
    print(f"ID: {file[0]}, 文件名: {file[1]}, 路径: {file[2]}, 类型: {file[3]}, 大小: {file[4]}, 上传时间: {file[5]}, 解析状态: {file[6]}")
    
    # 检查文件是否存在
    if not os.path.exists(file[2]):
        print(f"  ⚠️  文件不存在: {file[2]}")

# 关闭数据库连接
conn.close()
print("\n=== 检查完成 ===")
