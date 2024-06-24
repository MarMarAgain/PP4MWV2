"""
Django settings for PP4MWV2 project.


Generated by 'django-admin startproject' using Django 5.0.6.


For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/


For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""


from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-alcdllu=h@9-lyb8q5vp@ko^w$=*og2$q6$igd&1n%t(h*#a^-'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Local development server's URL is trusted
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']

# False for development and True for production
CSRF_COOKIE_SECURE = False


# Application definition

INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   "accounts.apps.AccountsConfig",
   "workshops.apps.WorkshopsConfig",
   "purchase.apps.PurchaseConfig",
   "other_pages.apps.OtherPagesConfig",
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


ROOT_URLCONF = 'PP4MWV2.urls'


TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
       'APP_DIRS': True,
       'OPTIONS': {
           'context_processors': [
               'django.template.context_processors.debug',
               'django.template.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               #'django.template.context_processors.csrf', #disabled for testing
               'django.contrib.messages.context_processors.messages',
           ],
       },
   },
]


WSGI_APPLICATION = 'PP4MWV2.wsgi.application'




# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'UTC'


USE_I18N = True


USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'


STATICFILES_DIRS = [BASE_DIR / "static"]


STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Payment configurations
PAYMENT_VARIANTS = {
   'default': ('payments.dummy.DummyProvider', {
       'client_id': 'dummy_client_id',
       'secret': 'dummy_secret'
   }),
   'stripe': ('payments.stripe.StripeProvider', {
       'secret_key': 'sk_test_your_stripe_secret_key',
       'public_key': 'pk_test_your_stripe_public_key'
   }),
   'paypal': ('payments.paypal.PaypalProvider', {
       'client_id': 'your_paypal_client_id',
       'secret': 'your_paypal_secret',
       'endpoint': 'https://api.sandbox.paypal.com',  # Use sandbox endpoint for testing
   })
}


PAYMENT_HOST = os.environ.get('PAYMENT_HOST', 'localhost')