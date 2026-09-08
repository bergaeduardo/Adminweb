# -*- encoding: utf-8 -*-
"""Capa de acceso a SQL Server para las transferencias entre depósitos.

A diferencia de `herramientas.sql_muestras_articulos`, acá el lote está scopeado
por un UUID que genera Django, así que no hay TRUNCATE global y dos usuarios
pueden trabajar en paralelo sin pisarse.

El SP `EB_TransferDeposito_Procesar` devuelve SIEMPRE dos resultsets:
  1) las filas con problema (vacío si el lote está limpio)
  2) una única fila de resumen
Una excepción de Python significa falla técnica, nunca dato malo del usuario.
"""

import logging
import uuid

from django.conf import settings
from django.db import connections

logger = logging.getLogger(__name__)


def _usar_base_laker_sa():
    """Otras vistas del proyecto repuntan el alias `mi_db_2` a TASKY_SA mutando
    settings a nivel proceso, así que hay que fijarlo antes de cada cursor.
    Mismo guard que usa la herramienta de muestras."""
    settings.DATABASES['mi_db_2']['NAME'] = 'LAKER_SA'


def _filas_como_dicts(cursor):
    columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


def nuevo_lote_id():
    return uuid.uuid4()


def crear_lote(lote_id, usuario, host, filas):
    """Inserta la cabecera del lote y su detalle.

    `filas` es una lista de tuplas ya validadas en forma:
    (dep_origen, ubic_origen, dep_destino, ubic_destino, articulo, cantidad).
    La `Fila` (número que ve el usuario) la asigna Django, empezando en 1.
    """
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO EB_TransferDepositoLote (IdLote, Usuario, Host, Estado, Filas)
            VALUES (%s, %s, %s, 0, %s)
            ''',
            [str(lote_id), usuario, host, len(filas)],
        )
        cursor.executemany(
            '''
            INSERT INTO EB_TransferDepositoDet
                (IdLote, Fila, DepOrigen, UbicOrigen, DepDestino, UbicDestino, Articulo, Cantidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            [
                (str(lote_id), indice, dep_o, ubic_o, dep_d, ubic_d, articulo, cantidad)
                for indice, (dep_o, ubic_o, dep_d, ubic_d, articulo, cantidad) in enumerate(filas, start=1)
            ],
        )


def procesar_lote(lote_id, usuario, host, solo_validar):
    """Ejecuta el SP y devuelve (filas_con_error, resumen).

    `filas_con_error` es una lista de dicts con la fila y su mensaje.
    `resumen` es un dict con Ok / FilasProcesadas / FilasConError / IdTarea /
    NroComprobante / ComprobInterno / Mensaje.
    """
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            'EXEC EB_TransferDeposito_Procesar %s, %s, %s, %s',
            [str(lote_id), usuario, host, 1 if solo_validar else 0],
        )

        filas_con_error = _filas_como_dicts(cursor)

        resumen = {}
        if cursor.nextset():
            resumenes = _filas_como_dicts(cursor)
            if resumenes:
                resumen = resumenes[0]

    return filas_con_error, resumen


def borrar_lote(lote_id):
    """Borra un lote y su detalle (la FK tiene ON DELETE CASCADE).

    Se usa para no dejar basura cuando la validación de forma en Python ya
    falló despues de haber creado el lote.
    """
    _usar_base_laker_sa()
    try:
        with connections['mi_db_2'].cursor() as cursor:
            cursor.execute('DELETE FROM EB_TransferDepositoLote WHERE IdLote = %s', [str(lote_id)])
    except Exception:
        # No es crítico: el lote queda huérfano y lo limpia la purga por antigüedad.
        logger.exception('No se pudo borrar el lote de transferencias %s', lote_id)
