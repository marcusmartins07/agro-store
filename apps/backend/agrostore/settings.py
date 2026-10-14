from datetime import timedelta
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-development-only-change-me',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'true').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if host.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'agrostore.main',
    'agrostore.usuarios',
    'agrostore.lojas',
    'agrostore.produtos',
    'agrostore.carrinhos',
    'agrostore.pedidos',
    'agrostore.favoritos',
    'agrostore.avaliacoes',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agrostore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'agrostore.wsgi.application'

def configurar_banco(database_url):
    if not database_url:
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }

    # Formato: postgresql://usuario:senha@host:porta/banco (ex.: Session pooler do Supabase).
    url = urlparse(database_url)
    if url.scheme not in ('postgres', 'postgresql'):
        raise ImproperlyConfigured('DATABASE_URL deve usar o esquema postgresql://.')

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote(url.path.lstrip('/')),
        'USER': unquote(url.username or ''),
        'PASSWORD': unquote(url.password or ''),
        'HOST': url.hostname,
        'PORT': url.port or 5432,
        # 0 fecha a conexão ao fim de cada requisição. O runserver cria uma thread por requisição,
        # então conexões persistentes ficam presas e esgotam o limite do Session pooler do Supabase.
        'CONN_MAX_AGE': int(os.getenv('DATABASE_CONN_MAX_AGE', '0')),
        # Necessário quando a conexão passa pelo Transaction pooler (porta 6543).
        'DISABLE_SERVER_SIDE_CURSORS': True,
        'OPTIONS': {'sslmode': os.getenv('DATABASE_SSLMODE', 'require')},
    }


DATABASES = {
    'default': configurar_banco(os.getenv('DATABASE_URL', '').strip()),
}

AUTH_USER_MODEL = "usuarios.Usuario"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Sem SUPABASE_STORAGE_BUCKET, os uploads ficam em MEDIA_ROOT (desenvolvimento local).
SUPABASE_STORAGE_BUCKET = os.getenv('SUPABASE_STORAGE_BUCKET', '').strip()

if SUPABASE_STORAGE_BUCKET:
    SUPABASE_URL = os.getenv('SUPABASE_URL', '').strip().rstrip('/')
    configuracoes_storage = {
        'SUPABASE_URL': SUPABASE_URL,
        'SUPABASE_S3_ACCESS_KEY_ID': os.getenv('SUPABASE_S3_ACCESS_KEY_ID', '').strip(),
        'SUPABASE_S3_SECRET_ACCESS_KEY': os.getenv('SUPABASE_S3_SECRET_ACCESS_KEY', '').strip(),
        'SUPABASE_S3_REGION': os.getenv('SUPABASE_S3_REGION', '').strip(),
    }
    faltando = [nome for nome, valor in configuracoes_storage.items() if not valor]
    if faltando:
        raise ImproperlyConfigured(f'Variáveis obrigatórias para o Supabase Storage: {", ".join(faltando)}.')

    url_supabase = urlparse(SUPABASE_URL)
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'bucket_name': SUPABASE_STORAGE_BUCKET,
                'endpoint_url': f'{SUPABASE_URL}/storage/v1/s3',
                'region_name': configuracoes_storage['SUPABASE_S3_REGION'],
                'access_key': configuracoes_storage['SUPABASE_S3_ACCESS_KEY_ID'],
                'secret_key': configuracoes_storage['SUPABASE_S3_SECRET_ACCESS_KEY'],
                'addressing_style': 'path',
                'file_overwrite': False,
                # Bucket público: a URL salva aponta para o endpoint público, sem assinatura temporária.
                'querystring_auth': False,
                'custom_domain': f'{url_supabase.netloc}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}',
            },
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:5173,http://127.0.0.1:5173',
    ).split(',')
    if origin.strip()
]
