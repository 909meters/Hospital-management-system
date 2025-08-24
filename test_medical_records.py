#!/usr/bin/env python3
"""
Test script for medical records functionality.
This script tests the fixed medical records endpoints.
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
DOCTOR_USERNAME = "testuser"  # This user has doctor role
DOCTOR_PASSWORD = "test123"

def login_user(username, password):
    """Login and get authentication token"""
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", data=login_data)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('token')
    else:
        print(f"Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_patients(token):
    """Get available patients"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/patients/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get patients: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_medical_records(token, patient_id):
    """Get medical records for a patient"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/records/", headers=headers)
    
    print(f"Medical records response status: {response.status_code}")
    print(f"Medical records response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def add_medical_record(token, patient_id):
    """Add a test medical record"""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    record_data = {
        "patient": patient_id,  # Add the patient field
        "diagnosis": "Common cold",
        "treatment": "Rest and fluids, paracetamol as needed",
        "notes": "Patient advised to return if symptoms worsen"
    }
    
    response = requests.post(f"{BASE_URL}/patients/{patient_id}/records/", 
                           headers=headers, 
                           json=record_data)
    
    print(f"Add record response status: {response.status_code}")
    print(f"Add record response: {response.text}")
    
    return response

def main():
    print("🔍 Testing Medical Records Functionality")
    print("=" * 50)
    
    # Step 1: Login as doctor
    print("1. Logging in as doctor...")
    token = login_user(DOCTOR_USERNAME, DOCTOR_PASSWORD)
    
    if not token:
        print("❌ Login failed! Please check credentials.")
        return
    
    print("✅ Login successful!")
    
    # Step 2: Get patients
    print("\n2. Getting available patients...")
    patients_response = get_patients(token)
    
    if not patients_response:
        print("❌ Failed to get patients!")
        return
    
    patients = patients_response.get('results', [])
    if not patients:
        print("❌ No patients available!")
        return
    
    print(f"✅ Found {len(patients)} patients:")
    for patient in patients:
        print(f"   - {patient['full_name']} (ID: {patient['user_id']})")
    
    # Step 3: Get medical records for first patient
    first_patient_id = patients[0]['user_id']
    print(f"\n3. Getting medical records for patient ID {first_patient_id}...")
    
    records = get_medical_records(token, first_patient_id)
    
    # Step 4: Add a test medical record
    print(f"\n4. Adding a test medical record...")
    add_response = add_medical_record(token, first_patient_id)
    
    if add_response.status_code == 201:
        print("✅ Medical record added successfully!")
        
        # Get records again to see the new one
        print(f"\n5. Getting updated medical records...")
        updated_records = get_medical_records(token, first_patient_id)
    else:
        print("❌ Failed to add medical record!")

if __name__ == "__main__":
    main()
