"""Genera apps/static/PlantillaTransferenciasDepositos.xlsx.

Script de mano, igual que herramientas/crear_plantilla_alta_muestras.py:

    python transferencias/crear_plantilla_transferencias.py

La hoja `Datos` va SIN encabezados a propósito: el parser lee todas las filas
como datos (reusa parsear_xlsx_ajuste, que es agnóstico a las columnas). Los
ejemplos van en gris para que se vea que hay que reemplazarlos.
"""

import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

libro = openpyxl.Workbook()
hoja_datos = libro.active
hoja_datos.title = 'Datos'

example_fill = PatternFill(start_color='E7E6E6', end_color='E7E6E6', fill_type='solid')
example_font = Font(name='Arial', size=10)
titulo_font = Font(name='Arial', size=11, bold=True)

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'),
)

# Sin encabezados: Dep. origen, Ubic. origen, Dep. destino, Ubic. destino, Artículo, Cantidad
ejemplos = [
    ['06', 'R1001A01', '20', 'A0201001', 'ARTICULO-001', 1],
    ['10', 'A0501001', '04', 'P0401001', 'ARTICULO-002', 2],
]

for fila_idx, ejemplo in enumerate(ejemplos, start=1):
    for col_idx, valor in enumerate(ejemplo, start=1):
        celda = hoja_datos.cell(row=fila_idx, column=col_idx, value=valor)
        celda.fill = example_fill
        celda.font = example_font
        celda.border = thin_border
        # Los códigos de depósito van como texto para no perder el cero inicial.
        if col_idx in (1, 3):
            celda.number_format = '@'

for columna, ancho in zip('ABCDEF', (14, 16, 14, 16, 20, 10)):
    hoja_datos.column_dimensions[columna].width = ancho

hoja_instrucciones = libro.create_sheet('Instrucciones')
instrucciones = [
    ('Transferencias entre Depósitos', 'titulo'),
    ('', None),
    ('Completá la hoja "Datos" con una fila por movimiento, SIN encabezados.', None),
    ('Las columnas van en este orden exacto:', None),
    ('', None),
    ('  A - Depósito de origen      (04, 06, 10 o 20)', None),
    ('  B - Ubicación de origen     (código de ubicación del WMS)', None),
    ('  C - Depósito de destino     (04, 06, 10 o 20)', None),
    ('  D - Ubicación de destino    (código de ubicación del WMS)', None),
    ('  E - Código de artículo', None),
    ('  F - Cantidad                (entero POSITIVO)', None),
    ('', None),
    ('Depósitos habilitados', 'titulo'),
    ('  04 - OUTLET', None),
    ('  06 - FALLAS', None),
    ('  10 - RECODIFICACIONES', None),
    ('  20 - ARREGLOS PRODUCCION', None),
    ('', None),
    ('Cosas importantes', 'titulo'),
    ('  * La cantidad SIEMPRE va positiva. El sentido lo dan las columnas', None),
    ('    de origen y destino, no el signo.', None),
    ('  * Cada ubicación tiene que pertenecer al depósito que declarás en la', None),
    ('    misma fila. Si no coincide, la fila se rechaza.', None),
    ('  * Los códigos de depósito llevan dos dígitos ("04", no "4"). La', None),
    ('    columna está formateada como texto para que Excel no coma el cero.', None),
    ('  * Si UNA fila falla la validación, NO se aplica nada del lote.', None),
    ('    Se corrigen todas las filas marcadas y se vuelve a validar.', None),
    ('  * Borrá las filas de ejemplo (en gris) antes de cargar las tuyas.', None),
]

for fila_idx, (texto, estilo) in enumerate(instrucciones, start=1):
    celda = hoja_instrucciones.cell(row=fila_idx, column=1, value=texto)
    celda.font = titulo_font if estilo == 'titulo' else Font(name='Arial', size=10)
    celda.alignment = Alignment(vertical='center')

hoja_instrucciones.column_dimensions['A'].width = 78

static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'apps', 'static')
ruta_archivo = os.path.join(static_dir, 'PlantillaTransferenciasDepositos.xlsx')
libro.save(ruta_archivo)
print(f'Plantilla generada en: {ruta_archivo}')
