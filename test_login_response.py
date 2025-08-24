#!/usr/bin/env python
import requests
import json

# Django backend URL
BASE_URL = 'http://127.0.0.1:8000'

def test_login_response():
    """Test what login API returns"""
    
    login_url = f"{BASE_URL}/api/auth/login/"
    data = {
        'username': 'patient_test',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(login_url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            json_data = response.json()
            print(f"JSON Data: {json.dumps(json_data, indent=2)}")
            
            if 'user' in json_data:
                print(f"✅ User data found in response")
                print(f"User role: {json_data['user'].get('role', 'NOT FOUND')}")
            else:
                print(f"❌ No user data in response")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login_response()
