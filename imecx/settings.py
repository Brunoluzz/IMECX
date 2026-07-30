"""
Django settings for Imecx project.
"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="dev-insecure-key-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

INSTALLED_APPS = [
    "jazzmin",  # antes do admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # third-party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_htmx",

    # local
    "core",
    "editions",
    "applications",
    "accounts",
    "dashboard",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "imecx.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",

                "tasks.context_processors.notifications_context",
            ],
        },
    },
]

WSGI_APPLICATION = "imecx.wsgi.application"

# Database
DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    import dj_database_url  # type: ignore  # opcional
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth / allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_REDIRECT_URL = "accounts:area_pessoal"
LOGOUT_REDIRECT_URL = "/"

# -------------------------
# django-allauth
# -------------------------

ACCOUNT_LOGIN_METHODS = {"email"}

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]

# obrigar confirmação do email
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# Não iniciar sessão imediatamente após o registo
ACCOUNT_LOGIN_ON_SIGNUP = False

# utilizador autenticado após confirmação
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# expiração do link (3 dias)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

# impedir enumeração de emails
ACCOUNT_PREVENT_ENUMERATION = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

ACCOUNT_ADAPTER = "accounts.adapter.IMECXAccountAdapter"

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[IMECX] "

ACCOUNT_CONFIRM_EMAIL_ON_GET = True

SITE_URL = "http://127.0.0.1:8000"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# Cloudinary opcional
CLOUDINARY_URL = config("CLOUDINARY_URL", default="")
if CLOUDINARY_URL and not DEBUG:
    INSTALLED_APPS += ["cloudinary", "cloudinary_storage"]
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Imecx Admin",
    "site_header": "Imecx",
    "site_brand": "Imecx Administração",
    "welcome_sign": "Bem-vindo à Administração Imecx",
    "copyright": "Imecx",
    "show_ui_builder": False,
    "site_logo_classes": "img-circle",
    "topmenu_links": [
        {"name": "Ver site", "url": "/", "new_window": True},
        {"app": "editions"},
    ],
    "order_with_respect_to": ["editions", "applications", "accounts", "auth"],
    "hide_apps": ["sites", "socialaccount"],
    "icons": {
        "editions.Edition": "fas fa-calendar-alt",
        "applications.Application": "fas fa-file-signature",
        "applications.EngineeringArea": "fas fa-cogs",
        "accounts.Profile": "fas fa-id-badge",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-primary",
}

LOGIN_URL = "/conta/login/"

ACCOUNT_FORMS = {
    "login": "accounts.allauth_forms.IMECXLoginForm",
    "signup": "accounts.allauth_forms.IMECXSignupForm",
    "reset_password": "accounts.allauth_forms.IMECXResetPasswordForm",
    "reset_password_key": "accounts.allauth_forms.IMECXResetPasswordKeyForm",
}
