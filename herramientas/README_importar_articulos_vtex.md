# Importar Artículos VTEX - Guía Completa

## 📋 Descripción

Esta herramienta permite importar artículos desde un archivo Excel para su procesamiento en VTEX. Los artículos son validados automáticamente contra la base de datos `SJ_ETIQUETAS_FINAL` antes de ser procesados.

## 🎯 Funcionalidades principales

- **Validación automática**: Verifica que los artículos existan en la base de datos
- **Interfaz intuitiva**: Proceso guiado paso a paso
- **Feedback visual**: Indica claramente los artículos con errores
- **Plantilla descargable**: Formato predefinido para facilitar la carga
- **Procesamiento en lote**: Permite cargar múltiples artículos simultáneamente

## 📁 Estructura del archivo Excel

### Formato requerido
- **Extensión**: `.xlsx` (Excel 2007 o superior)
- **Nombre**: Sin espacios en blanco

### Columnas principales

| Columna | Descripción | Obligatorio | Ejemplo |
|---------|-------------|-------------|---------|
| `ARTICULO` | Código del artículo en el sistema | ✅ Sí | G2502Z05 |
| `DESCRIPCION` | Descripción detallada del artículo | ⚠️ Recomendado | Producto ejemplo |

## 📝 Paso a paso

### 1. Descargar la plantilla
- Haz clic en el botón **"Descargar plantilla"**
- Se descargará el archivo `AltaArtVtex.xls`

### 2. Completar la información
- Abre el archivo con Microsoft Excel
- Completa los campos requeridos:
  - **ARTICULO**: Código del artículo (debe existir en `SJ_ETIQUETAS_FINAL`)
  - **DESCRIPCION**: Se completará automáticamente al validar
  - Otros campos según corresponda

### 3. Guardar el archivo
- Guarda el archivo en formato `.xlsx`
- Asegúrate de que el nombre no contenga espacios

### 4. Subir el archivo
- Haz clic en **"Elija el archivo"**
- Selecciona tu archivo Excel
- Haz clic en **"Cargar y procesar"**

### 5. Verificar los resultados
- Revisa la tabla de resultados
- Los artículos inválidos aparecerán:
  - Con fondo **rojo** 
  - Marcados con **asteriscos (*)**
  - Icono de advertencia ⚠️

## ⚠️ Requisitos y restricciones

### Requisitos técnicos
- Formato de archivo: `.xlsx` (Excel 2007 o superior)
- No usar formato `.xls` (versiones antiguas de Excel)
- Sin espacios en el nombre del archivo

### Validaciones automáticas
- ✅ Los artículos deben existir en `SJ_ETIQUETAS_FINAL`
- ✅ No se permiten celdas vacías en columnas principales
- ✅ Estructura de columnas debe coincidir con la plantilla

### Base de datos
- Conexión a: `LAKER_SA`
- Tabla de validación: `SJ_ETIQUETAS_FINAL`

## 🚨 Manejo de errores

### Artículos no encontrados
Si un artículo no existe en la base de datos:
- Aparecerá en la tabla con fondo **rojo**
- Se marcará con asteriscos: `*G2502Z05*`
- Se mostrará un mensaje de error
- El archivo NO se procesará completamente

### Formato incorrecto
Si el archivo no es `.xlsx`:
- Se rechazará automáticamente
- Se mostrará un mensaje de error
- El archivo se eliminará del sistema

### Artículos válidos
- Fondo blanco en la tabla
- Sin marcadores especiales
- La descripción se completa automáticamente

## 📊 Proceso interno

### Flujo de trabajo

```
1. Usuario sube archivo .xlsx
   ↓
2. Sistema valida extensión
   ↓
3. Sistema lee el archivo
   ↓
4. Para cada fila:
   - Valida artículo en SJ_ETIQUETAS_FINAL
   - Obtiene información adicional
   - Marca errores si existen
   ↓
5. Genera archivo de salida
   ↓
6. Muestra resultados en tabla
   ↓
7. Permite descargar archivo procesado
```

### Validación de artículos
```python
# Pseudocódigo del proceso de validación
for cada_fila in archivo_excel:
    articulo = fila['ARTICULO']
    resultado = validar_articulo(articulo)
    
    if resultado == 'ERROR':
        marcar_fila_con_error()
    else:
        obtener_informacion_completa()
        agregar_a_archivo_salida()
```

## 💡 Consejos y buenas prácticas

### Antes de cargar
- ✅ Descarga siempre la plantilla más reciente
- ✅ Verifica los códigos de artículo antes de cargar
- ✅ Mantén una copia de seguridad del archivo original
- ✅ Revisa que no haya celdas vacías

### Durante el proceso
- ⏳ Espera a que el proceso termine completamente
- 📊 No cierres la ventana mientras se procesa
- 🔄 No envíes el formulario múltiples veces

### Después de cargar
- 📋 Revisa la tabla de resultados cuidadosamente
- ⚠️ Corrige los artículos marcados en rojo
- 💾 Descarga el archivo procesado como respaldo
- 🔄 Si hay errores, corrígelos y vuelve a cargar

## 🔧 Resolución de problemas

### Problema: "El formato del archivo debe ser de tipo .xlsx"
**Solución**: 
- Asegúrate de guardar el archivo como Excel 2007+ (.xlsx)
- No uses el formato antiguo .xls

### Problema: "Hay artículos que no existen en SJ_ETIQUETAS_FINAL"
**Solución**:
- Verifica los códigos de artículo en rojo
- Corrige los códigos incorrectos
- Contacta al administrador si el artículo debería existir

### Problema: El archivo no se carga
**Solución**:
- Verifica que el archivo sea .xlsx
- Elimina espacios del nombre del archivo
- Asegúrate de que el archivo no esté corrupto
- Intenta con un archivo de prueba simple

### Problema: La tabla no se muestra
**Solución**:
- Verifica que el archivo tenga datos
- Asegúrate de que la primera fila contenga encabezados
- Revisa la consola del navegador para errores

## 📞 Soporte

Si tienes problemas o dudas:
1. Revisa esta documentación completa
2. Verifica los requisitos técnicos
3. Prueba con la plantilla de ejemplo
4. Contacta al equipo de soporte técnico

## 🔄 Actualizaciones

**Versión actual**: 2.0 (Modernizada)
- ✨ Interfaz mejorada y más intuitiva
- 📚 Guía de uso integrada
- 🎨 Diseño responsive y moderno
- 🔔 Notificaciones mejoradas
- 📊 Mejor visualización de resultados
- 🆘 Modal de ayuda detallada

---

**Última actualización**: Octubre 2025  
**Mantenido por**: Equipo de Desarrollo
