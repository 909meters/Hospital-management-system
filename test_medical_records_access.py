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

def test_medical_records_access():
    """Test medical records API access for patient"""
    
    print(f"{'='*50}")
    print(f"Testing Medical Records Access for PATIENT")
    print(f"{'='*50}")
    
    # Get token for patient
    token = get_auth_token('patient_test', 'testpass123')
    if not token:
        print(f"❌ Failed to get token for patient_test")
        return
    
    print(f"✅ Successfully got token for patient_test")
    
    # Test GET /api/patients/15/records/ (patient's own records)
    headers = {'Authorization': f'Token {token}'}
    
    try:
        print(f"\nTesting GET /api/patients/15/records/...")
        response = requests.get(f"{BASE_URL}/api/patients/15/records/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle paginated response
            if isinstance(data, dict) and 'results' in data:
                results = data['results']
                print(f"✅ Success! Found {len(results)} medical records (Total: {data.get('count', 'N/A')})")
                for i, record in enumerate(results):
                    print(f"  Record {i+1}: {record}")
            else:
                print(f"✅ Success! Found {len(data)} medical records (non-paginated)")
                for i, record in enumerate(data):
                    print(f"  Record {i+1}: {record}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    # Test accessing other patient's records (should fail)
    try:
        print(f"\nTesting GET /api/patients/2/records/ (should fail - other patient's records)...")
        response = requests.get(f"{BASE_URL}/api/patients/2/records/", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print(f"✅ Correctly blocked access to other patient's records")
        elif response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                results = data['results']
                if len(results) == 0:
                    print(f"✅ Correctly returned empty list for other patient's records")
                else:
                    print(f"❌ Incorrectly returned {len(results)} records for other patient")
            else:
                print(f"❌ Unexpected response format: {data}")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_medical_records_access()
