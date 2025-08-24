#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from users.models import CustomUser
from patients.models import Patient, MedicalRecord
from datetime import datetime

def create_test_medical_record():
    try:
        # Get patient_test user
        patient_user = CustomUser.objects.get(username='patient_test')
        patient = Patient.objects.get(user=patient_user)
        
        # Get a doctor to create the record
        doctor = CustomUser.objects.filter(role='DOCTOR').first()
        if not doctor:
            print("No doctor found. Creating one...")
            doctor = CustomUser.objects.create_user(
                username='test_doctor_records',
                password='testpass123',
                email='testdoc@hospital.com',
                role='DOCTOR',
                first_name='Test',
                last_name='Doctor'
            )
        
        # Create a test medical record
        record = MedicalRecord.objects.create(
            patient=patient,
            created_by=doctor,
            diagnosis='Common Cold',
            treatment='Rest, fluids, and over-the-counter pain relievers',
            notes='Patient presented with mild cold symptoms. Recommended home care.'
        )
        
        print(f"✅ Created medical record for patient: {patient_user.get_full_name()}")
        print(f"   - Record ID: {record.id}")
        print(f"   - Diagnosis: {record.diagnosis}")
        print(f"   - Created by: Dr. {doctor.get_full_name()}")
        print(f"   - Visit date: {record.visit_date}")
        
    except CustomUser.DoesNotExist:
        print("❌ Patient 'patient_test' not found. Please create the patient first.")
    except Patient.DoesNotExist:
        print("❌ Patient profile for 'patient_test' not found.")
    except Exception as e:
        print(f"❌ Error creating medical record: {e}")

if __name__ == "__main__":
    create_test_medical_record()
