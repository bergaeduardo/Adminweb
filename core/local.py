from core.settings import *
# from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

DATABASES = {
    # Base de administracio de roles
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'extra,123',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5232',
    },
    # Base de Tango
    'mi_db_2':{
            'ENGINE': 'mssql',
            'NAME': 'LAKER_SA',
            'USER': 'sa',
            'PASSWORD': 'Axoft1988',
            'HOST': 'SERVIDOR',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
            
    },
    # Base Sistema de Ubicacione
    'mi_db_3':{
            'ENGINE': 'mssql',
            'NAME': 'UbicacionesStockMvc',
            'USER': 'sa',
            'PASSWORD': 'Axoft1988',
            # ----Produccion----
            'HOST': '192.168.0.226\SQL2016',

            # ----Testing----
            # 'HOST': '192.168.0.227',

            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
            
    },
    # Base LOCALES_LAKERS
    'mi_db_4':{
            'ENGINE': 'mssql',
            'NAME': 'LOCALES_LAKERS',
            'USER': 'sa',
            'PASSWORD': 'Axoft',
            'HOST': 'LAKERBIS',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
            
    },
}

DATABASE_ROUTERS = ['consultasTango.routers.MiApp2Router','consultasLakersBis.routers.MiApp4Router','consultasWMS.routers.MiApp3Router']