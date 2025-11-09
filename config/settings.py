from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r347vdxssioux=x34$jpcf6$gnv7732psk*mjq1@r+=y0nku*c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'shop',
    'rest_framework',
    'drf_yasg',
    'django_extensions'
]

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_item_count',

            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# pour définir le multilinguisme
LANGUAGES = [
    ('fr', 'Français'),
    ('nl', 'Nederlands'),
]

# Langue par défaut
LANGUAGE_CODE = 'fr'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Paramètres de session pour gérer la langue
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
LANGUAGE_COOKIE_NAME = 'django_language'

# Répertoire où se trouvent les fichiers de traduction .po et .mo
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'UTC'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATICFILES_DIRS : Répertoire où Django cherchera les fichiers statiques supplémentaires
# Ici, on indique à Django de chercher dans le dossier 'static' à la racine du projet.
STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA_URL : URL qui permet d'accéder aux fichiers médias (images, vidéos, etc.)
# Par exemple, une image téléchargée sera accessible via '/media/nom_image.jpg'.
MEDIA_URL = '/media/'

# MEDIA_ROOT : Dossier où les fichiers téléchargés par les utilisateurs seront stockés
# Les fichiers téléchargés seront enregistrés dans un dossier 'media' à la racine du projet.
MEDIA_ROOT = BASE_DIR / 'media'

# user personnalisé
AUTH_USER_MODEL = 'accounts.Shopper'

# les clé stripe (la premiere est pour le backend et la 2eme est celle a mettre ds le script javascript dans la page user_orders.html)
STRIPE_SECRET_KEY = 'sk_test_51QMQIRFzkLwpXRndzsaIAzzr3atN3rbOsgYdq0afnM4u5TEpuxPuDhHowFYzICbMnYWFKZiMyEUrdgtPimEBAjAU00VPloTj6J'
STRIPE_PUBLISHABLE_KEY = "pk_test_51QMQIRFzkLwpXRndHrv4cEF348SeNqZwKgQ68sWR52Ax1SCyoYE4ziDYN0MWVfDKs8cypUtM3Fgw01iBVMORzOl2000vmyMj8s"


# infos pour l'adresse email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sweetyworld1180@gmail.com'
EMAIL_HOST_PASSWORD = 'vzuo yxhv mzuh vlws'
DEFAULT_FROM_EMAIL = 'sweetyworld1180@gmail.com'
