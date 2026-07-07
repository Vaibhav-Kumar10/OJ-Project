from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost").split(
    ","
)

# CSRF_TRUSTED_ORIGINS = [
#     "https://oj-project-w5uv.onrender.com",
#     "https://codeforge-hnfg.onrender.com",
#     "https://my-ojproject.onrender.com",
# ]

# ALLOWED_HOSTS = [
#     "13.233.196.157",
#     "oj-project-w5uv.onrender.com",
#     "codeforge-hnfg.onrender.com",
#     "my-ojproject.onrender.com",
#     "*",
# ]

AUTH_USER_MODEL = "user_auth.User"
LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"

# ------------------------------------------------------------------
# APPS & MIDDLEWARE
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "user_auth",
    "core",
    "contests",
    "compiler",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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
]

ROOT_URLCONF = "oj.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "oj.wsgi.application"

# ------------------------------------------------------------------
# DATABASE
# ssl_require=True  → only for hosted providers (Render, Railway)
# ssl_require=False → for local Docker postgres
# Controlled via DB_SSL env variable
# ------------------------------------------------------------------
_ssl = os.environ.get("DB_SSL", "False") == "True"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=_ssl,
    )
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB", "ojdb"),
#         "USER": os.getenv("POSTGRES_USER", "ojuser"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "ojpassword"),
#         "HOST": os.getenv(
#             "DB_HOST",
#             "db" if os.path.exists("/.dockerenv") else "localhost",
#         ),
#         "PORT": os.getenv("DB_PORT", "5432"),
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB", "ojdb"),
#         "USER": os.getenv("POSTGRES_USER", "ojuser"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "ojpassword"),
#         "HOST": os.getenv("DB_HOST", "db"),
#         "PORT": os.getenv("DB_PORT", "5432"),
#     }
# }


# ------------------------------------------------------------------
# COMPILER MICROSERVICE URL
# ------------------------------------------------------------------
# COMPILER_SERVICE_URL = os.environ.get("COMPILER_SERVICE_URL", "http://localhost:8001")
COMPILER_SERVICE_URL = os.getenv(
    "COMPILER_SERVICE_URL",
    (
        "http://compiler:8001"
        if os.path.exists("/.dockerenv")
        else "http://127.0.0.1:8001"
    ),
)


# ------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# INTERNATIONALISATION
# ------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATIC FILES
# ------------------------------------------------------------------
STATIC_URL = "/static/"

# Folders Django looks in during development (runserver / collectstatic source)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Where collectstatic dumps everything for production
# Whitenoise then serves files from here
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise compressed caching (good for production)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
