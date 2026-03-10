import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CareerSwift.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from job_seeker.models import Job_seeker
from django.core.files.uploadedfile import SimpleUploadedFile

user = User.objects.order_by('-date_joined').first()
print(f"Testing with user: {user.username}")

client = Client()
client.force_login(user)

# Try uploading a PDF resume
file_content = b"%PDF-1.4\n%..."
resume_file = SimpleUploadedFile("dummy_resume.pdf", file_content, content_type="application/pdf")

response = client.post('/profile/', {'Resume': resume_file})
print("Response status:", response.status_code)
if response.status_code == 302:
    print("Redirect location:", response.url)

job_seeker = Job_seeker.objects.get(user=user)
if job_seeker.Resume:
    print("Resume uploaded successfully:", job_seeker.Resume.name)
else:
    print("Resume upload failed. Resume field is empty.")

# Let's see if the form errors are rendered if not 302
if response.status_code == 200:
    print("Response Context Form Errors:", response.context.get('form').errors if response.context and response.context.get('form') else None)
