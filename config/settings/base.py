"""
Base settings to build other settings files upon.
"""
from datetime import timedelta
from pathlib import Path


def gettext_noop(s):
    return s


import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# autobuyfast/
APPS_DIR = ROOT_DIR / "autobuyfast"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Africa/Lagos"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("af", gettext_noop("Afrikaans")),
    ("ar", gettext_noop("Arabic")),
    ("en", gettext_noop("English")),
    ("es", gettext_noop("Spanish")),
    ("fr", gettext_noop("French")),
    ("ig", gettext_noop("Igbo")),
]

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = ["he", "ar", "ar-dz", "fa", "ur"]

# Settings for language cookie
LANGUAGE_COOKIE_NAME = "django_language"
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = "/"
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = None

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_ADMIN = [
    "tinymce",
    'filebrowser',
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "dal",
    "dal_select2",
    "admin_honeypot",
]

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "django_celery_beat",

    # Shell commands with imports to all necessary models
    "shell_plus",
    # Django country plus with list of all the countries available
    "countries_plus",
    # Django dynamic filtering based on model fields
    'django_filters',
    # django tables 2
    'django_tables2',
    # Category settings https://pypi.org/project/django-category/
    "category",
    # comments app
    "comment",

]

LOCAL_APPS = [
    "autobuyfast.users.apps.UsersConfig",
    # Your stuff: custom apps go here
    "autobuyfast.cars.apps.CarsConfig",
    "autobuyfast.blog.apps.BlogConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_ADMIN + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# latest update for django 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "autobuyfast.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
LOGOUT_URL = "account_logout"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
# Default hashing algorithm to use for encoding cookies, password reset tokens
# in the admin site, user sessions, and signatures. It's a transitional setting
# helpful in migrating multiple instance of the same project to Django 3.1+.
# Algorithm must be 'sha1' or 'sha256'.
DEFAULT_HASHING_ALGORITHM = "sha256"

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    # HTML Minification
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
    # Django default security middlewares
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE_CLASSES = MIDDLEWARE


# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"

# List of upload handler classes to be applied in order.
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # i.e. 25.0 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400  # i.e. 25.0 MB

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "autobuyfast.utils.context_processors.settings_context",
            ],
        },
    }
]

# Decimal separator symbol
DECIMAL_SEPARATOR = "."

# Boolean that sets whether to add thousand separator when formatting numbers
USE_THOUSAND_SEPARATOR = False

# Number of digits that will be together, when splitting them by
# THOUSAND_SEPARATOR. 0 means no grouping, 3 means splitting by thousands...
NUMBER_GROUPING = 0

# Thousand separator symbol
THOUSAND_SEPARATOR = ","

# Default primary key field type.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "dashboard/"
ADMIN_DOC_URL = "dashboard/doc/"
ADMIN_FILEBROWSER_URL = "dashboard/filebrowser/"

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Advance Scholar""", "info@autobuyfast.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
# if USE_TZ:
#     # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
#     CELERY_TIMEZONE = TIME_ZONE
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
# CELERY_ACCEPT_CONTENT = ["json"]
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
# CELERY_TASK_SERIALIZER = "json"
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
# CELERY_RESULT_SERIALIZER = "json"
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_TIME_LIMIT = 5 * 60
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_SOFT_TIME_LIMIT = 60
# # http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# # django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
# login attempts security
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "autobuyfast.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "autobuyfast.users.adapters.SocialAccountAdapter"
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# Your stuff...
# ------------------------------------------------------------------------------
# Allauth Custom forms
ACCOUNT_FORMS = {
    # "add_email": "allauth.account.forms.AddEmailForm",
    # "change_password": "allauth.account.forms.ChangePasswordForm",
    # "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    # "login": "allauth.account.forms.LoginForm",
    # "reset_password": "allauth.account.forms.ResetPasswordForm",
    # "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    # "set_password": "allauth.account.forms.SetPasswordForm",
    "signup": "autobuyfast.users.forms.UserCreationForm",
    # "signup": "allauth.socialaccount.forms.SignupForm",
}

# Your stuff...
# ------------------------------------------------------------------------------
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


JET_DEFAULT_THEME = "light-blue"
JET_SIDE_MENU_COMPACT = True
JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = str(ROOT_DIR / "client_secrets.json")


HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ("/admin/*", "/jet/*", "/jet/dashboard/*")
KEEP_COMMENTS_ON_MINIFYING = True

TINYMCE_JS_URL = "https://bizwallet-bucket.s3.amazonaws.com/static/tinymce/tinymce.min.js" #str(APPS_DIR / "/static/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = "https://bizwallet-bucket.s3.amazonaws.com/static/tinymce" #str(APPS_DIR / "/static/tinymce")
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "width": "100%",
    'relative_urls': False,
    "height": 500,
    "menubar": False,
    "statusbar": True,
    "selector": "textarea",
    "content_css": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
    "plugins": "a11ychecker,advcode,advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullpage,fullscreen,insertdatetime,media,table,tabfocus,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | code"
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
    "menubar":"tools",
    "custom_undo_redo_levels": 10,
    "fullpage_default_doctype": '<!DOCTYPE html>',
    "fullpage_default_encoding": 'UTF-8'
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

# Whether to append trailing slashes to URLs.
APPEND_SLASH = True


PROFILE_APP_NAME = 'users'
PROFILE_MODEL_NAME = 'Profile' # letter case insensitive
COMMENT_FLAGS_ALLOWED = 3
COMMENT_SHOW_FLAGGED=True
COMMENT_FLAG_REASONS = [
    (1, 'Spam | Exists only to promote a service'),
    (2, 'Abusive | Intended at promoting hatred'),
    (3, 'Racist | Sick mentality'),
    (4, 'Whatever | Your reason'),
]
COMMENT_ALLOW_ANONYMOUS = True
COMMENT_ALLOW_MODERATOR_TO_BLOCK = True
COMMENT_ALLOW_BLOCKING_USERS = True
