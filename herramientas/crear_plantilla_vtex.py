import xlwt
import os

libro = xlwt.Workbook()
hoja = libro.add_sheet('Articulos VTEX')

estilo_encabezado = xlwt.XFStyle()
font = xlwt.Font()
font.bold = True
font.name = 'Arial'
font.height = 220
estilo_encabezado.font = font

pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['ice_blue']
estilo_encabezado.pattern = pattern

borders = xlwt.Borders()
borders.left = xlwt.Borders.THIN
borders.right = xlwt.Borders.THIN
borders.top = xlwt.Borders.THIN
borders.bottom = xlwt.Borders.THIN
estilo_encabezado.borders = borders

alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
estilo_encabezado.alignment = alignment

estilo_ejemplo = xlwt.XFStyle()
font_ejemplo = xlwt.Font()
font_ejemplo.name = 'Arial'
font_ejemplo.height = 200
estilo_ejemplo.font = font_ejemplo

pattern_ejemplo = xlwt.Pattern()
pattern_ejemplo.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_ejemplo.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
estilo_ejemplo.pattern = pattern_ejemplo

borders_ejemplo = xlwt.Borders()
borders_ejemplo.left = xlwt.Borders.THIN
borders_ejemplo.right = xlwt.Borders.THIN
borders_ejemplo.top = xlwt.Borders.THIN
borders_ejemplo.bottom = xlwt.Borders.THIN
estilo_ejemplo.borders = borders_ejemplo

encabezados = ['Codigo', 'Descripcion', 'DescripcionMetaTag']

for col, encabezado in enumerate(encabezados):
    hoja.write(0, col, encabezado, estilo_encabezado)

ejemplos = [
    ['XV4SLL20A0101', 'CHELSEA PORTACOSMETICO', 'de la coleccion primavera-verano 2024/25 en cuotas sin interes en productos nacionales y envios a todo el pais.'],
    ['XV4SLL20A0109', 'CHELSEA PORTACOSMETICO', 'de la coleccion primavera-verano 2024/25 en cuotas sin interes en productos nacionales y envios a todo el pais.'],
    ['XV4SLL21A0101', 'PATTI COSMETIC', 'de la coleccion primavera-verano 2024/25 en cuotas sin interes en productos nacionales y envios a todo el pais.'],
    ['XV4SLL21B0558', 'PATTI FICHERO DOBLE', 'de la coleccion primavera-verano 2024/25 en cuotas sin interes en productos nacionales y envios a todo el pais.'],
    ['XV4SLL22B0301', 'CLARA FICH C SOLAPA Y CIERRE', 'de la coleccion primavera-verano 2024/25 en cuotas sin interes en productos nacionales y envios a todo el pais.']
]

for fila_idx, ejemplo in enumerate(ejemplos, start=1):
    for col_idx, valor in enumerate(ejemplo):
        hoja.write(fila_idx, col_idx, valor, estilo_ejemplo)

hoja.col(0).width = 4500
hoja.col(1).width = 9000
hoja.col(2).width = 20000

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
media_dir = os.path.join(project_root, 'media')

if not os.path.exists(media_dir):
    os.makedirs(media_dir)

ruta_archivo = os.path.join(media_dir, 'AltaArtVtex.xls')
libro.save(ruta_archivo)

print('Plantilla creada exitosamente en:', ruta_archivo)
print('Columnas: Codigo, Descripcion, DescripcionMetaTag')
print('5 filas de ejemplo incluidas')
