#!/usr/bin/env python3
"""
Test script for appointment creation functionality.
This script tests the fixed appointment creation endpoint.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
PATIENT_USERNAME = "patient1"
PATIENT_PASSWORD = "patient123"

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

def get_user_profile(token):
    """Get current user profile"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get profile: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_doctors(token):
    """Get available doctors"""
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/users/doctors/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get doctors: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_appointment(token, doctor_id):
    """Test appointment creation"""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Create appointment for tomorrow at 10:00 AM
    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    appointment_data = {
        "doctor": doctor_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "SCHEDULED",
        "notes": "Test appointment via API"
    }
    
    print(f"Creating appointment with data: {json.dumps(appointment_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/scheduling/appointments/", 
                           headers=headers, 
                           json=appointment_data)
    
    return response

def main():
    print("🔍 Testing Appointment Creation")
    print("=" * 50)
    
    # Step 1: Login
    print("1. Logging in as patient...")
    token = login_user(PATIENT_USERNAME, PATIENT_PASSWORD)
    
    if not token:
        print("❌ Login failed! Please check credentials.")
        return
    
    print("✅ Login successful!")
    
    # Step 2: Get user profile
    print("\n2. Getting user profile...")
    profile = get_user_profile(token)
    
    if not profile:
        print("❌ Failed to get user profile!")
        return
    
    print(f"✅ User profile: {profile['first_name']} {profile['last_name']} (Role: {profile['role']})")
    
    if profile['role'] != 'PATIENT':
        print("❌ User is not a patient! Only patients can create appointments.")
        return
    
    # Step 3: Get doctors
    print("\n3. Getting available doctors...")
    doctors_response = get_doctors(token)
    
    if not doctors_response:
        print("❌ Failed to get doctors!")
        return
    
    doctors = doctors_response.get('results', [])
    if not doctors:
        print("❌ No doctors available!")
        return
    
    print(f"✅ Found {len(doctors)} doctors:")
    for doctor in doctors:
        print(f"   - Dr. {doctor['first_name']} {doctor['last_name']} (ID: {doctor['id']})")
    
    # Step 4: Create appointment
    print("\n4. Creating appointment...")
    first_doctor_id = doctors[0]['id']
    response = create_appointment(token, first_doctor_id)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 201:
        appointment = response.json()
        print("✅ Appointment created successfully!")
        print(f"   - Appointment ID: {appointment['id']}")
        print(f"   - Doctor: {appointment['doctor_name']}")
        print(f"   - Start time: {appointment['start_time']}")
        print(f"   - Status: {appointment['status']}")
    else:
        print("❌ Appointment creation failed!")
        try:
            error_data = response.json()
            print(f"   Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw error: {response.text}")

if __name__ == "__main__":
    main()
