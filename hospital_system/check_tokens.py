#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import CustomUser

def check_and_create_tokens():
    """Check and create tokens for all users"""
    users = CustomUser.objects.all()
    
    for user in users:
        print(f"\n--- User: {user.username} ({user.role}) ---")
        
        # Check if token exists
        try:
            token = Token.objects.get(user=user)
            print(f"Token exists: {token.key}")
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            print(f"Created new token: {token.key}")
        
        # Test authentication
        auth_user = authenticate(username=user.username, password='testpass123')
        if auth_user:
            print(f"✅ Authentication successful")
        else:
            print(f"❌ Authentication failed")
            # Try to set password
            user.set_password('testpass123')
            user.save()
            print(f"Password reset for {user.username}")

if __name__ == "__main__":
    check_and_create_tokens()
