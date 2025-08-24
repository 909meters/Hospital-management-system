#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings_simple')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='testuser')

print(f'Username: {user.username}')
print(f'Role: {user.role}')
print(f'Is active: {user.is_active}')
print(f'Check password: {user.check_password("test123")}')
print(f'Email: {user.email}')
