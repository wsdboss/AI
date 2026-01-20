import sqlite3
import os

# 数据库路径
DATABASE = os.path.join('backend', 'database.db')

def check_files():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 查询所有文件
        cursor.execute('SELECT * FROM interface_files')
        files = cursor.fetchall()
        
        print('所有文件列表:')
        for file in files:
            print(f"ID: {file[0]}")
            print(f"Filename: {file[1]}")
            print(f"File Path: {file[2]}")
            print(f"File Type: {file[3]}")
            print(f"Size: {file[4]}")
            print(f"Uploaded At: {file[5]}")
            print(f"Parsed: {file[6]}")
            print(f"Parsed Interfaces: {file[7]}")
            print(f"Parsed Params: {file[8]}")
            print(f"Parsed Responses: {file[9]}")
            print('-' * 50)
        
        # 查询接口数量
        cursor.execute('SELECT COUNT(*) FROM interfaces')
        interfaces_count = cursor.fetchone()[0]
        print(f"\n总接口数量: {interfaces_count}")
        
    except Exception as e:
        print(f"查询数据库失败: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_files()