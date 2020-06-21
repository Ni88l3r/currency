SECRET_KEY = 'y4w0e^)3!j7e9+n*v@htp(2of&f2075x(+vn%az$q-_y$vig*0'

DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'koekuachu@ukr.net'
EMAIL_HOST_PASSWORD = 'bLPw2kqp8DsIr8Ir'
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
