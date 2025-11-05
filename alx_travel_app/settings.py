# alx_travel_app/settings.py

import os
from pathlib import Path
import environ # 1. استيراد django-environ

# 1. تهيئة environ وقراءة ملف .env
env = environ.Env(
    # تعيين الأنواع الافتراضية للمتغيرات
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ----------------------------------------------------------------------
# Core Django Settings
# ----------------------------------------------------------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# 2. التطبيقات المثبتة (Installed Apps)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',        # djangorestframework
    'corsheaders',           # django-cors-headers
    'drf_yasg',              # Swagger/OpenAPI documentation
    
    # Project Apps
    'listings.apps.ListingsConfig', # التطبيق الجديد
]

# (MIDDLEWARE, TEMPLATES, AUTH_PASSWORD_VALIDATORS ... remain the same)

# ----------------------------------------------------------------------
# 3. إعداد قاعدة البيانات (MySQL)
# ----------------------------------------------------------------------
DATABASES = {
    # قراءة إعدادات MySQL من متغير DATABASE_URL في ملف .env
    'default': env.db(),
}


# ----------------------------------------------------------------------
# 4. إعداد Django REST Framework و CORS
# ----------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # يمكنك إضافة إعدادات أخرى هنا لاحقًا
}

# CORS Headers configuration
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_ALL_ORIGINS = DEBUG # السماح للكل في وضع التطوير (DEBUG=True)

# ----------------------------------------------------------------------
# 5. إعداد Celery (للتذكير في المستقبل)
# ----------------------------------------------------------------------
# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

# (STATIC_URL, DEFAULT_AUTO_FIELD ... remain the same)