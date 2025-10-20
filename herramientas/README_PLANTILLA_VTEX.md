# 📄 Plantilla de Importación VTEX

## 🎯 Ubicación

La plantilla de ejemplo se encuentra en:
```
media/AltaArtVtex.xls
```

## 📋 Estructura de la Plantilla

La plantilla contiene las siguientes columnas:

| Columna | Descripción | Obligatorio | Ejemplo |
|---------|-------------|-------------|---------|
| **ARTICULO** | Código del artículo que debe existir en SJ_ETIQUETAS_FINAL | ✅ Sí | G2502Z05 |
| **DESCRIPCION** | Descripción del artículo (debe completarse manualmente) | ✅ Sí | Producto ejemplo |
| **OTROS** | Información adicional según necesidades | ❌ No | - |

## 📝 Fila de Ejemplo

La plantilla incluye una fila de ejemplo con el formato:
- **ARTICULO**: `G2502Z05`
- **DESCRIPCION**: `Ingrese descripción del artículo`
- **OTROS**: (vacío)

**⚠️ IMPORTANTE**: 
- Esta fila debe ser **eliminada** antes de cargar tus datos reales
- La columna DESCRIPCION **NO** se completa automáticamente, debe ser ingresada por el usuario

## 🔄 Cómo Regenerar la Plantilla

Si necesitas regenerar la plantilla (por ejemplo, si se borra accidentalmente), sigue estos pasos:

### Método 1: Usando el script Python

```bash
# Navegar a la carpeta herramientas
cd c:\Users\santos.garcia\Desktop\Adminweb\herramientas

# Ejecutar el script
python crear_plantilla_vtex.py
```

### Método 2: Desde el entorno virtual

```bash
# Activar el entorno virtual
cd c:\Users\santos.garcia\Desktop\Adminweb
env\Scripts\activate

# Ejecutar el script
python herramientas\crear_plantilla_vtex.py
```

### Método 3: Con ruta completa de Python

```bash
C:/Users/santos.garcia/Desktop/Adminweb/env/Scripts/python.exe c:\Users\santos.garcia\Desktop\Adminweb\herramientas\crear_plantilla_vtex.py
```

## 📦 Dependencias Necesarias

Para regenerar la plantilla, necesitas tener instalado:

```bash
pip install xlwt==1.3.0
```

Esta dependencia ya está incluida en `requirements.txt`.

## 🎨 Características de la Plantilla

### Formato Visual
- ✅ Encabezados con fondo azul claro
- ✅ Texto en negrita para encabezados
- ✅ Bordes en las celdas
- ✅ Ancho de columnas ajustado
- ✅ Fila de ejemplo en cursiva y color gris

### Especificaciones Técnicas
- **Formato**: Excel 97-2003 (.xls)
- **Hoja**: "Artículos VTEX"
- **Codificación**: Compatible con xlwt
- **Tamaño**: ~5 KB

## ⚠️ Notas Importantes

1. **Formato del archivo para cargar**: Aunque la plantilla es .xls, el sistema **requiere archivos .xlsx** para la carga
2. **Conversión**: Después de completar la plantilla .xls, guárdala como .xlsx antes de subirla
3. **Validación**: Los códigos de artículo deben existir en la tabla SJ_ETIQUETAS_FINAL
4. **Primera fila**: Es el encabezado, no la elimines
5. **Segunda fila**: Es un ejemplo, debes eliminarla antes de agregar tus datos

## 📖 Cómo Usar la Plantilla

### Paso 1: Descargar
1. Ve a la herramienta de importación VTEX
2. Haz clic en "Descargar plantilla"
3. El archivo `AltaArtVtex.xls` se descargará

### Paso 2: Completar
1. Abre el archivo con Excel
2. **Elimina las filas 2 y 3** (fila de ejemplo y advertencia)
3. Completa la columna **ARTICULO** con los códigos de artículos
4. Completa la columna **DESCRIPCION** con las descripciones de cada artículo
5. Opcionalmente completa la columna OTROS

### Paso 3: Guardar
1. Ve a Archivo > Guardar como
2. Selecciona formato: **Excel 2007-365 (*.xlsx)**
3. Guarda con un nombre sin espacios

### Paso 4: Subir
1. En la herramienta web, haz clic en "Elija el archivo"
2. Selecciona tu archivo .xlsx
3. Haz clic en "Cargar y procesar"

## 🔍 Ejemplo Completo

### Plantilla Completada (después de eliminar las filas de ejemplo)
```
| ARTICULO  | DESCRIPCION                    | OTROS |
|-----------|--------------------------------|-------|
| G2502Z05  | Producto de ejemplo A          |       |
| A1234B56  | Producto de ejemplo B          |       |
| Z9876C43  | Producto de ejemplo C          |       |
```

### Después del Procesamiento en el Sistema
El sistema validará que los códigos de artículos existan en la base de datos SJ_ETIQUETAS_FINAL.
Los artículos válidos se procesarán, los inválidos se marcarán en rojo con asteriscos (*).

## 🛠️ Script de Generación

El script `crear_plantilla_vtex.py` hace lo siguiente:

1. Crea un nuevo libro Excel (.xls)
2. Define estilos para encabezados (azul, negrita, bordes)
3. Define estilos para ejemplos (gris, cursiva)
4. Escribe los encabezados: ARTICULO, DESCRIPCION, OTROS
5. Agrega una fila de ejemplo
6. Ajusta el ancho de las columnas
7. Guarda el archivo en `media/AltaArtVtex.xls`

## 📞 Soporte

Si tienes problemas con la plantilla:

1. **No se descarga**: Regenera la plantilla con el script
2. **Error de formato**: Asegúrate de guardar como .xlsx antes de subir
3. **Artículos inválidos**: Verifica que existan en SJ_ETIQUETAS_FINAL
4. **Errores al regenerar**: Verifica que xlwt esté instalado

## 🔄 Historial de Cambios

- **v1.0** (Octubre 2025): Creación inicial de la plantilla
  - 3 columnas: ARTICULO, DESCRIPCION, OTROS
  - Formato con estilos y ejemplo
  - Script de generación automatizado

---

**Última actualización**: Octubre 2025  
**Mantenido por**: Equipo de Desarrollo  
**Archivo relacionado**: `herramientas/crear_plantilla_vtex.py`
