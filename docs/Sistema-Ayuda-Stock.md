# Sistema de Ayuda para Tablas de Stock

## Descripción

Este sistema proporciona funcionalidades de ayuda avanzadas para las tablas de inventario en la aplicación AdminWeb, incluyendo tooltips informativos, modal de ayuda detallado y mejoras en la experiencia del usuario.

## Funcionalidades Implementadas

### 1. Tooltips Informativos
- **Ubicación**: Columnas de la tabla de stock
- **Activación**: Hover sobre los encabezados de columna
- **Características**:
  - Tooltips enriquecidos con HTML
  - Iconos contextuales
  - Información detallada sobre cada columna
  - Animaciones suaves
  - Diseño responsivo

### 2. Botón de Ayuda
- **Ubicación**: Esquina superior derecha del card de la tabla
- **Funcionalidad**: Abre modal con información completa
- **Características**:
  - Animaciones hover
  - Acceso rápido con `Ctrl + H`
  - Tooltip informativo sobre atajos

### 3. Modal de Ayuda Completo
- **Contenido**:
  - Descripción detallada de todas las columnas
  - Fórmulas de cálculo
  - Consideraciones importantes
  - Atajos de teclado
- **Características**:
  - Diseño responsivo
  - Iconos contextuales
  - Secciones organizadas
  - Animaciones de entrada

### 4. Mejoras en la Tabla
- **Resaltado inteligente de filas**:
  - Rojo: Sin stock disponible
  - Amarillo: Stock por debajo del nivel de seguridad
  - Azul: Productos con reservas activas
- **Tooltips en filas**: Información contextual sobre el estado del stock
- **Cálculo dinámico**: Total actualizado según filtros aplicados

## Archivos del Sistema

### CSS
- **Ubicación**: `/static/assets/css/stock-help-system.css`
- **Contenido**: Estilos reutilizables para tooltips, modales y componentes de ayuda

### JavaScript
- **Ubicación**: `/static/assets/js/stock-help-system.js`
- **Contenido**: Clase `StockHelpSystem` para funcionalidades de ayuda

### HTML Template
- **Archivo**: `StockCentral_ecommerce.html`
- **Modificaciones**: Integración de tooltips, modal y estilos

## Uso

### Implementación Básica
```html
<!-- Incluir CSS -->
<link rel="stylesheet" href="/static/assets/css/stock-help-system.css">

<!-- Incluir JavaScript -->
<script src="/static/assets/js/stock-help-system.js"></script>

<!-- Inicializar automáticamente -->
<script>
$(document).ready(function() {
    if ($('#example1').length > 0 && $('#helpModal').length > 0) {
        window.stockHelpSystem = new StockHelpSystem();
    }
});
</script>
```

### Configuración Personalizada
```javascript
var customHelpSystem = new StockHelpSystem({
    tooltipContainer: 'body',
    tooltipTrigger: 'hover focus',
    modalId: '#helpModal',
    tableId: '#example1',
    enableKeyboardShortcuts: true,
    enableRowHighlighting: true
});
```

### Agregar Tooltips Manualmente
```javascript
// Agregar tooltip a un elemento específico
stockHelpSystem.addTooltip('#miElemento', 'Texto del tooltip', 'top');

// Actualizar tooltip existente
stockHelpSystem.updateTooltip('#miElemento', 'Nuevo texto');

// Remover tooltip
stockHelpSystem.removeTooltip('#miElemento');
```

## Atajos de Teclado

- **`Ctrl + H`**: Abrir/cerrar modal de ayuda
- **`Esc`**: Cerrar modal de ayuda

## Personalización

### Agregar Nuevos Tooltips
1. Editar la configuración en `StockHelpSystem.getEcommerceStockConfig()`
2. Llamar a `applyEcommerceStockTooltips()` para aplicar automáticamente

### Modificar Estilos
1. Editar `/static/assets/css/stock-help-system.css`
2. Los estilos son modulares y reutilizables

### Agregar Nuevas Funcionalidades
1. Extender la clase `StockHelpSystem`
2. Agregar métodos según sea necesario

## Consideraciones Técnicas

### Dependencias
- jQuery
- Bootstrap 4
- FontAwesome
- DataTables

### Compatibilidad
- Navegadores modernos (Chrome, Firefox, Safari, Edge)
- Dispositivos móviles y tablets
- Modo de alto contraste

### Performance
- Tooltips con lazy loading
- Animaciones optimizadas con CSS
- Event delegation para mejor rendimiento

## Mantenimiento

### Actualizaciones de Contenido
1. Modificar las definiciones en el modal HTML
2. Actualizar tooltips en la configuración JavaScript
3. Sincronizar con cambios en el modelo de datos

### Depuración
- Console logs disponibles en modo desarrollo
- Verificar inicialización con `window.stockHelpSystem`
- Validar dependencias antes de usar

## Extensibilidad

### Para Otras Tablas
1. Copiar el modal de ayuda
2. Personalizar las definiciones de columnas
3. Aplicar estilos CSS existentes
4. Inicializar nueva instancia de `StockHelpSystem`

### Ejemplo para Nueva Tabla
```javascript
// Configuración para tabla de pedidos
var pedidosHelpSystem = new StockHelpSystem({
    modalId: '#pedidosHelpModal',
    tableId: '#pedidosTable',
    // ... otras opciones
});
```

## Soporte

Para reportar problemas o sugerir mejoras:
1. Documentar el comportamiento esperado vs actual
2. Incluir información del navegador y dispositivo
3. Proporcionar pasos para reproducir el problema

## Changelog

### v1.0 (Implementación inicial)
- Tooltips informativos en columnas
- Modal de ayuda completo
- Botón de ayuda con atajos
- Resaltado inteligente de filas
- Sistema modular y reutilizable
- Diseño responsivo
- Documentación completa