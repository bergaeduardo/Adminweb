# -*- encoding: utf-8 -*-
"""Constantes de la herramienta de transferencias entre depósitos.

Los nombres son los de STA22.NOMBRE_SUC en LAKER_SA. La lista está acotada a
propósito: son los depósitos de proceso entre los que se mueve mercadería.
"""

DEPOSITOS_HABILITADOS = {
    '04': 'OUTLET',
    '06': 'FALLAS',
    '10': 'RECODIFICACIONES',
    '20': 'ARREGLOS PRODUCCION',
}

# Orden de las columnas del Excel / del texto pegado.
#
# El artículo puede CAMBIAR entre origen y destino: la operación es una
# recodificación con movimiento (baja de un código en el origen, alta de otro
# en el destino). Las dos cantidades se piden por separado como doble control
# de tipeo, pero la validación exige que coincidan.
COLUMNAS = [
    'DepOrigen', 'UbicOrigen', 'ArtOrigen', 'CantBaja',
    'DepDestino', 'UbicDestino', 'ArtDestino', 'CantAlta',
]
CANTIDAD_COLUMNAS = len(COLUMNAS)

# Etiquetas para los mensajes de error, en el mismo orden.
ETIQUETAS_COLUMNAS = [
    'Dep. origen', 'Ubic. origen', 'Art. origen', 'Cant. baja',
    'Dep. destino', 'Ubic. destino', 'Art. destino', 'Cant. alta',
]

GRUPOS_HABILITADOS = ['admin', 'abastecimiento_sup']


def normalizar_deposito(valor):
    """Excel entrega `4` donde el usuario escribió `04`. Devuelve el código de 2
    dígitos, o None si no puede representarse como tal."""
    texto = str(valor).strip()
    if not texto:
        return None
    # Excel puede entregar '4' o incluso '4.0' si la celda quedó numérica.
    if texto.endswith('.0'):
        texto = texto[:-2]
    if not texto.isdigit() or len(texto) > 2:
        return None
    return texto.zfill(2)
