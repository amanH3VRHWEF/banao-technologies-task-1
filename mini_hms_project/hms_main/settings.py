import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'hms-secret-key'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','appointments',]
AUTH_USER_MODEL = 'appointments.User'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql','NAME': 'hms_db','USER': 'postgres','PASSWORD': 'your_password','HOST': '127.0.0.1','PORT': '5432'}}
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [os.path.join(BASE_DIR, 'templates')],'APP_DIRS': True,'OPTIONS': {'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages'],},}]