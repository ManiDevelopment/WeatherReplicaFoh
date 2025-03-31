# You should not edit this file unless you know what you're doing!
from pathlib import Path
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ General config
DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'django-insecure-session-key'

# ✅ REST framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# ✅ Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'data_wizard',
    'data_wizard.sources',
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',

    'MySourceReplica',
]

# ✅ Middleware stack
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'UnchangeableReplica.urls'

# ✅ Template config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # if you have global templates, add them here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'UnchangeableReplica.wsgi.application'

# ✅ Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Internationalisation
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'label_music_manager' / 'locale']

# ✅ Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # where your weather.js lives
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # for collectstatic (do NOT match staticfiles_dirs)

# ✅ Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Crispy forms (Bootstrap 5)
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ✅ Messages (flash tags)
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# ✅ CORS
CORS_ALLOW_ALL_ORIGINS = True

# ✅ Auth redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ✅ Email (dummy backend for dev)
SUPPORT_EMAIL = "support@UnchangeableReplica.com"
DEFAULT_FROM_EMAIL = "noreply@UnchangeableReplica.com"
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
