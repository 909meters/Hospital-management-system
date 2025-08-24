#!/usr/bin/env python3
"""
Test script to verify all Hospital Management System API endpoints work correctly.
"""

import requests
import json

API_BASE_URL = "http://127.0.0.1:8000/api"

def test_login():
    """Test login functionality"""
    print("🔐 Testing login...")
    response = requests.post(f"{API_BASE_URL}/auth/login/", json={
        'username': 'testuser',
        'password': 'test123'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful! Token: {data['token'][:20]}...")
        return data['token']
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_endpoints(token):
    """Test all main endpoints"""
    headers = {'Authorization': f'Token {token}'}
    
    endpoints = [
        ('/patients/', 'Patients'),
        ('/scheduling/appointments/', 'Appointments'),
        ('/users/doctors/', 'Doctors'),
        ('/auth/profile/', 'User Profile'),
    ]
    
    for endpoint, name in endpoints:
        print(f"🔍 Testing {name} ({endpoint})...")
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'results' in data:
                    count = len(data['results'])
                    print(f"✅ {name}: {response.status_code} - {count} items")
                else:
                    print(f"✅ {name}: {response.status_code} - Data received")
            except json.JSONDecodeError:
                print(f"❌ {name}: JSON decode error")
        elif response.status_code == 403:
            print(f"⚠️ {name}: {response.status_code} - Permission denied")
        else:
            print(f"❌ {name}: {response.status_code} - {response.text[:100]}")

def main():
    print("🏥 Hospital Management System API Test")
    print("=" * 50)
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    print()
    # Test endpoints
    test_endpoints(token)
    
    print()
    print("✅ API testing completed!")

if __name__ == "__main__":
    main()
