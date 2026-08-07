from django.conf import settings
from django.db import connections


def _usar_base_laker_sa():
    settings.DATABASES['mi_db_2']['NAME'] = 'LAKER_SA'


def truncar_tablas_ajuste():
    """Limpia las tablas temporales usadas por el SP de recodificación antes de una nueva carga."""
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('TRUNCATE TABLE temAjusteRecodificacion')
        cursor.execute('TRUNCATE TABLE EB_ProcResults')


def insertar_filas_ajuste(filas):
    """Inserta filas (CodigoUbicacion, CodigoArticulo, CantidadAjuste) en temAjusteRecodificacion."""
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        for codigo_ubicacion, codigo_articulo, cantidad_ajuste in filas:
            cursor.execute(
                '''
                INSERT INTO temAjusteRecodificacion (CodigoUbicacion, CodigoArticulo, CantidadAjuste)
                VALUES (%s, %s, %s)
                ''',
                [codigo_ubicacion, codigo_articulo, cantidad_ajuste],
            )


def ejecutar_recodificacion():
    """Ejecuta el SP de recodificación y devuelve el resultado por fila y los mensajes del proceso."""
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('EXEC [EB_RecodificacionV1.2]')

        cursor.execute('SELECT * FROM EB_ProcResults')
        columnas_proc = [col[0] for col in cursor.description]
        mensajes_proceso = [dict(zip(columnas_proc, fila)) for fila in cursor.fetchall()]

        cursor.execute(
            '''
            SELECT CodigoUbicacion, CodigoArticulo, CantidadAjuste, Resultado
            FROM temAjusteRecodificacion
            WHERE Resultado IS NOT NULL
            '''
        )
        columnas_filas = [col[0] for col in cursor.description]
        resultado_filas = [dict(zip(columnas_filas, fila)) for fila in cursor.fetchall()]

    return {
        'mensajes_proceso': mensajes_proceso,
        'resultado_filas': resultado_filas,
    }
