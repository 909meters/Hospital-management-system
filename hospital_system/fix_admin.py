#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from users.models import CustomUser
from rest_framework.authtoken.models import Token

def fix_admin():
    try:
        admin = CustomUser.objects.get(username='admin')
        admin.set_password('testpass123')
        admin.save()
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=admin)
        
        print(f"Admin password updated!")
        print(f"Username: {admin.username}")
        print(f"Role: {admin.role}")
        print(f"Token: {token.key}")
        
    except CustomUser.DoesNotExist:
        admin = CustomUser.objects.create_user(
            username='admin',
            password='testpass123',
            email='admin@hospital.com',
            role='ADMIN',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        token = Token.objects.create(user=admin)
        print(f"Created new admin user!")
        print(f"Username: {admin.username}")
        print(f"Role: {admin.role}")
        print(f"Token: {token.key}")

if __name__ == "__main__":
    fix_admin()
