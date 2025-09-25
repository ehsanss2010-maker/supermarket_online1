from .base import *

DEBUG = True

# برای شروع ساده، از SQLite استفاده می‌کنیم
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# برنامه‌های اضافی برای توسعه
INSTALLED_APPS += [
    'django_extensions',
]

# ایمیل در حالت توسعه
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'