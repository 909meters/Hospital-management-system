# 🏥 Полное руководство по ручной проверке Hospital Management System

## 📋 Оглавление
1. [Подготовка к тестированию](#подготовка-к-тестированию)
2. [Запуск системы](#запуск-системы)
3. [Тестирование Backend API](#тестирование-backend-api)
4. [Тестирование Frontend (Streamlit)](#тестирование-frontend-streamlit)
5. [Тестирование CRUD операций](#тестирование-crud-операций)
6. [Тестирование безопасности](#тестирование-безопасности)
7. [Тестирование производительности](#тестирование-производительности)
8. [Проверка логов и ошибок](#проверка-логов-и-ошибок)

---

## 1. Подготовка к тестированию

### 1.1 Проверка окружения
```bash
# Активировать виртуальное окружение
.\envir\Scripts\Activate.ps1

# Проверить установленные пакеты
pip list

# Проверить версию Python
python --version
```

### 1.2 Проверка базы данных
```bash
cd hospital_system
python manage.py migrate --check
python manage.py showmigrations
```

### 1.3 Создание тестовых данных
```bash
# Создать суперпользователя (если не существует)
python manage.py createsuperuser

# Проверить тестового пользователя
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings_local')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.get(username='testuser')
    print(f'Тестовый пользователь найден: {user.username}, роль: {user.role}')
except User.DoesNotExist:
    print('Тестовый пользователь не найден, создаем...')
    user = User.objects.create_user(
        username='testuser',
        password='test123',
        email='test@hospital.com',
        first_name='Test',
        last_name='User',
        role='DOCTOR'
    )
    print(f'Создан пользователь: {user.username}')
"
```

---

## 2. Запуск системы

### 2.1 Запуск Backend сервера
```bash
# В первом терминале
cd hospital_system
python manage.py runserver 127.0.0.1:8000
```

**✅ Проверки:**
- [ ] Сервер запустился без ошибок
- [ ] Доступен по адресу http://127.0.0.1:8000
- [ ] Admin панель доступна по http://127.0.0.1:8000/admin/

### 2.2 Запуск Frontend приложения
```bash
# Во втором терминале
cd frontend
streamlit run hospital_app.py --server.port 8501
```

**✅ Проверки:**
- [ ] Streamlit запустился без ошибок
- [ ] Доступен по адресу http://localhost:8501
- [ ] Отображается страница логина

---

## 3. Тестирование Backend API

### 3.1 Тест соединения
```bash
python test_api_endpoints.py
```

**Ожидаемый результат:**
```
🏥 Hospital Management System API Test
==================================================
🔐 Testing login...
✅ Login successful! Token: 1f60fa01f3e8962c3108...
🔍 Testing Patients (/patients/)...
✅ Patients: 200 - X items
🔍 Testing Appointments (/scheduling/appointments/)...
✅ Appointments: 200 - X items
🔍 Testing Doctors (/users/doctors/)...
✅ Doctors: 200 - X items
🔍 Testing User Profile (/auth/profile/)...
✅ User Profile: 200 - Data received
✅ API testing completed!
```

### 3.2 Ручная проверка API через curl/PowerShell

#### 3.2.1 Тест авторизации
```powershell
# Получение токена
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login/" -Method Post -ContentType "application/json" -Body '{"username":"testuser","password":"test123"}'
$token = $response.token
Write-Host "Token: $token"
```

#### 3.2.2 Тест защищенных эндпоинтов
```powershell
# Заголовки с токеном
$headers = @{"Authorization" = "Token $token"}

# Тест пациентов
$patients = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/patients/" -Headers $headers
Write-Host "Patients count: $($patients.count)"

# Тест записей на прием
$appointments = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/scheduling/appointments/" -Headers $headers
Write-Host "Appointments count: $($appointments.count)"

# Тест докторов
$doctors = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/doctors/" -Headers $headers
Write-Host "Doctors count: $($doctors.count)"
```

### 3.3 Проверка CORS
```javascript
// Открыть браузер и в консоли выполнить:
fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        password: 'test123'
    })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

---

## 4. Тестирование Frontend (Streamlit)

### 4.1 Проверка страницы логина
1. **Открыть**: http://localhost:8501
2. **Проверить элементы:**
   - [ ] Заголовок "🏥 Hospital Management System"
   - [ ] Поля ввода "Username" и "Password"
   - [ ] Кнопка "Login"
   - [ ] Корректное отображение CSS стилей

### 4.2 Тест авторизации
1. **Ввести данные:**
   - Username: `testuser`
   - Password: `test123`
2. **Нажать "Login"**
3. **Проверить:**
   - [ ] Сообщение "Login successful!"
   - [ ] Переход на главную панель
   - [ ] Отображение имени пользователя в сайдбаре
   - [ ] Отображение роли пользователя

### 4.3 Тест навигации
**Проверить доступность всех страниц:**
- [ ] Dashboard Overview
- [ ] Patients
- [ ] Appointments
- [ ] Medical Records
- [ ] Users

### 4.4 Тест выхода
1. **Нажать "Logout" в сайдбаре**
2. **Проверить:**
   - [ ] Возврат на страницу логина
   - [ ] Очистка сессии
   - [ ] Невозможность доступа к защищенным страницам

---

## 5. Тестирование CRUD операций

### 5.1 Управление пациентами

#### 5.1.1 Просмотр списка пациентов
1. **Перейти на страницу "Patients"**
2. **Проверить:**
   - [ ] Загрузка списка пациентов
   - [ ] Отображение полной информации
   - [ ] Корректное форматирование данных

#### 5.1.2 Добавление нового пациента
1. **Перейти на вкладку "Add New Patient"**
2. **Заполнить форму:**
   ```
   First Name: Иван
   Last Name: Петров
   Date of Birth: 1990-01-15
   Phone: +7-777-123-4567
   Address: ул. Абая 123, Алматы
   ```
3. **Нажать "Add Patient"**
4. **Проверить:**
   - [ ] Сообщение об успешном добавлении
   - [ ] Пациент появился в списке
   - [ ] Корректное отображение данных

#### 5.1.3 Просмотр деталей пациента
1. **Выбрать пациента из списка**
2. **Проверить отображение:**
   - [ ] Полная информация о пациенте
   - [ ] Корректное форматирование
   - [ ] Все поля заполнены

### 5.2 Управление записями на прием

#### 5.2.1 Просмотр записей
1. **Перейти на страницу "Appointments"**
2. **Проверить:**
   - [ ] Загрузка списка записей
   - [ ] Отображение в виде таблицы
   - [ ] Корректные даты и время

#### 5.2.2 Создание новой записи
1. **Перейти на вкладку "Schedule New Appointment"**
2. **Заполнить форму:**
   ```
   Patient: [Выбрать пациента]
   Doctor: [Выбрать доктора]
   Date: [Завтрашняя дата]
   Time: 14:30
   Notes: Плановый осмотр
   ```
3. **Нажать "Schedule Appointment"**
4. **Проверить:**
   - [ ] Сообщение об успешном создании
   - [ ] Запись появилась в списке

### 5.3 Медицинские записи

#### 5.3.1 Просмотр медицинских записей
1. **Перейти на страницу "Medical Records"**
2. **Выбрать пациента**
3. **Проверить:**
   - [ ] Загрузка записей пациента
   - [ ] Корректное отображение истории

#### 5.3.2 Добавление медицинской записи
1. **Перейти на вкладку "Add New Medical Record"**
2. **Заполнить форму:**
   ```
   Diagnosis: Острая респираторная инфекция
   Treatment: Симптоматическое лечение
   Medications: Парацетамол 500мг 3 раза в день
   Notes: Рекомендован постельный режим
   ```
3. **Нажать "Add Medical Record"**
4. **Проверить:**
   - [ ] Успешное добавление записи
   - [ ] Отображение в истории пациента

### 5.4 Управление пользователями

#### 5.4.1 Просмотр списка докторов
1. **Перейти на страницу "Users"**
2. **Проверить:**
   - [ ] Загрузка списка докторов
   - [ ] Отображение информации о врачах

#### 5.4.2 Добавление нового доктора
1. **Перейти на вкладку "Add New User"**
2. **Заполнить форму:**
   ```
   Username: doctor_new
   Email: new.doctor@hospital.com
   Password: secure123
   First Name: Анна
   Last Name: Смирнова
   Role: DOCTOR
   ```
3. **Нажать "Create User"**
4. **Проверить:**
   - [ ] Успешное создание пользователя
   - [ ] Доктор появился в списке

---

## 6. Тестирование безопасности

### 6.1 Проверка аутентификации
```bash
# Тест без токена
curl -X GET http://127.0.0.1:8000/api/patients/
# Ожидаемый результат: 401 Unauthorized

# Тест с неверным токеном
curl -H "Authorization: Token invalid_token" -X GET http://127.0.0.1:8000/api/patients/
# Ожидаемый результат: 401 Unauthorized
```

### 6.2 Проверка авторизации
1. **Создать пользователя с ролью PATIENT**
2. **Попробовать получить доступ к данным пациентов**
3. **Ожидаемый результат: 403 Forbidden**

### 6.3 Проверка валидации данных
1. **Попробовать создать пациента с неполными данными**
2. **Проверить валидацию email адресов**
3. **Проверить валидацию номеров телефонов**

---

## 7. Тестирование производительности

### 7.1 Нагрузочное тестирование API
```python
# Создать файл load_test.py
import requests
import time
import threading

def test_login():
    start_time = time.time()
    response = requests.post('http://127.0.0.1:8000/api/auth/login/', 
                           json={'username': 'testuser', 'password': 'test123'})
    end_time = time.time()
    print(f"Login time: {end_time - start_time:.2f}s, Status: {response.status_code}")

# Запустить 10 параллельных запросов
threads = []
for i in range(10):
    thread = threading.Thread(target=test_login)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

### 7.2 Тестирование отзывчивости UI
1. **Проверить время загрузки страниц Streamlit**
2. **Проверить время отклика при переключении между страницами**
3. **Проверить поведение при больших объемах данных**

---

## 8. Проверка логов и ошибок

### 8.1 Проверка логов Django
```bash
# В терминале с Django сервером проверить:
# - Отсутствие ошибок 500
# - Корректные HTTP коды ответов
# - Время выполнения запросов
```

### 8.2 Проверка логов Streamlit
```bash
# В терминале с Streamlit проверить:
# - Отсутствие Python исключений
# - Корректную работу сессий
# - Правильную обработку ошибок API
```

### 8.3 Проверка в браузере
1. **Открыть Developer Tools (F12)**
2. **Проверить Console на ошибки JavaScript**
3. **Проверить Network tab на failed requests**
4. **Проверить время загрузки ресурсов**

---

## 9. Чек-лист финальной проверки

### 9.1 Backend ✅
- [ ] Django сервер запускается без ошибок
- [ ] Все API эндпоинты отвечают корректно
- [ ] Аутентификация работает
- [ ] Авторизация настроена правильно
- [ ] CORS настроен корректно
- [ ] База данных мигрирована
- [ ] Admin панель доступна

### 9.2 Frontend ✅
- [ ] Streamlit приложение запускается
- [ ] Логин/логаут работает
- [ ] Все страницы загружаются
- [ ] CRUD операции выполняются
- [ ] Валидация форм работает
- [ ] Обработка ошибок корректна

### 9.3 Интеграция ✅
- [ ] Frontend успешно взаимодействует с Backend
- [ ] Данные корректно передаются между компонентами
- [ ] Сессии управляются правильно
- [ ] Токены обновляются при необходимости

### 9.4 Безопасность ✅
- [ ] Неавторизованный доступ заблокирован
- [ ] Роли пользователей работают корректно
- [ ] Валидация входных данных активна
- [ ] Токены защищены

---

## 10. Документация результатов

### 10.1 Отчет о тестировании
Заполнить таблицу результатов:

| Компонент | Тест | Статус | Примечания |
|-----------|------|--------|------------|
| Backend API | Login | ✅/❌ | |
| Backend API | Patients CRUD | ✅/❌ | |
| Backend API | Appointments CRUD | ✅/❌ | |
| Frontend | Login UI | ✅/❌ | |
| Frontend | Navigation | ✅/❌ | |
| Frontend | Forms | ✅/❌ | |
| Integration | API Connection | ✅/❌ | |
| Security | Authentication | ✅/❌ | |
| Security | Authorization | ✅/❌ | |

### 10.2 Выявленные проблемы
Документировать все найденные проблемы с указанием:
- Описание проблемы
- Шаги для воспроизведения
- Ожидаемое поведение
- Фактическое поведение
- Критичность (High/Medium/Low)

---

## 🎯 Заключение

После выполнения всех проверок система Hospital Management System должна:
- ✅ Полностью функционировать
- ✅ Обеспечивать безопасность данных
- ✅ Предоставлять удобный интерфейс
- ✅ Быть готовой к production развертыванию

**Время выполнения полной проверки: ~2-3 часа**
