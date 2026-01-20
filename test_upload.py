import requests
import os

# 上传文件
def upload_file():
    file_path = "backend/uploads/d26677ea-e9a4-4273-93cc-79bc1763a5e6_position-planning-api.md"
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    print(f"上传文件: {file_path}")
    files = {'file': open(file_path, 'rb')}
    response = requests.post('http://localhost:8000/api/files/upload', files=files)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

if __name__ == "__main__":
    upload_file()
