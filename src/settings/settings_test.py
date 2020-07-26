from settings.settings import *

SECRET_KEY = '7zbn5g%8%4)72%b6i(=$2gj9n3=hk7r%y36@i^8#$59e=a$e(i'

DEBUG = False

ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = CELERY_TASK_ALWAYS_EAGER = True  # run celery tasks as functions

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-test.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.outbox'
