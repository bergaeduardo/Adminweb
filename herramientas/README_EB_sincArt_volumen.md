# Gestión de Volúmenes de Artículos (EB_sincArt_volumen)

## Descripción
Este módulo proporciona funcionalidad CRUD completa para la gestión de dimensiones y pesos de artículos almacenados en la tabla `EB_sincArt_volumen` de la base de datos SQL Server `LAKER_SA`.

## Características

### ✅ Funcionalidades Implementadas
- **Lista de artículos** con paginación y búsqueda
- **Vista detallada** con cálculos automáticos
- **Edición de artículos** con validación
- **Eliminación segura** con confirmación
- **Búsqueda avanzada** por código y descripción
- **Filtros por Estado y Rubro** con persistencia en paginación
- **Interfaz responsive** y moderna
- **Cálculos automáticos** de volumen y densidad

### 🔒 Campos de Solo Lectura
- `COD_ARTICULO` - Código del artículo
- `DESCRIPCION` - Descripción del artículo
- `Rubro` - Rubro del artículo
- `FECHA_ALTA` - Fecha de alta (no visible en formularios)
- `Activo` - Estado del registro (mostrado como Estado en la interfaz)
- `FECHA_SINC` - Fecha de sincronización (no visible en formularios)

### ✏️ Campos Editables
- `altoEmbalaje` - Alto del embalaje (mm)
- `anchoEmbalaje` - Ancho del embalaje (mm)
- `largoEmbalaje` - Largo del embalaje (mm)
- `altoReal` - Alto real del producto (mm)
- `anchoReal` - Ancho real del producto (mm)
- `largoReal` - Largo real del producto (mm)
- `pesoEmbalaje` - Peso del embalaje (gramos)
- `pesoReal` - Peso real del producto (gramos)

## Estructura de Archivos

### Modelos y Lógica de Negocio
```
herramientas/
├── models.py              # Clase EBSincArtVolumen
├── forms.py               # EBSincArtVolumenForm
├── sql_volumen.py         # Funciones de acceso a datos
└── views.py               # Vistas CRUD
```

### Templates
```
herramientas/templates/herramientas/eb_sinc_art_volumen/
├── list.html              # Listado con paginación y búsqueda
├── detail.html            # Vista detallada con cálculos
├── edit.html              # Formulario de edición
└── delete.html            # Confirmación de eliminación
```

### Filtros de Template
```
herramientas/templatetags/
├── __init__.py
└── volumen_filters.py     # Filtros para cálculos y formatos
```

## URLs

### Rutas Principales
- `/herramientas/eb-sinc-art-volumen/` - Lista de artículos
- `/herramientas/eb-sinc-art-volumen/<codigo>/` - Detalle del artículo
- `/herramientas/eb-sinc-art-volumen/<codigo>/edit/` - Editar artículo
- `/herramientas/eb-sinc-art-volumen/<codigo>/delete/` - Eliminar artículo

### Parámetros de URL
- `search` - Término de búsqueda (código o descripción)
- `page` - Número de página para paginación

## Funciones SQL

### `obtener_articulos_volumen()`
Lista todos los artículos ordenados por código.

### `obtener_articulo_volumen_por_codigo(cod_articulo)`
Obtiene un artículo específico por su código.

### `actualizar_articulo_volumen(cod_articulo, datos)`
Actualiza los campos editables y la fecha de sincronización.

### `crear_articulo_volumen(datos)`
Crea un nuevo registro (funcionalidad disponible para extensión futura).

### `eliminar_articulo_volumen(cod_articulo)`
Elimina un artículo de la base de datos.

### `buscar_articulos_volumen(termino_busqueda)`
Busca artículos por código o descripción usando LIKE.

## Validaciones y Reglas de Negocio

### Campos Numéricos
- Todos los campos numéricos aceptan valores enteros positivos
- Los campos pueden ser NULL/vacíos
- Los valores se expresan en:
  - Dimensiones: milímetros (mm)
  - Pesos: gramos (g)

### Seguridad
- Requiere autenticación (`@login_required`)
- Permisos: grupos `admin`, `Abastecimiento_Sup`, `Abastecimiento`
- Validación CSRF en todos los formularios
- Confirmación doble para eliminaciones

### Base de Datos
- Conexión: `mi_db_2` (LAKER_SA)
- Motor: SQL Server
- Actualización automática de `FECHA_SINC` en modificaciones

## Características de la Interfaz

### Lista de Artículos
- **Paginación**: 25 elementos por página
- **Búsqueda en tiempo real**: Filtro por código/descripción
- **Vista compacta**: Dimensiones resumidas con badges
- **Acciones rápidas**: Ver, Editar, Eliminar

### Vista Detallada
- **Información completa**: Todos los campos visibles
- **Cálculos automáticos**: Volumen, densidad, diferencias
- **Visualización gráfica**: Cards diferenciados por tipo
- **Navegación fluida**: Enlaces a edición y listado

### Formulario de Edición
- **Campos organizados**: Agrupación lógica por tipo
- **Acciones rápidas**: Copiar dimensiones, limpiar campos
- **Validación en vivo**: Cálculo automático de volúmenes
- **UX mejorada**: Tooltips y notificaciones

### Eliminación Segura
- **Confirmación doble**: Checkbox + confirmación JavaScript
- **Información completa**: Vista previa del registro a eliminar
- **Advertencias claras**: Consecuencias de la acción
- **Prevención de errores**: Botón deshabilitado hasta confirmar

## Cálculos Automáticos

### Volumen
```javascript
Volumen (mm³) = Alto × Ancho × Largo
```

### Densidad
```javascript
Densidad (g/cm³) = Peso (g) / (Volumen (mm³) / 1000)
```

### Diferencias
- Diferencia de peso: `Peso Embalaje - Peso Real`
- Comparación visual de dimensiones

## Configuración de Permisos

### Grupos de Usuario Autorizados
```python
# En sidebar_herramientas.html
{% if request.user|has_any_group:"admin,Abastecimiento_Sup,Abastecimiento" %}
```

### Decoradores de Seguridad
```python
@login_required(login_url="/login/")
```

## Extensiones Futuras

### Funcionalidades Potenciales
- [ ] Importación masiva desde Excel
- [ ] Exportación de datos a CSV/Excel
- [ ] Historial de cambios
- [ ] API REST para integración
- [ ] Validaciones avanzadas (rangos de dimensiones)
- [ ] Carga de imágenes de productos
- [ ] Calculadora de costos de envío
- [ ] Integración con sistemas de inventario

### Mejoras Técnicas
- [ ] Caché de consultas frecuentes
- [ ] Índices optimizados en base de datos
- [ ] Tests unitarios completos
- [ ] Logging de operaciones
- [ ] Backup automático antes de eliminaciones

## Troubleshooting

### Errores Comunes

**Error de conexión a base de datos**
```
Verificar configuración en production.py:
- HOST: 'SERVIDOR'
- Puerto: 1433
- Usuario: sa
- Base: LAKER_SA
```

**Campos no editables**
```
Los campos COD_ARTICULO y DESCRIPCION tienen readonly=True
en el formulario por diseño.
```

**Permisos insuficientes**
```
Verificar que el usuario pertenezca a alguno de estos grupos:
- admin
- Abastecimiento_Sup  
- Abastecimiento
```

## Notas de Desarrollo

### Patrones Utilizados
- **Repository Pattern**: Separación de lógica de datos en `sql_volumen.py`
- **Form-based Views**: Uso de formularios Django para validación
- **Template Inheritance**: Herencia de `layouts/base.html`
- **Custom Template Tags**: Filtros específicos para cálculos

### Consideraciones de Performance
- Paginación automática en listas grandes
- Consultas optimizadas con índices en COD_ARTICULO
- Lazy loading de relaciones cuando sea posible

### Mantenimiento
- Fechas de sincronización actualizadas automáticamente
- Logs de errores en Django logging
- Validación de integridad antes de operaciones críticas