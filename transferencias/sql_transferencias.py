# -*- encoding: utf-8 -*-
"""Capa de acceso a SQL Server para las transferencias entre depósitos.

A diferencia de `herramientas.sql_muestras_articulos`, acá el lote está scopeado
por un UUID que genera Django, así que no hay TRUNCATE global y dos usuarios
pueden trabajar en paralelo sin pisarse.

El SP `EB_TransferDeposito_Procesar` devuelve SIEMPRE tres resultsets:
  1) las filas con problema (vacío si el lote está limpio)
  2) una única fila de resumen
  3) sugerencias de dónde sí está el artículo
Una excepción de Python significa falla técnica, nunca dato malo del usuario.

`buscar_articulo` y `ubicaciones_habilitadas` son las dos únicas funciones que
NO pasan por el SP: son lecturas sueltas para el modo escaneo, y consultan
directo cada base (sin linked server ni SQL dinámico).
"""

import logging
import uuid

from django.conf import settings
from django.db import connections

from .constantes import DEPOSITOS_HABILITADOS

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


def ubicaciones_habilitadas():
    """Todas las ubicaciones de los depósitos habilitados, para poblar los
    desplegables del modo escaneo sin un round trip por cada elección.

    Son 52 en total (~2 KB), así que se embeben enteras en la página. Eso
    además elimina el tipeo de ubicaciones, que es la causa de rechazo más
    común del modo manual.
    """
    codigos = sorted(DEPOSITOS_HABILITADOS)
    marcadores = ','.join(['%s'] * len(codigos))
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute(
            f'''
            SELECT Num_Deposito, Cod_Ubicacion, Nombre_Ubicacion, Tipo_Ubicacion
            FROM Ubicacion
            WHERE Num_Deposito IN ({marcadores})
            ORDER BY Num_Deposito, Cod_Ubicacion
            ''',
            codigos,
        )
        return [
            {
                'deposito': (r[0] or '').strip(),
                'ubicacion': (r[1] or '').strip(),
                'nombre': (r[2] or '').strip(),
                'tipo': (r[3] or '').strip(),
            }
            for r in cursor.fetchall()
        ]


def buscar_articulo(codigo):
    """Resuelve un código escaneado y devuelve dónde tiene saldo.

    Devuelve un dict con `articulo`, `descripcion`, `usa_partidas`,
    `existe_en_wms` y `ubicaciones` (solo las de los depósitos habilitados y
    con saldo positivo). Si el código no existe en Tango devuelve None.

    Son dos consultas sueltas, una por base, sin linked server ni SQL dinámico.
    Medido: ~0,65 s, dominado por el cálculo de saldo sobre `Movimientos`
    (2,8M de filas).
    """
    codigo = (codigo or '').strip().upper()
    if not codigo:
        return None

    _usar_base_laker_sa()

    # 1) Validez en Tango. Misma consulta que usa el SP: excluye las carpetas
    #    ocultas con DESCRIP NOT LIKE '[_]%'. El % va DUPLICADO porque el
    #    cursor de Django interpreta el string como formato de parámetros; si
    #    no, revienta con "unsupported format character".
    #    Se prueba COD_ARTICU, y como fallback COD_BARRA y SINONIMO: los tres
    #    son únicos donde están cargados, así que no hay ambigüedad. Hoy la
    #    práctica es que la etiqueta lleve el COD_ARTICU.
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            '''
            SELECT TOP (1)
                   LTRIM(RTRIM(A.COD_ARTICU)),
                   LTRIM(RTRIM(ISNULL(A.DESCRIPCIO, ''))),
                   CAST(ISNULL(A.usa_partid, 0) AS INT)
            FROM SJ_VIEW_STA11 A
            JOIN STA11ITC B ON A.COD_ARTICU = B.CODE
            JOIN STA11FLD C ON B.IDFOLDER = C.IDFOLDER
            WHERE C.DESCRIP NOT LIKE '[_]%%'
              AND (   LTRIM(RTRIM(A.COD_ARTICU)) = %s
                   OR LTRIM(RTRIM(ISNULL(A.COD_BARRA, ''))) = %s
                   OR LTRIM(RTRIM(ISNULL(A.SINONIMO, ''))) = %s)
            ''',
            [codigo, codigo, codigo],
        )
        fila = cursor.fetchone()

    if not fila:
        return None

    articulo, descripcion, usa_partidas = fila[0], fila[1], bool(fila[2])

    # 2) Saldo por ubicación en el WMS, solo depósitos habilitados y saldo > 0.
    #    Consulta directa a mi_db_3: no hace falta el linked server porque
    #    Django tiene conexión propia a esa base.
    codigos_dep = sorted(DEPOSITOS_HABILITADOS)
    marcadores = ','.join(['%s'] * len(codigos_dep))
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute(
            f'''
            SELECT u.Num_Deposito, u.Cod_Ubicacion, u.Nombre_Ubicacion, SUM(q.s)
            FROM (
                SELECT id_Articulo, id_ubicacionDestino AS idu, Cantidad_Asosciada AS s
                FROM Movimientos WHERE id_ubicacionDestino > 0
                UNION ALL
                SELECT id_Articulo, id_ubicacionOrigen, -Cantidad_Asosciada
                FROM Movimientos WHERE id_ubicacionOrigen > 0
            ) q
            JOIN Ubicacion u ON u.id_Ubicacion = q.idu
            JOIN Articulo  a ON a.id_Articulo  = q.id_Articulo
            WHERE a.Cod_Articulo = %s
              AND u.Num_Deposito IN ({marcadores})
            GROUP BY u.Num_Deposito, u.Cod_Ubicacion, u.Nombre_Ubicacion
            HAVING SUM(q.s) > 0
            ORDER BY SUM(q.s) DESC
            ''',
            [articulo] + codigos_dep,
        )
        ubicaciones = [
            {
                'deposito': (r[0] or '').strip(),
                'ubicacion': (r[1] or '').strip(),
                'nombre': (r[2] or '').strip(),
                'saldo': int(r[3]),
            }
            for r in cursor.fetchall()
        ]

        # Si no tiene saldo, igual se distingue "no existe en el WMS" de
        # "existe pero está en cero": son dos problemas distintos para el
        # operario, y el segundo además rompería la validación por otro motivo.
        cursor.execute('SELECT TOP (1) id_Articulo FROM Articulo WHERE Cod_Articulo = %s', [articulo])
        existe_en_wms = cursor.fetchone() is not None

    return {
        'articulo': articulo,
        'descripcion': descripcion,
        'usa_partidas': usa_partidas,
        'existe_en_wms': existe_en_wms,
        'ubicaciones': ubicaciones,
    }


def crear_lote(lote_id, usuario, host, filas):
    """Inserta la cabecera del lote y su detalle.

    `filas` es una lista de tuplas ya validadas en forma:
    (dep_origen, ubic_origen, art_origen, cant_baja,
     dep_destino, ubic_destino, art_destino, cant_alta).
    La `Fila` (número que ve el usuario) la asigna Django, empezando en 1.

    Ojo con los nombres de las columnas: `Articulo` y `Cantidad` son EL LADO DE
    ORIGEN (se mantienen así de la v1 para no migrar los lotes ya aplicados) y
    el destino va en `ArtDestino` / `CantAlta`.
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
                (IdLote, Fila,
                 DepOrigen, UbicOrigen, Articulo, Cantidad,
                 DepDestino, UbicDestino, ArtDestino, CantAlta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            [
                (str(lote_id), indice, dep_o, ubic_o, art_o, cant_baja,
                 dep_d, ubic_d, art_d, cant_alta)
                for indice, (dep_o, ubic_o, art_o, cant_baja,
                             dep_d, ubic_d, art_d, cant_alta) in enumerate(filas, start=1)
            ],
        )


def procesar_lote(lote_id, usuario, host, solo_validar):
    """Ejecuta el SP y devuelve (filas_con_error, resumen, sugerencias).

    El SP devuelve SIEMPRE tres resultsets, en este orden:
      1) filas con problema (Fila + Resultado + los datos de entrada)
      2) una única fila de resumen (Ok / FilasProcesadas / FilasConError /
         IdTarea / NroComprobante / ComprobInterno / Mensaje)
      3) sugerencias de dónde sí está el artículo (vacío si no hace falta)
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

        sugerencias = []
        if cursor.nextset():
            sugerencias = _filas_como_dicts(cursor)

    return filas_con_error, resumen, sugerencias


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
