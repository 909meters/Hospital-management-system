import requests
import json

# Test the API login endpoint
url = "http://127.0.0.1:8000/api/auth/login/"

# Test with testuser credentials
data = {
    "username": "testuser",
    "password": "test123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        print(f"Token: {token_data.get('token', 'No token')}")
        print(f"User: {token_data.get('username', 'No username')}")
        print(f"Role: {token_data.get('role', 'No role')}")
    else:
        print("❌ Login failed!")
        
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    print("Make sure Django server is running on http://127.0.0.1:8000")
except Exception as e:
    print(f"❌ Error: {e}")
