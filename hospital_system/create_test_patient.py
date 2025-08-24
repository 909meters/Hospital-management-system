#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from users.models import CustomUser
from patients.models import Patient

def create_test_patient():
    # Create patient user
    patient_user, created = CustomUser.objects.get_or_create(
        username='patient_test',
        defaults={
            'email': 'patient@test.com',
            'role': 'PATIENT',
            'first_name': 'Test',
            'last_name': 'Patient',
            'is_active': True
        }
    )
    
    if created:
        patient_user.set_password('testpass123')
        patient_user.save()
        print(f"Created patient user: {patient_user.username}")
    else:
        print(f"Patient user already exists: {patient_user.username}")
        # Update role if needed
        if patient_user.role != 'PATIENT':
            patient_user.role = 'PATIENT'
            patient_user.save()
            print(f"Updated role to PATIENT for user: {patient_user.username}")
    
    # Create patient profile
    patient_profile, created = Patient.objects.get_or_create(
        user=patient_user,
        defaults={
            'date_of_birth': '1990-01-01',
            'phone_number': '+1234567890',
            'address': '123 Test Street, Test City'
        }
    )
    
    if created:
        print(f"Created patient profile for: {patient_user.username}")
    else:
        print(f"Patient profile already exists for: {patient_user.username}")
    
    print(f"Patient details:")
    print(f"- User ID: {patient_user.id}")
    print(f"- Username: {patient_user.username}")
    print(f"- Role: {patient_user.role}")
    print(f"- Full name: {patient_user.get_full_name()}")
    print(f"- Patient profile created: {created}")

if __name__ == "__main__":
    create_test_patient()
