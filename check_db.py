import sqlite3
import os

# 数据库路径
DATABASE = 'backend/database.db'

def check_db():
    try:
        # 连接数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # 查询所有文件记录
        cursor.execute("SELECT * FROM interface_files")
        files = cursor.fetchall()
        
        print("数据库中的文件记录:")
        print("=" * 60)
        for i, file in enumerate(files):
            print(f"文件 {i+1}:")
            print(f"  ID: {file[0]}")
            print(f"  文件名: {file[1]}")
            print(f"  文件路径: {file[2]}")
            print(f"  文件类型: {file[3]}")
            print(f"  文件大小: {file[4]} bytes")
            print(f"  上传时间: {file[5]}")
            print(f"  解析状态: {file[6]}")
            print(f"  解析接口数: {file[7]}")
            print(f"  解析参数数: {file[8]}")
            print(f"  解析响应数: {file[9]}")
            # 检查文件是否存在
            file_exists = os.path.exists(file[2])
            print(f"  文件实际存在: {file_exists}")
            if not file_exists:
                print(f"  实际文件路径: {file[2]}")
            print("-" * 60)
        
        conn.close()
        print(f"\n总文件数: {len(files)}")
        
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_db()