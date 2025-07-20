import os
from pathlib import Path
import environ
from django.contrib.messages import constants

# Criando arquivos de ambiente
env=environ.Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY=env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['192.168.0.251','localhost','127.0.0.1',]


# Application definition

INSTALLED_APPS = [


    #app
    'usuarios',
    'cidadao',
    'despesas',
    'transportes',
    'core',
    'profissionais',
    'tfds',
    'estabelecimentos',
    'especialidades',
    'relatorios',

    #Pacote
   
    'bootstrap5',
    "widget_tweaks",
    'crispy_forms',
    "crispy_bootstrap5",
    'django.contrib.admin',
    'django.contrib.auth',
    'django_select2',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rolepermissions',
    
    
    
    #pacote
    "localflavor",
    'dbbackup',
   # "debug_toolbar",
    
   
    
   
    
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = 'bootstrap5' 

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgtdv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'sgtdv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD':env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'), 
        }
    }
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    'static'
]


#configuração da pasta de Media(arquivos, fotos, videos)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}


DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/servidor-regulacao/Documentos/BACKUP SGTDV'}

SELECT2_CACHE_BACKEND = "select2"


MESSAGE_TAGS = {

    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.DEBUG: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
}

ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True

AUTH_USER_MODEL = "usuarios.Usuario"
LOGIN_URL= 'usuarios:login_usuario'
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = 'usuarios:login_usuario'


#Configuracao do servidor de email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

#INTERNAL_IPS = [
    # ...
   # "127.0.0.1",
    # ...
#]

ROLEPERMISSIONS_MODULE = "sgtdv.roles"
