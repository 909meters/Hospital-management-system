import os
import sys
import django

# Set the Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings_local')

# Setup Django
sys.path.append(r'c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\hospital_system')
django.setup()

from users.models import CustomUser

print("🔍 Checking existing users:")
users = CustomUser.objects.all()

if users.exists():
    for user in users:
        print(f"  - Username: {user.username}")
        print(f"    Email: {user.email}")
        print(f"    Role: {user.role}")
        print(f"    Active: {user.is_active}")
        print(f"    Staff: {user.is_staff}")
        print(f"    Superuser: {user.is_superuser}")
        print()
else:
    print("  No users found!")

print("\n🔧 Creating test user for demo...")
try:
    # Create a test user if it doesn't exist
    test_user, created = CustomUser.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@hospital.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'doctor',
            'is_active': True
        }
    )
    
    if created:
        test_user.set_password('test123')
        test_user.save()
        print(f"✅ Created test user: testuser / test123")
    else:
        print(f"✅ Test user already exists: testuser")
        
except Exception as e:
    print(f"❌ Error creating test user: {e}")

print("\n👤 Final user list:")
for user in CustomUser.objects.all():
    print(f"  - {user.username} ({user.role}) - Active: {user.is_active}")
