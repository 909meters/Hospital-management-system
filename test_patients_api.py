#!/usr/bin/env python
import requests
import json

# Django backend URL
BASE_URL = 'http://127.0.0.1:8000'

def get_auth_token(username, password):
    """Get authentication token"""
    login_url = f"{BASE_URL}/api/auth/login/"
    data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(login_url, data=data)
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
        return None

def test_patients_api_access():
    """Test patients API access for different user roles"""
    
    # Test credentials
    test_users = [
        {'username': 'patient_test', 'password': 'testpass123', 'role': 'PATIENT'},
        {'username': 'testuser', 'password': 'testpass123', 'role': 'DOCTOR'},
        {'username': 'admin', 'password': 'admin123', 'role': 'ADMIN'}
    ]
    
    for user in test_users:
        print(f"\n{'='*50}")
        print(f"Testing with {user['role']}: {user['username']}")
        print(f"{'='*50}")
        
        # Get token
        token = get_auth_token(user['username'], user['password'])
        if not token:
            print(f"❌ Failed to get token for {user['username']}")
            continue
        
        print(f"✅ Successfully got token for {user['username']}")
        
        # Test GET /api/patients/
        headers = {'Authorization': f'Token {token}'}
        
        try:
            print(f"\nTesting GET /api/patients/...")
            response = requests.get(f"{BASE_URL}/api/patients/", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle paginated response
                if isinstance(data, dict) and 'results' in data:
                    results = data['results']
                    print(f"✅ Success! Returned {len(results)} patients (Total: {data.get('count', 'N/A')})")
                    for i, patient in enumerate(results):
                        print(f"  Patient {i+1}: {patient}")
                        # Try to extract user info if it exists
                        if isinstance(patient, dict) and 'user' in patient:
                            user_info = patient['user']
                            if isinstance(user_info, dict):
                                print(f"    Username: {user_info.get('username', 'N/A')}")
                                print(f"    Name: {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
                                print(f"    Role: {user_info.get('role', 'N/A')}")
                            else:
                                print(f"    User: {user_info}")
                        elif isinstance(patient, dict):
                            print(f"    Patient data: {patient}")
                else:
                    print(f"✅ Success! Returned {len(data)} patients (non-paginated)")
                    for i, patient in enumerate(data):
                        print(f"  Patient {i+1}: {patient}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        # Test user profile endpoint
        try:
            print(f"\nTesting GET /api/users/profile/...")
            response = requests.get(f"{BASE_URL}/api/users/profile/", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! User profile: {data.get('username')} - Role: {data.get('role')}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_patients_api_access()
