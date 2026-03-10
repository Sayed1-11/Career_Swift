import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CareerSwift.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from employee.models import Employee

# Ensure cleanup before test
existing_user = User.objects.filter(email='new_employer@demo.com').first()
if existing_user:
    existing_user.delete()

client = Client()

print("\n--- Testing Employer Registration GET ---")
response = client.get('/register/')
print("Access /register/ - Status:", response.status_code)
# We expect to hit employee_register using /register/ from employee.urls but account uses it too.
# Let's check which template is rendered or what form is used.
if response.status_code == 200:
    print("Template used:", [t.name for t in response.templates])

print("\n--- Testing Employer Registration POST ---")
data = {
    'first_name': 'New',
    'last_name': 'Employer',
    'email': 'new_employer@demo.com',
    'password': 'StrongPassword123!',
    'confirm_password': 'StrongPassword123!',
    'company_name': 'Demo Corp',
    'Company_number': '1234567890'
}

response = client.post('/register/', data, follow=True)
print("Submit /register/ - Status:", response.status_code)

# Check if user and employee were created
new_user = User.objects.filter(email='new_employer@demo.com').first()
if new_user:
    print(f"User created: {new_user.email}, mapped username: {new_user.username}")
    is_employee = Employee.objects.filter(user=new_user).exists()
    print("Is an Employee?", is_employee)
    if is_employee:
        emp = Employee.objects.get(user=new_user)
        print(f"Employee Company Name: {emp.company_name}")
else:
    print("User was NOT created.")
    # Print form errors if any
    if hasattr(response, 'context') and 'form' in response.context:
        print("Form Errors:", response.context['form'].errors)

