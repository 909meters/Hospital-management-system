#!/usr/bin/env python3
"""
Скрипт для тестирования API больничной системы
"""

import requests
import json
import random
import string

# Базовые настройки
BASE_URL = "http://127.0.0.1:8000"
USERNAME = "testdoctor"  # Замените на реальное имя пользователя
PASSWORD = "testdoc123"  # Замените на реальный пароль

def get_token(username, password):
    """Получение токена аутентификации"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token_data = response.json()
        print("✅ Токен получен успешно!")
        print(f"Token: {token_data['token']}")
        print(f"User: {token_data['username']} ({token_data['role']})")
        return token_data['token']
    else:
        print("❌ Ошибка получения токена:")
        print(response.text)
        return None

def test_protected_endpoint(token):
    """Тестирование защищенного endpoint"""
    url = f"{BASE_URL}/api/auth/profile/"
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        print("✅ Профиль пользователя получен:")
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))
        return True
    else:
        print("❌ Ошибка получения профиля:")
        print(response.text)
        return False

def test_patients_api(token):
    """Тестирование API пациентов"""
    url = f"{BASE_URL}/api/patients/patients/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Получение списка пациентов
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        patients = response.json()
        print(f"✅ Получен список пациентов: {len(patients.get('results', patients))} записей")
    else:
        print("❌ Ошибка получения списка пациентов:")
        print(response.text)
        return False
    
    # Создание нового пациента
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    new_patient = {
        "first_name": f"Тест-{random_suffix}",
        "last_name": "Пациент",
        "date_of_birth": "1990-01-01",
        "phone_number": f"+7 (999) 999-{random.randint(10,99)}-{random.randint(10,99)}",
        "email": f"test.patient.{random_suffix}@email.com",
        "address": f"Тестовый адрес {random_suffix}"
    }
    
    response = requests.post(url, json=new_patient, headers=headers)
    if response.status_code == 201:
        created_patient = response.json()
        print(f"✅ Пациент создан! Ответ сервера:")
        print(json.dumps(created_patient, indent=2, ensure_ascii=False))
        return created_patient.get('id')
    else:
        print("❌ Ошибка создания пациента:")
        print(f"Status: {response.status_code}")
        print(response.text)
        return None

def main():
    """Основная функция для тестирования"""
    print("🏥 Тестирование API больничной системы")
    print("=" * 50)
    
    # Получение токена
    token = get_token(USERNAME, PASSWORD)
    if not token:
        print("❌ Невозможно продолжить без токена")
        return
    
    print("\n" + "=" * 50)
    
    # Тестирование профиля
    test_protected_endpoint(token)
    
    print("\n" + "=" * 50)
    
    # Тестирование API пациентов
    patient_id = test_patients_api(token)
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    main()
