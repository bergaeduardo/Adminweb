from core.settings import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]
ALLOWED_HOSTS = ['192.168.1.127', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'BD_Pruebas',
#         'USER': 'openpg',
#         'PASSWORD': 'openpgpwd',
#         'HOST': '127.0.0.1',
#         'DATABASE_PORT': '5232',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'DATABASE_PORT': '5432',
    },
    'mi_db_2':{
            'ENGINE': 'mssql',
            'NAME': 'LAKER_SA',
            'USER': 'sa',
            'PASSWORD': 'Axoft1988',
            'HOST': 'SERVIDOR',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 13 for SQL Server',
            },
            
    },
}

DATABASE_ROUTERS = ['consultasTango.routers.MiApp2Router']