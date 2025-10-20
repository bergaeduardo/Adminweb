"""
Script para crear la plantilla de ejemplo AltaArtVtex.xls
Ejecutar este script para generar el archivo de plantilla en la carpeta media
"""

import xlwt
import os

# Crear un nuevo libro de Excel
libro = xlwt.Workbook()
hoja = libro.add_sheet('Artículos VTEX')

# Definir estilo para encabezados
estilo_encabezado = xlwt.XFStyle()
font = xlwt.Font()
font.bold = True
font.name = 'Arial'
font.height = 220  # 11 puntos
estilo_encabezado.font = font

# Definir patrón de fondo para encabezados
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['ice_blue']
estilo_encabezado.pattern = pattern

# Agregar bordes
borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
estilo_encabezado.borders = borders

# Centrar texto
alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
estilo_encabezado.alignment = alignment

# Definir estilo para ejemplos
estilo_ejemplo = xlwt.XFStyle()
font_ejemplo = xlwt.Font()
font_ejemplo.name = 'Arial'
font_ejemplo.height = 200  # 10 puntos
font_ejemplo.colour_index = xlwt.Style.colour_map['grey50']
font_ejemplo.italic = True
estilo_ejemplo.font = font_ejemplo

# Encabezados de las columnas
encabezados = ['ARTICULO', 'DESCRIPCION', 'OTROS']

# Escribir encabezados
for col, encabezado in enumerate(encabezados):
    hoja.write(0, col, encabezado, estilo_encabezado)

# Fila de ejemplo con datos reales (fila 1)
# Esta fila debe ser ELIMINADA por el usuario antes de agregar sus datos
ejemplos = [
    'G2502Z05', 
    'Ingrese descripción del artículo', 
    ''
]

for col, ejemplo in enumerate(ejemplos):
    hoja.write(1, col, ejemplo, estilo_ejemplo)

# Agregar nota informativa en fila 2
estilo_nota = xlwt.XFStyle()
font_nota = xlwt.Font()
font_nota.name = 'Arial'
font_nota.height = 180
font_nota.colour_index = xlwt.Style.colour_map['red']
font_nota.italic = True
estilo_nota.font = font_nota

hoja.write(2, 0, '⚠ IMPORTANTE: Eliminar esta fila de ejemplo antes de cargar sus datos', estilo_nota)

# Ajustar ancho de columnas
hoja.col(0).width = 4000  # ARTICULO
hoja.col(1).width = 8000  # DESCRIPCION
hoja.col(2).width = 6000  # OTROS

# Determinar la ruta donde guardar el archivo
# Usar la ruta del directorio media del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
media_dir = os.path.join(project_root, 'media')

# Crear carpeta media si no existe
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Ruta del archivo
ruta_archivo = os.path.join(media_dir, 'AltaArtVtex.xls')

# Guardar el archivo
libro.save(ruta_archivo)

print(f"✅ Plantilla creada exitosamente en: {ruta_archivo}")
print(f"📄 El archivo contiene {len(encabezados)} columnas: {', '.join(encabezados)}")
print(f"📝 Incluye una fila de ejemplo (debe ser eliminada antes de usar)")
print(f"⚠️  IMPORTANTE: La columna DESCRIPCION debe ser completada por el usuario")
