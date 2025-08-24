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

def test_medical_record_creation():
    """Test creating medical records for patients"""
    
    print(f"{'='*60}")
    print(f"Testing Medical Record Creation")
    print(f"{'='*60}")
    
    # Get token for doctor
    token = get_auth_token('fil1', 'testpass123')
    if not token:
        print(f"❌ Failed to get token for doctor")
        return
    
    print(f"✅ Successfully got token for doctor")
    
    # Test data for new medical record
    record_data = {
        'diagnosis': 'Test Diagnosis',
        'treatment': 'Test Treatment Plan',
        'notes': 'Test notes for the medical record'
    }
    
    # Test creating record for patient with ID 2 (should exist)
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    patient_id = 2  # Patient ID from previous tests
    
    try:
        print(f"\nTesting POST /api/patients/{patient_id}/records/...")
        response = requests.post(f"{BASE_URL}/api/patients/{patient_id}/records/", 
                               headers=headers, 
                               json=record_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print(f"✅ Successfully created medical record!")
            record_response = response.json()
            print(f"Record ID: {record_response.get('id')}")
            print(f"Diagnosis: {record_response.get('diagnosis')}")
            print(f"Patient: {record_response.get('patient')}")
            print(f"Created by: {record_response.get('created_by_name')}")
        else:
            print(f"❌ Failed to create medical record")
            if response.headers.get('content-type', '').startswith('application/json'):
                error_data = response.json()
                print(f"Error details: {error_data}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_medical_record_creation()
