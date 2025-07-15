#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Set admin password
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("Admin password set to 'admin123'")
    print(f"Admin user: {admin_user.username}")
    print(f"Is staff: {admin_user.is_staff}")
    print(f"Is superuser: {admin_user.is_superuser}")
except User.DoesNotExist:
    print("Admin user not found")
