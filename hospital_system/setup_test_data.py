#!/usr/bin/env python3
"""
Script to create test data for Hospital Management System Docker setup
This script should be run after the first Docker startup to populate the database
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
sys.path.append('/app')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient
from scheduling.models import Appointment

User = get_user_model()

def create_test_users():
    """Create test users if they don't exist"""
    print("🔧 Creating test users...")
    
    # Admin user
    if not User.objects.filter(username='testadmin').exists():
        admin = User.objects.create_user(
            username='testadmin',
            email='admin@hospital.com',
            password='test123',
            first_name='Test',
            last_name='Admin',
            role=User.Role.ADMIN
        )
        print(f"✅ Created admin user: {admin.username}")
    
    # Doctor user
    if not User.objects.filter(username='testdoctor').exists():
        doctor = User.objects.create_user(
            username='testdoctor',
            email='doctor@hospital.com',
            password='test123',
            first_name='Dr. Test',
            last_name='Doctor',
            role=User.Role.DOCTOR
        )
        print(f"✅ Created doctor user: {doctor.username}")
    
    # Patient user
    if not User.objects.filter(username='testpatient').exists():
        patient = User.objects.create_user(
            username='testpatient',
            email='patient@hospital.com',
            password='test123',
            first_name='Test',
            last_name='Patient',
            role=User.Role.PATIENT
        )
        print(f"✅ Created patient user: {patient.username}")
    
    print("👥 Test users created successfully!")

def create_test_patients():
    """Create test patient records"""
    print("🏥 Creating test patient records...")
    
    # Get users
    try:
        doctor = User.objects.get(username='testdoctor')
        patient_user = User.objects.get(username='testpatient')
    except User.DoesNotExist:
        print("❌ Required users not found. Please run create_test_users first.")
        return
    
    # Create patient record for testpatient user
    if not Patient.objects.filter(user=patient_user).exists():
        patient = Patient.objects.create(
            user=patient_user,
            phone_number='+1234567890',
            date_of_birth='1990-01-01',
            address='123 Test Street, Test City'
        )
        print(f"✅ Created patient record for: {patient.user.first_name} {patient.user.last_name}")
    
    print("🏥 Patient records created successfully!")

def main():
    print("🚀 Setting up test data for Hospital Management System...")
    print("=" * 60)
    
    try:
        create_test_users()
        print()
        create_test_patients()
        print()
        print("✨ Test data setup completed successfully!")
        print()
        print("📋 Available test accounts:")
        print("   👑 Admin: testadmin / test123")
        print("   🩺 Doctor: testdoctor / test123")
        print("   🤒 Patient: testpatient / test123")
        print()
        print("🌐 You can now access the system at:")
        print("   Frontend: http://localhost:8501")
        print("   Admin: http://localhost:8000/admin")
        
    except Exception as e:
        print(f"❌ Error setting up test data: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
