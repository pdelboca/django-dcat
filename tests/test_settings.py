import os

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'dcat',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DB_NAME', 'db.sqlite3'),
    }
}
