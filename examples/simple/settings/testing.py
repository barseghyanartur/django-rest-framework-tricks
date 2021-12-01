from .base import *  # NOQA

DEV = False
DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TOOLBAR_PANELS = {}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_DIR(os.path.join("..", "..", "db", "example.db")),
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
    "formatters": {
        "verbose": {
            "format": "\n%(levelname)s %(asctime)s [%(pathname)s:%(lineno)s] "
            "%(message)s"
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
