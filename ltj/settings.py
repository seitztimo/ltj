import os
import environ
import raven

root = environ.Path(__file__) - 2
BASE_DIR = root()

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    SHARED_SECRET=(str, ''),
    ALLOWED_HOSTS=(list, []),
    ADMINS=(list, []),
    DATABASE_URL=(str, 'postgis:///ltj'),
    MEDIA_ROOT=(environ.Path(), root('media')),
    STATIC_ROOT=(environ.Path(), root('static')),
    MEDIA_URL=(str, '/media/'),
    STATIC_URL=(str, '/static/'),
    LOG_LEVEL=(str, 'INFO'),
    SENTRY_DSN=(str, ''),
    SENTRY_ENVIRONMENT=(str, 'unconfigured'),
    WFS_SERVER_URL=(str, 'http://localhost/'),
    WFS_NAMESPACE=(str, 'ltj-dev'),
)

# .env file, should load only in development environment
DISABLE_CONFIG_FILES = env.bool('DJANGO_DISABLE_CONFIG_FILES', default=False)
if not DISABLE_CONFIG_FILES:
    env_file = root('config.env')
    env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY')
SHARED_SECRET = env('SHARED_SECRET')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
ADMINS = env('ADMINS')

STATIC_URL = env('STATIC_URL')
MEDIA_URL = env('MEDIA_URL')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_ROOT = env('MEDIA_ROOT')

# log to stderr, at level specified by LOG_LEVEL and add metadata
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'metadata': {
            'format': '%(asctime)s %(levelname)s %(module)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'metadata',
            'level': env('LOG_LEVEL'),
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOG_LEVEL'),
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'ckeditor',
    'rest_framework',
    'rest_framework_gis',
    'nature',
    'imports',
    'files',
]

# Sentry
if env('SENTRY_DSN'):
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        'environment': env('SENTRY_ENVIRONMENT'),
        'release': raven.fetch_git_sha(BASE_DIR),
    }
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'ltj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('templates')],
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

WSGI_APPLICATION = 'ltj.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

DATABASES = {
    'default': env.db(),
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

LANGUAGE_CODE = 'fi'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom settings

SRID = 3879  # Spatial reference system identifier used for geometry fields

WFS_SERVER_URL = env('WFS_SERVER_URL')  # WFS server url for features
WFS_NAMESPACE = env('WFS_NAMESPACE')  # Namespace for WFS layers
