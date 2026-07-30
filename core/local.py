from core.settings import *
from decouple import config

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
        'PASSWORD': config('DB_DEFAULT_PASSWORD'),
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5232',
    },
    # Base de Tango
    'mi_db_2':{
            'ENGINE': 'mssql',
            'NAME': 'LAKER_SA',
            'USER': 'sa',
            'PASSWORD': config('DB_TANGO_PASSWORD'),
            'HOST': 'XL-TANGO',
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
            'PASSWORD': config('DB_WMS_PASSWORD'),
            # ----Produccion----
            'HOST': 'XL-SALES\SQLEXPRESS',

            # ----Testing----
            # 'HOST': '192.168.0.227',

            # 'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
            
    },
    # Base LOCALES_LAKERS
    'mi_db_4':{
            'ENGINE': 'mssql',
            'NAME': 'LOCALES_LAKERS',
            'USER': 'sa',
            'PASSWORD': config('DB_LOCALES_PASSWORD'),
            'HOST': 'XL-LAKERBIS',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
            
    },
    # Base sistemas (XL-SALES) - tabla PuntosDeVenta
    'mi_db_5':{
            'ENGINE': 'mssql',
            'NAME': 'sistemas',
            'USER': 'sa',
            'PASSWORD': config('DB_SISTEMAS_PASSWORD'),
            'HOST': 'XL-APPS',
            'PORT': '1433',

            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },

    },
    'db_proveedores': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_PROVEEDORES_NAME', default='proveedores_xl'),
        'USER': config('DB_PROVEEDORES_USER', default='postgres'),
        'PASSWORD': config('DB_PROVEEDORES_PASSWORD', default=config('DB_DEFAULT_PASSWORD', default='')),
        'HOST': config('DB_PROVEEDORES_HOST', default='192.168.0.9'),
        'PORT': config('DB_PROVEEDORES_PORT', default='5432'),
    },
}

DATABASE_ROUTERS = ['consultasTango.routers.MiApp2Router','consultasLakersBis.routers.MiApp4Router','consultasWMS.routers.MiApp3Router']