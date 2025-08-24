#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings_simple')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='testuser')

# Обновим пароль
user.set_password('test123')
user.save()

print(f'Пароль для пользователя {user.username} обновлен!')
print(f'Проверка пароля: {user.check_password("test123")}')
