import os
import zipfile

# --- PROJECT CONTENT DEFINITION ---
project_files = {
    # ROOT FILES
    "requirements.txt": """django\npsycopg2-binary\ngoogle-api-python-client\ngoogle-auth-oauthlib\nrequests\npython-dotenv""",
    "README.md": """# Mini Hospital Management System (HMS)
1. Install PostgreSQL and create a DB named 'hms_db'.
2. Run 'pip install -r requirements.txt'.
3. Run 'python manage.py migrate'.
4. In 'email_service' folder, run 'npm install' and 'sls offline'.
5. Run 'python manage.py runserver'.""",

    # DJANGO PROJECT CONFIG
    "hms_main/settings.py": """import os\nfrom pathlib import Path\nBASE_DIR = Path(__file__).resolve().parent.parent\nSECRET_KEY = 'hms-secret-key'\nDEBUG = True\nALLOWED_HOSTS = []\nINSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','appointments',]\nAUTH_USER_MODEL = 'appointments.User'\nDATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql','NAME': 'hms_db','USER': 'postgres','PASSWORD': 'your_password','HOST': '127.0.0.1','PORT': '5432'}}\nTEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [os.path.join(BASE_DIR, 'templates')],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages'],},}]""",
    "hms_main/urls.py": """from django.contrib import admin\nfrom django.urls import path, include\nurlpatterns = [path('admin/', admin.site.urls),path('', include('appointments.urls')),]""",

    # APPOINTMENTS APP
    "appointments/models.py": """from django.db import models\nfrom django.contrib.auth.models import AbstractUser\nclass User(AbstractUser):\n    is_doctor = models.BooleanField(default=False)\n    is_patient = models.BooleanField(default=False)\nclass Slot(models.Model):\n    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')\n    start_time = models.DateTimeField()\n    is_booked = models.BooleanField(default=False)\nclass Booking(models.Model):\n    patient = models.ForeignKey(User, on_delete=models.CASCADE)\n    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)""",
    "appointments/views.py": """from django.shortcuts import render, redirect\nfrom django.contrib.auth import login\nfrom .models import Slot, Booking\nfrom .forms import SignUpForm\nimport requests\ndef signup_view(request):\n    if request.method == 'POST':\n        form = SignUpForm(request.POST)\n        if form.is_valid():\n            user = form.save(commit=False)\n            if form.cleaned_data['role'] == 'doctor': user.is_doctor = True\n            else: user.is_patient = True\n            user.save(); login(request, user)\n            requests.post("http://localhost:3000/dev/send-email", json={"type": "SIGNUP_WELCOME", "email": user.email})\n            return redirect('dashboard')\n    return render(request, 'signup.html', {'form': SignUpForm()})\ndef dashboard(request):\n    if request.user.is_doctor: return render(request, 'doctor_dashboard.html', {'slots': Slot.objects.filter(doctor=request.user)})\n    return render(request, 'patient_dashboard.html', {'slots': Slot.objects.filter(is_booked=False)})""",
    "appointments/urls.py": """from django.urls import path\nfrom . import views\nurlpatterns = [path('signup/', views.signup_view, name='signup'),path('', views.dashboard, name='dashboard'),]""",
    "appointments/forms.py": """from django import forms\nfrom django.contrib.auth.forms import UserCreationForm\nfrom .models import User\nclass SignUpForm(UserCreationForm):\n    role = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')])\n    class Meta(UserCreationForm.Meta): model = User; fields = UserCreationForm.Meta.fields + ('email',)""",

    # EMAIL SERVICE (SERVERLESS)
    "email_service/handler.py": """import json\ndef send_email(event, context):\n    body = json.loads(event.get('body', '{}'))\n    print(f"Email sent to {body.get('email')}")\n    return {"statusCode": 200, "body": json.dumps({"message": "Success"})}""",
    "email_service/serverless.yml": """service: hms-email\nprovider:\n  name: aws\n  runtime: python3.9\nfunctions:\n  send-email:\n    handler: handler.send_email\n    events: [{http: {path: send-email, method: post}}]\nplugins: [serverless-offline]""",

    # FRONTEND TEMPLATES
    "templates/base.html": """<html><head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head><body>{% block content %}{% endblock %}</body></html>""",
    "templates/signup.html": """{% extends 'base.html' %}{% block content %}<h2>Sign Up</h2><form method="post">{% csrf_token %}{{ form.as_p }}<button type="submit">Join</button></form>{% endblock %}""",
}

def create_structure():
    base_dir = "mini_hms_project"
    if not os.path.exists(base_dir): os.makedirs(base_dir)

    for path, content in project_files.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

    # Zip the project
    with zipfile.ZipFile("hms_project_final.zip", "w") as zf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), base_dir))
    print("DONE! Created folder 'mini_hms_project' and 'hms_project_final.zip'")

if __name__ == "__main__":
    create_structure()