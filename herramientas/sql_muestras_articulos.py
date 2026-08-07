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


PATRON_STOCK_INSUFICIENTE = 'La Cantidad en stock no es suficiente'


def _obtener_filas_con_error():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            '''
            SELECT CodigoUbicacion, CodigoArticulo, CantidadAjuste, Resultado
            FROM temAjusteRecodificacion
            WHERE Resultado IS NOT NULL
            '''
        )
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


def _obtener_filas_pendientes():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('SELECT CodigoUbicacion, CodigoArticulo, CantidadAjuste FROM temAjusteRecodificacion')
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


def _eliminar_filas_stock_insuficiente():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            "DELETE FROM temAjusteRecodificacion WHERE Resultado LIKE %s",
            [f'%{PATRON_STOCK_INSUFICIENTE}%'],
        )


def _ejecutar_sp_una_vez():
    """Ejecuta el SP una vez. Si el SP aborta el lote por errores de validación, devuelve
    esos errores en vez de dejar propagar la excepción cruda."""
    try:
        with connections['mi_db_2'].cursor() as cursor:
            cursor.execute('EXEC [EB_RecodificacionV1.2]')
    except Exception:
        filas_con_error = _obtener_filas_con_error()
        if not filas_con_error:
            raise
        return False, [], filas_con_error

    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('SELECT * FROM EB_ProcResults')
        columnas_proc = [col[0] for col in cursor.description]
        mensajes_proceso = [dict(zip(columnas_proc, fila)) for fila in cursor.fetchall()]

    return True, mensajes_proceso, []


def ejecutar_recodificacion():
    """Ejecuta el SP de recodificación.

    Si alguna fila falla por ubicación o artículo inválido, el lote completo se aborta
    (esos errores requieren corregir los datos e importar de nuevo). Si el único problema
    son filas con stock insuficiente, esas filas se omiten automáticamente y se reintenta
    con el resto, ya que si no hay stock no hace falta dar de baja ese artículo.
    """
    _usar_base_laker_sa()

    exito, mensajes_proceso, filas_error = _ejecutar_sp_una_vez()

    if exito:
        return {
            'ejecutado': True,
            'mensajes_proceso': mensajes_proceso,
            'resultado_filas': [],
            'filas_procesadas': _obtener_filas_pendientes(),
            'filas_omitidas': [],
        }

    errores_bloqueantes = [f for f in filas_error if PATRON_STOCK_INSUFICIENTE not in (f['Resultado'] or '')]
    filas_stock_insuficiente = [f for f in filas_error if PATRON_STOCK_INSUFICIENTE in (f['Resultado'] or '')]

    if errores_bloqueantes:
        return {
            'ejecutado': False,
            'mensajes_proceso': [],
            'resultado_filas': filas_error,
            'filas_procesadas': [],
            'filas_omitidas': [],
        }

    # Los únicos errores son de stock insuficiente: se omiten esas filas y se reintenta con el resto.
    _eliminar_filas_stock_insuficiente()

    if not _obtener_filas_pendientes():
        return {
            'ejecutado': False,
            'mensajes_proceso': [],
            'resultado_filas': [],
            'filas_procesadas': [],
            'filas_omitidas': filas_stock_insuficiente,
        }

    exito2, mensajes_proceso2, filas_error2 = _ejecutar_sp_una_vez()

    if not exito2:
        # No debería pasar (ya se validó), pero por seguridad no se oculta el error.
        return {
            'ejecutado': False,
            'mensajes_proceso': [],
            'resultado_filas': filas_error2,
            'filas_procesadas': [],
            'filas_omitidas': [],
        }

    return {
        'ejecutado': True,
        'mensajes_proceso': mensajes_proceso2,
        'resultado_filas': [],
        'filas_procesadas': _obtener_filas_pendientes(),
        'filas_omitidas': filas_stock_insuficiente,
    }
