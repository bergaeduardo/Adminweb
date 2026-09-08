# -*- encoding: utf-8 -*-
import datetime
import json
import logging
from decimal import Decimal

from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render

from herramientas.sql_muestras_articulos import parsear_xlsx_ajuste

from .constantes import (
    CANTIDAD_COLUMNAS,
    DEPOSITOS_HABILITADOS,
    GRUPOS_HABILITADOS,
    normalizar_deposito,
)
from .models import RegistroTransferenciaDeposito
from . import sql_transferencias

logger = logging.getLogger(__name__)

HOST_TANGO = 'TRANSFER-DEP'


def usuario_puede_transferir(user):
    """Verifica si el usuario pertenece a un grupo habilitado para transferir
    stock entre depósitos."""
    return user.groups.annotate(name_lower=Lower('name')).filter(
        name_lower__in=GRUPOS_HABILITADOS
    ).exists() or user.is_superuser


def _validar_forma(filas_crudas):
    """Valida forma y normaliza, sin tocar la base. Devuelve (filas, errores).

    Se acumulan TODOS los errores en vez de cortar en el primero, para que el
    usuario corrija el Excel de una sola pasada.
    """
    filas = []
    errores = []

    for indice, fila in enumerate(filas_crudas, start=1):
        if len(fila) != CANTIDAD_COLUMNAS:
            errores.append(
                f'Fila {indice}: se esperaban {CANTIDAD_COLUMNAS} columnas '
                f'(Dep. origen, Ubic. origen, Dep. destino, Ubic. destino, Artículo, Cantidad), '
                f'se recibieron {len(fila)}.'
            )
            continue

        dep_o_crudo, ubic_o, dep_d_crudo, ubic_d, articulo, cantidad_cruda = [str(v).strip() for v in fila]

        problemas = []

        dep_o = normalizar_deposito(dep_o_crudo)
        dep_d = normalizar_deposito(dep_d_crudo)

        if dep_o is None or dep_o not in DEPOSITOS_HABILITADOS:
            problemas.append(
                f'el depósito de origen "{dep_o_crudo}" no está habilitado '
                f'({", ".join(sorted(DEPOSITOS_HABILITADOS))})'
            )
        if dep_d is None or dep_d not in DEPOSITOS_HABILITADOS:
            problemas.append(
                f'el depósito de destino "{dep_d_crudo}" no está habilitado '
                f'({", ".join(sorted(DEPOSITOS_HABILITADOS))})'
            )

        if not ubic_o:
            problemas.append('la ubicación de origen es obligatoria')
        if not ubic_d:
            problemas.append('la ubicación de destino es obligatoria')
        if not articulo:
            problemas.append('el artículo es obligatorio')

        if dep_o and dep_d and ubic_o and ubic_d and dep_o == dep_d and ubic_o.upper() == ubic_d.upper():
            problemas.append('el origen y el destino son la misma ubicación')

        cantidad = None
        try:
            # Excel puede entregar '2.0' en una celda numérica.
            cantidad = int(float(cantidad_cruda))
            if float(cantidad_cruda) != cantidad:
                problemas.append(f'la cantidad "{cantidad_cruda}" debe ser un número entero')
                cantidad = None
            elif cantidad <= 0:
                problemas.append('la cantidad debe ser mayor a cero')
                cantidad = None
        except (ValueError, TypeError):
            problemas.append(f'la cantidad "{cantidad_cruda}" no es un número')

        if problemas:
            errores.append(f'Fila {indice}: ' + '; '.join(problemas) + '.')
            continue

        filas.append((dep_o, ubic_o.upper(), dep_d, ubic_d.upper(), articulo.upper(), cantidad))

    return filas, errores


def _json_seguro(valor):
    """Convierte a algo serializable por JSONField.

    Las cantidades vuelven de SQL Server como Decimal y las fechas como
    datetime, y ninguno de los dos entra en un JSONField. Sin esto el registro
    de auditoría falla en silencio (el try/except de _auditar lo tapa, que es
    justo lo que no queremos que pase inadvertido).
    """
    if isinstance(valor, Decimal):
        entero = int(valor)
        return entero if valor == entero else float(valor)
    if isinstance(valor, (datetime.datetime, datetime.date)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {k: _json_seguro(v) for k, v in valor.items()}
    if isinstance(valor, (list, tuple)):
        return [_json_seguro(v) for v in valor]
    return valor


def _auditar(usuario, accion, lote_id, filas, filas_con_error=None, resumen=None):
    """El stock ya se movió cuando esto corre; si falla la auditoría no debe
    parecer que la operación falló (evitaría que el usuario reintente y duplique
    el movimiento)."""
    resumen = resumen or {}
    try:
        RegistroTransferenciaDeposito.objects.create(
            usuario=usuario,
            accion=accion,
            lote_id=lote_id,
            filas=_json_seguro(filas),
            filas_con_error=_json_seguro(filas_con_error) or None,
            numero_tarea=(str(resumen.get('IdTarea')) if resumen.get('IdTarea') is not None else None),
            nro_comprobante=resumen.get('NroComprobante'),
        )
    except Exception:
        logger.exception('No se pudo guardar el registro de auditoría de transferencias (%s)', accion)


@user_passes_test(usuario_puede_transferir, login_url="/login/")
def transferencias_depositos(request):
    return render(request, 'transferencias/index.html', {
        'depositos': sorted(DEPOSITOS_HABILITADOS.items()),
        'cantidad_columnas': CANTIDAD_COLUMNAS,
    })


@user_passes_test(usuario_puede_transferir, login_url="/login/")
def transferencias_depositos_subir_archivo(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    archivo = request.FILES.get('archivo')
    if not archivo:
        return JsonResponse({'errores': ['No se recibió ningún archivo.']}, status=400)

    if not archivo.name.lower().endswith('.xlsx'):
        return JsonResponse({'errores': ['El archivo debe tener formato .xlsx.']}, status=400)

    try:
        filas = parsear_xlsx_ajuste(archivo)
    except Exception as e:
        return JsonResponse({'errores': [f'No se pudo leer el archivo: {str(e)}']}, status=400)

    return JsonResponse({'filas': filas})


def _procesar(request, solo_validar):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        payload = json.loads(request.body)
        filas_crudas = payload.get('filas', [])
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    filas, errores = _validar_forma(filas_crudas)

    if errores:
        return JsonResponse({'errores': errores}, status=400)

    if not filas:
        return JsonResponse({'errores': ['No se recibieron filas para procesar.']}, status=400)

    lote_id = sql_transferencias.nuevo_lote_id()

    try:
        sql_transferencias.crear_lote(lote_id, request.user.username, HOST_TANGO, filas)
    except Exception as e:
        logger.exception('Error al crear el lote de transferencias')
        return JsonResponse({'errores': [f'Error al cargar los datos: {str(e)}']}, status=500)

    try:
        filas_con_error, resumen = sql_transferencias.procesar_lote(
            lote_id, request.user.username, HOST_TANGO, solo_validar
        )
    except Exception as e:
        logger.exception('Error técnico al procesar el lote de transferencias %s', lote_id)
        sql_transferencias.borrar_lote(lote_id)
        return JsonResponse({'errores': [f'Error al procesar la transferencia: {str(e)}']}, status=500)

    accion = (
        RegistroTransferenciaDeposito.ACCION_VALIDAR if solo_validar
        else RegistroTransferenciaDeposito.ACCION_EJECUTAR
    )
    _auditar(request.user, accion, lote_id, filas, filas_con_error, resumen)

    return JsonResponse({
        'lote_id': str(lote_id),
        'ok': bool(resumen.get('Ok')),
        'filas_con_error': filas_con_error,
        'filas_procesadas': resumen.get('FilasProcesadas'),
        'cantidad_errores': resumen.get('FilasConError'),
        'numero_tarea': resumen.get('IdTarea'),
        'nro_comprobante': resumen.get('NroComprobante'),
        'mensaje': resumen.get('Mensaje'),
    })


@user_passes_test(usuario_puede_transferir, login_url="/login/")
def transferencias_depositos_validar(request):
    return _procesar(request, solo_validar=True)


@user_passes_test(usuario_puede_transferir, login_url="/login/")
def transferencias_depositos_ejecutar(request):
    return _procesar(request, solo_validar=False)
