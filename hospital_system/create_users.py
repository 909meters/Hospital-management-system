#!/usr/bin/env python
"""
Скрипт для создания тестового пользователя и суперпользователя
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings_simple')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient

User = get_user_model()

# Создание суперпользователя
try:
    admin_user = User.objects.get(username='admin')
    print("✅ Суперпользователь 'admin' уже существует")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@hospital.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='ADMIN'
    )
    print("✅ Суперпользователь 'admin' создан")

# Создание тестового врача
try:
    test_user = User.objects.get(username='testuser')
    print("✅ Тестовый пользователь 'testuser' уже существует")
    # Обновляем роль если нужно
    if test_user.role != 'DOCTOR':
        test_user.role = 'DOCTOR'
        test_user.save()
        print("✅ Роль пользователя обновлена до DOCTOR")
except User.DoesNotExist:
    test_user = User.objects.create_user(
        username='testuser',
        email='test@hospital.com',
        password='test123',
        first_name='Test',
        last_name='User',
        role='DOCTOR'
    )
    print("✅ Тестовый пользователь 'testuser' создан")

# Создание врача
try:
    doctor_user = User.objects.get(username='doctor1')
    print("✅ Врач 'doctor1' уже существует")
except User.DoesNotExist:
    doctor_user = User.objects.create_user(
        username='doctor1',
        email='doctor1@hospital.com',
        password='doctor123',
        first_name='Uldana',
        last_name='Sagynay',
        role='DOCTOR'
    )
    print("✅ Врач 'doctor1' создан")

# Создание тестового пациента
try:
    patient_user = User.objects.get(username='patient1')
    print("✅ Пациент-пользователь 'patient1' уже существует")
    try:
        patient = Patient.objects.get(user=patient_user)
        print("✅ Профиль пациента уже существует")
    except Patient.DoesNotExist:
        patient = Patient.objects.create(
            user=patient_user,
            date_of_birth='1990-01-01',
            address='123 Test Street',
            phone_number='+1234567890'
        )
        print("✅ Профиль пациента создан")
except User.DoesNotExist:
    patient_user = User.objects.create_user(
        username='patient1',
        email='patient1@example.com',
        password='patient123',
        first_name='John',
        last_name='Doe',
        role='PATIENT'
    )
    print("✅ Пациент-пользователь 'patient1' создан")
    
    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth='1990-01-01',
        address='123 Test Street',
        phone_number='+1234567890'
    )
    print("✅ Профиль пациента создан")

print("\n🎉 Все пользователи и данные созданы!")
print("\n📝 Данные для входа:")
print("Admin: admin / admin123")
print("Doctor: testuser / test123") 
print("Doctor2: doctor1 / doctor123")
print("Patient: patient1 / patient123")
