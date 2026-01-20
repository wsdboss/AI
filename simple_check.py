import sqlite3
import os

# 数据库路径
DATABASE = os.path.join('backend', 'database.db')

def simple_check():
    try:
        # 检查数据库文件是否存在
        if not os.path.exists(DATABASE):
            print(f"数据库文件不存在: {DATABASE}")
            return
        
        print(f"数据库文件存在: {DATABASE}")
        print(f"文件大小: {os.path.getsize(DATABASE)} bytes")
        
        # 连接数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        print("数据库连接成功")
        
        # 获取表列表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"表列表: {[table[0] for table in tables]}")
        
        # 检查表结构
        cursor.execute("PRAGMA table_info(interface_files);")
        columns = cursor.fetchall()
        print("interface_files表结构:")
        for col in columns:
            print(f"{col[1]}: {col[2]}")
        
        # 统计文件数量
        cursor.execute("SELECT COUNT(*) FROM interface_files;")
        file_count = cursor.fetchone()[0]
        print(f"\n文件数量: {file_count}")
        
        # 统计接口数量
        cursor.execute("SELECT COUNT(*) FROM interfaces;")
        interface_count = cursor.fetchone()[0]
        print(f"接口数量: {interface_count}")
        
        # 查询最近的5个文件
        cursor.execute("SELECT id, filename, uploaded_at FROM interface_files ORDER BY id DESC LIMIT 5;")
        recent_files = cursor.fetchall()
        print("\n最近5个文件:")
        for file in recent_files:
            print(f"ID: {file[0]}, Filename: {file[1]}, Uploaded At: {file[2]}")
        
        conn.close()
        print("\n检查完成")
        
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    simple_check()