"""
Django settings for Gracie Hospital Management System
Location: Hebbal, Mysore, Karnataka, India
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

from environs import Env
env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g$95qor-(xnlh_nb-vo^sn2v!d+g+_8@eo*6#^p3rh3tjwngs5'

DEBUG = True

ALLOWED_HOSTS = ['*']
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'userauths',
    'doctor',
    'patient',
    'anymail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hms_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'base.context.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hms_prj.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── India / Mysore Locale ───────────────────────────────────────────────────
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─── Static / Media ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "userauths:sign-in"
LOGIN_REDIRECT_URL = ""
LOGOUT_REDIRECT_URL = "userauths:sign-in"
AUTH_USER_MODEL = 'userauths.User'

MESSAGE_TAGS = {messages.ERROR: 'danger'}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ─── Google Pay / UPI ────────────────────────────────────────────────────────
GPAY_UPI_ID = "kirancrispy@okicici"
GPAY_MERCHANT_NAME = "Gracie Hospital Management"
GPAY_MERCHANT_CODE = "GRACIEHOSP001"

# ─── Email ───────────────────────────────────────────────────────────────────
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY", ""),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN", ""),
}
FROM_EMAIL = env('FROM_EMAIL', default='noreply@graciehospital.in')
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Gracie Hospital <noreply@graciehospital.in>')
SERVER_EMAIL = env('SERVER_EMAIL', default='noreply@graciehospital.in')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kiraj8899@gmail.com'       # ← your Gmail
EMAIL_HOST_PASSWORD = 'dbqe dfjf nbcj qlbs'   # ← Gmail App Password (see below)
DEFAULT_FROM_EMAIL = 'Gracie Hospital <kiraj8899gmail@gmail.com>'


# ─── Jazzmin Admin Theme ─────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_title': "Gracie Hospital Admin",
    'site_header': "Gracie Hospital",
    'site_brand': "Gracie Hospital",
    'copyright': "Gracie Hospital Management, Hebbal, Mysore © 2024",
    'welcome_sign': "Welcome to Gracie Hospital Admin Panel",
    'order_with_respect_to': ['base'],
    'icons': {
        'admin.LogEntry': 'fas fa-file',
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
    },
    'show_ui_builder': True,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': True,
    'brand_colour': 'navbar-success',
    'accent': 'accent-success',
    'navbar': 'navbar-success navbar-dark',
    'no_navbar_border': False,
    'navbar_fixed': False,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-success',
    'sidebar_nav_small_text': False,
    'sidebar_nav_compact_style': True,
    'theme': 'default',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}
