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

`buscar_articulo` y `ubicaciones_habilitadas` son lecturas sueltas para el modo
escaneo, y las `historial_*` para la pantalla de historial: no pasan por el SP y
consultan directo cada base (sin linked server ni SQL dinámico).

OJO con las tablas EB_TransferDeposito*: los lotes con Estado = 2 (aplicados)
son EL HISTORIAL de la herramienta, no staging descartable. Ver el comentario de
013_EB_TransferDeposito_LimpiarLotes.sql.
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


# ============================================================================
# HISTORIAL
#
# Lee los lotes APLICADOS (Estado = 2), que son el registro de lo que
# efectivamente movió stock. Los validados-sin-ejecutar y los rechazados quedan
# afuera a propósito: nunca movieron nada, así que no sirven para contar
# cantidades.
#
# Los totales se calculan EN SQL sobre todo el conjunto filtrado, no sobre la
# página. (En el proyecto hay un total hecho en JS recorriendo el DOM
# —Mov_WMS.html— que justamente por eso suma solo la página visible.)
# ============================================================================

_ESTADO_APLICADO = 2

# El artículo de destino NORMALIZADO, con fallback al crudo.
#
# Por qué el COALESCE: los lotes de la v1 (cuando el código no podía cambiar)
# tienen ArtDestinoN en NULL. El ALTER de la v2 rellenó las columnas de ENTRADA
# (ArtDestino, CantAlta) pero no la normalizada, que solo la setea el SP de
# validación — y esos lotes nunca se revalidaron.
# Sin el COALESCE esas filas pierden su ALTA en los totales por artículo, se
# escapan del filtro por artículo, y todo eso EN SILENCIO. Son 5 de las 15
# filas aplicadas hoy.
_ART_DESTINO = "COALESCE(d.ArtDestinoN, UPPER(LTRIM(RTRIM(d.ArtDestino))))"


def _where_historial(filtros):
    """Arma el WHERE común a las tres consultas. Devuelve (sql, parametros).

    Todo parametrizado: los filtros vienen del usuario y no se interpolan.

    Los filtros de depósito y artículo matchean CUALQUIERA de las dos puntas:
    un movimiento toca dos depósitos, y con recodificación dos artículos, así
    que filtrar por "06" trae lo que salió del 06 y lo que entró al 06.
    """
    # EsPrueba = 0 deja afuera los lotes ejecutados durante el desarrollo de la
    # herramienta. Fueron transferencias reales contra producción, pero todas
    # devueltas con un movimiento inverso (efecto neto CERO), así que ensucian
    # el historial y sus totales sin aportar nada. Ver 004_marcar_pruebas.sql.
    condiciones = ['l.Estado = %s', 'l.EsPrueba = 0']
    params = [_ESTADO_APLICADO]

    filtros = filtros or {}

    if filtros.get('desde'):
        condiciones.append('l.FechaProceso >= %s')
        params.append(filtros['desde'])
    if filtros.get('hasta'):
        # < día siguiente, en vez de CAST(FechaProceso AS DATE) <= hasta, para
        # que el índice por FechaProceso siga siendo usable.
        condiciones.append('l.FechaProceso < DATEADD(DAY, 1, %s)')
        params.append(filtros['hasta'])
    if filtros.get('deposito'):
        condiciones.append('(d.DepOrigenN = %s OR d.DepDestinoN = %s)')
        params.extend([filtros['deposito'], filtros['deposito']])
    if filtros.get('articulo'):
        condiciones.append('(d.ArticuloN LIKE %s OR ' + _ART_DESTINO + ' LIKE %s)')
        patron = '%' + filtros['articulo'].strip().upper() + '%'
        params.extend([patron, patron])
    if filtros.get('usuario'):
        condiciones.append('l.Usuario LIKE %s')
        params.append('%' + filtros['usuario'].strip() + '%')

    return ' AND '.join(condiciones), params


def historial_totales_por_deposito(filtros=None):
    """Salidas, entradas, neto y movimientos por depósito.

    Es el número que se pidió: cuánto pasó por la herramienta. Cada movimiento
    SACA del depósito de origen y PONE en el de destino, así que aporta a dos.
    """
    where, params = _where_historial(filtros)
    consulta = (
        'SELECT x.Deposito,'
        '       SUM(CASE WHEN x.Signo = -1 THEN x.Cant ELSE 0 END) AS Salidas,'
        '       SUM(CASE WHEN x.Signo =  1 THEN x.Cant ELSE 0 END) AS Entradas,'
        '       COUNT(*) AS Movimientos '
        'FROM ('
        '  SELECT d.DepOrigenN AS Deposito, -1 AS Signo, d.Cantidad AS Cant'
        '  FROM EB_TransferDepositoDet d'
        '  JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote'
        '  WHERE ' + where + ' AND d.DepOrigenN IS NOT NULL'
        '  UNION ALL'
        '  SELECT d.DepDestinoN, 1, d.CantAlta'
        '  FROM EB_TransferDepositoDet d'
        '  JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote'
        '  WHERE ' + where + ' AND d.DepDestinoN IS NOT NULL'
        ') x GROUP BY x.Deposito ORDER BY x.Deposito'
    )

    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(consulta, params + params)
        return [
            {
                'deposito': (r[0] or '').strip(),
                'nombre': DEPOSITOS_HABILITADOS.get((r[0] or '').strip(), ''),
                'salidas': int(r[1] or 0),
                'entradas': int(r[2] or 0),
                'neto': int(r[2] or 0) - int(r[1] or 0),
                'movimientos': int(r[3] or 0),
            }
            for r in cursor.fetchall()
        ]


def historial_totales_por_articulo(filtros=None, limite=100):
    """Bajas y altas por artículo, ordenado por volumen.

    Con recodificación el código de cada punta es distinto, así que un artículo
    puede aparecer con solo bajas (el código viejo) y otro con solo altas.
    """
    where, params = _where_historial(filtros)
    consulta = (
        'SELECT TOP (' + str(int(limite)) + ') x.Articulo,'
        '       SUM(CASE WHEN x.Signo = -1 THEN x.Cant ELSE 0 END) AS Bajas,'
        '       SUM(CASE WHEN x.Signo =  1 THEN x.Cant ELSE 0 END) AS Altas '
        'FROM ('
        '  SELECT d.ArticuloN AS Articulo, -1 AS Signo, d.Cantidad AS Cant'
        '  FROM EB_TransferDepositoDet d'
        '  JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote'
        '  WHERE ' + where + ' AND d.ArticuloN IS NOT NULL'
        '  UNION ALL'
        '  SELECT ' + _ART_DESTINO + ', 1, d.CantAlta'
        '  FROM EB_TransferDepositoDet d'
        '  JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote'
        '  WHERE ' + where + ' AND ' + _ART_DESTINO + ' IS NOT NULL'
        ') x GROUP BY x.Articulo ORDER BY SUM(x.Cant) DESC, x.Articulo'
    )

    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(consulta, params + params)
        return [
            {
                'articulo': (r[0] or '').strip(),
                'bajas': int(r[1] or 0),
                'altas': int(r[2] or 0),
            }
            for r in cursor.fetchall()
        ]


_SELECT_MOVIMIENTOS = (
    'SELECT l.FechaProceso, l.Usuario, l.NroComprobante, l.IdTarea,'
    '       d.DepOrigenN, d.UbicOrigen, d.Articulo, d.Cantidad,'
    '       d.DepDestinoN, d.UbicDestino, d.ArtDestino, d.CantAlta,'
    '       CASE WHEN d.ArticuloN <> ' + _ART_DESTINO + ' THEN 1 ELSE 0 END AS EsRecodificacion '
    'FROM EB_TransferDepositoDet d '
    'JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote '
    'WHERE '
)


def _fila_movimiento(r):
    return {
        'fecha': r[0],
        'usuario': (r[1] or '').strip(),
        # SIN strip: Tango guarda n_comp con un espacio inicial (' 02005...'),
        # así que recortarlo rompe la correspondencia exacta con sta14. En HTML
        # el espacio inicial no se ve, así que no molesta al mostrarlo.
        'comprobante': r[2] or '',
        'tarea': r[3],
        'dep_origen': (r[4] or '').strip(),
        'ubic_origen': (r[5] or '').strip(),
        'art_origen': (r[6] or '').strip(),
        'cant_baja': int(r[7] or 0),
        'dep_destino': (r[8] or '').strip(),
        'ubic_destino': (r[9] or '').strip(),
        'art_destino': (r[10] or '').strip(),
        'cant_alta': int(r[11] or 0),
        'es_recodificacion': bool(r[12]),
    }


def historial_movimientos(filtros=None, pagina=1, tamano=50):
    """El detalle, paginado en SQL. Devuelve (filas, total).

    Se pagina con OFFSET/FETCH y se cuenta aparte, para no traer todo a Python
    cuando la tabla crezca.
    """
    where, params = _where_historial(filtros)
    pagina = max(1, int(pagina))
    tamano = max(1, int(tamano))
    offset = (pagina - 1) * tamano

    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            'SELECT COUNT(*) FROM EB_TransferDepositoDet d '
            'JOIN EB_TransferDepositoLote l ON l.IdLote = d.IdLote WHERE ' + where,
            params,
        )
        total = cursor.fetchone()[0]

        cursor.execute(
            _SELECT_MOVIMIENTOS + where
            + ' ORDER BY l.FechaProceso DESC, d.Fila'
              ' OFFSET %s ROWS FETCH NEXT %s ROWS ONLY',
            params + [offset, tamano],
        )
        filas = [_fila_movimiento(r) for r in cursor.fetchall()]

    return filas, total


def historial_movimientos_todos(filtros=None, tope=20000):
    """Igual que historial_movimientos pero sin paginar, para la exportación.

    El tope evita que un rango de fechas enorme genere una descarga
    inmanejable; la vista avisa si se truncó.
    """
    where, params = _where_historial(filtros)
    _usar_base_laker_sa()
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute(
            _SELECT_MOVIMIENTOS.replace('SELECT ', 'SELECT TOP (' + str(int(tope)) + ') ', 1)
            + where + ' ORDER BY l.FechaProceso DESC, d.Fila',
            params,
        )
        return [_fila_movimiento(r) for r in cursor.fetchall()]
