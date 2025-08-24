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

def test_patient_creation_permissions():
    """Test that patients cannot create new patients"""
    
    print(f"{'='*60}")
    print(f"Testing Patient Creation Permissions")
    print(f"{'='*60}")
    
    # Test data for new patient
    new_patient_data = {
        'first_name': 'Test',
        'last_name': 'NewPatient',
        'date_of_birth': '1995-01-01',
        'phone_number': '+1234567890',
        'email': 'testnew@example.com',
        'address': 'Test Address'
    }
    
    # Test with different user roles
    test_users = [
        {'username': 'patient_test', 'password': 'testpass123', 'role': 'PATIENT'},
        {'username': 'fil1', 'password': 'testpass123', 'role': 'DOCTOR'},
        {'username': 'admin', 'password': 'testpass123', 'role': 'ADMIN'}
    ]
    
    for user in test_users:
        print(f"\n--- Testing with {user['role']}: {user['username']} ---")
        
        # Get token
        token = get_auth_token(user['username'], user['password'])
        if not token:
            print(f"❌ Failed to get token for {user['username']}")
            continue
        
        print(f"✅ Successfully got token for {user['username']}")
        
        # Test POST /api/patients/
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
        
        try:
            print(f"Testing POST /api/patients/ (create new patient)...")
            response = requests.post(f"{BASE_URL}/api/patients/", 
                                   headers=headers, 
                                   json=new_patient_data)
            print(f"Status Code: {response.status_code}")
            
            if user['role'] == 'PATIENT':
                if response.status_code == 403:
                    print(f"✅ Correctly blocked patient from creating new patients (403)")
                elif response.status_code == 405:
                    print(f"✅ Correctly blocked patient from creating new patients (405 - Method not allowed)")
                else:
                    print(f"❌ SECURITY ISSUE: Patient was able to create new patient! Status: {response.status_code}")
                    print(f"Response: {response.text}")
            else:
                # Doctor or Admin
                if response.status_code in [200, 201]:
                    print(f"✅ {user['role']} successfully created patient")
                    # Try to delete the created patient to clean up
                    response_data = response.json()
                    if 'user_id' in response_data:
                        delete_response = requests.delete(f"{BASE_URL}/api/patients/{response_data['user_id']}/", headers=headers)
                        if delete_response.status_code in [200, 204]:
                            print(f"✅ Cleaned up created patient")
                elif response.status_code == 403:
                    print(f"❌ {user['role']} was blocked from creating patients (should be allowed)")
                else:
                    print(f"⚠️ {user['role']} got unexpected status: {response.status_code}")
                    print(f"Response: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_patient_creation_permissions()
