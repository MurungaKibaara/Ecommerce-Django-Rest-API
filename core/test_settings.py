from .settings import *             # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':eretail:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
