import requests
import json

# Test the health check endpoint first
print("Testing health check endpoint...")
try:
    response = requests.get("http://localhost:8001/health")
    print(f"Health check status: {response.status_code}")
    print(f"Health check response: {response.json()}")
except Exception as e:
    print(f"Error testing health check: {e}")

# Test a dynamic interface endpoint
print("\nTesting dynamic interface endpoint...")
try:
    # Create a test interface by directly inserting into the database
    import sqlite3
    import os
    db_path = os.path.join(os.path.dirname(__file__), "api_generator.db")
    conn = sqlite3.connect(db_path)
    print(f"Using database path: {db_path}")
    cursor = conn.cursor()
    
    # Insert a test file
    cursor.execute('''
        INSERT INTO interface_files (filename, file_path, file_type, size, uploaded_at, parsed)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("test_file.json", "data/test_file.json", "application/json", 100, "2024-01-01T00:00:00", 1))
    file_id = cursor.lastrowid
    
    # Insert a test interface
    cursor.execute('''
        INSERT INTO interfaces (name, path, method, description, file_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Test Interface", "/api/test", "GET", "Test API endpoint", file_id))
    interface_id = cursor.lastrowid
    
    # Insert a mock config
    cursor.execute('''
        INSERT INTO mock_configs (interface_id, enabled, default_count)
        VALUES (?, ?, ?)
    ''', (interface_id, 1, 5))
    
    # Insert response fields
    cursor.execute('''
        INSERT INTO interface_responses (name, response_type, description, example, interface_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("code", "int", "Response code", "0", interface_id))
    
    cursor.execute('''
        INSERT INTO interface_responses (name, response_type, description, example, interface_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("data", "list", "Response data", "[]", interface_id))
    
    cursor.execute('''
        INSERT INTO interface_responses (name, response_type, description, example, interface_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("data.id", "string", "Item ID", "123", interface_id))
    
    cursor.execute('''
        INSERT INTO interface_responses (name, response_type, description, example, interface_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("data.name", "string", "Item name", "Test", interface_id))
    
    conn.commit()
    conn.close()
    
    print(f"Created test interface with ID: {interface_id}")
    
    # Now test the endpoint
    print("Testing the dynamic interface...")
    response = requests.get("http://localhost:8001/dynamic/api/test")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Test passed! The fix is working correctly.")
    else:
        print("\n❌ Test failed! The fix is not working correctly.")
        
except Exception as e:
    print(f"Error testing dynamic interface: {e}")
    import traceback
    traceback.print_exc()