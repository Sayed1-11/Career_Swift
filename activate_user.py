import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CareerSwift.settings')
django.setup()

from django.contrib.auth.models import User

# Get the most recently created user
user = User.objects.order_by('-date_joined').first()
if user:
    user.is_active = True
    user.save()
    print(f"Successfully activated user: {user.username} ({user.email})")
else:
    print("No users found.")
