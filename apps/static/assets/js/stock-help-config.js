/**
 * Configuración del Sistema de Ayuda para Tablas de Stock
 * Archivo centralizado para configurar tooltips, mensajes y comportamientos
 * 
 * @author Sistema Adminweb
 * @version 1.0
 */

window.StockHelpConfig = {
    
    // Configuraciones de tooltips por tabla
    tables: {
        
        // Configuración para Stock Central Ecommerce
        stockCentralEcommerce: {
            tooltips: {
                'ARTICULO': {
                    title: 'Código único del artículo en el sistema Tango.',
                    placement: 'top',
                    icon: 'fas fa-barcode'
                },
                'DESCRIPCION': {
                    title: 'Descripción detallada del producto según catálogo.',
                    placement: 'top',
                    icon: 'fas fa-info'
                },
                'DISPONIBLE': {
                    title: '<i class="fas fa-check-circle context-icon" style="color: #28a745;"></i><strong>Stock Disponible:</strong><br>Stock actualmente disponible para la venta (calculado automáticamente).<br><em>Fórmula: Total - Comprometido - Reservas - Excluido</em>',
                    placement: 'top',
                    icon: 'fas fa-check-circle'
                },
                'TOTAL': {
                    title: '<i class="fas fa-warehouse context-icon" style="color: #6f42c1;"></i><strong>Stock Total:</strong><br>Stock total físico en el depósito, incluyendo todo el inventario.',
                    placement: 'top',
                    icon: 'fas fa-warehouse'
                },
                'CANTIDAD COMPROMETIDA': {
                    title: '<i class="fas fa-handshake context-icon" style="color: #17a2b8;"></i><strong>Stock Comprometido:</strong><br>Stock reservado para pedidos confirmados pero no despachados aún.',
                    placement: 'top',
                    icon: 'fas fa-handshake'
                },
                'RESERVA ECOMMERCE': {
                    title: '<i class="fas fa-shopping-cart context-icon" style="color: #28a745;"></i><strong>Stock Exclusivo Ecommerce:</strong><br>Stock físico asignado exclusivamente al canal Ecommerce en el depósito 01.<br><em>Este stock está destinado únicamente para ventas online.</em>',
                    placement: 'top',
                    icon: 'fas fa-shopping-cart'
                },
                'RESERVA VTEX': {
                    title: '<i class="fas fa-pause-circle context-icon" style="color: #ffc107;"></i><strong>Stock Reservado por Pedidos Ecommerce:</strong><br>Stock bloqueado temporalmente en VTEX cuando:<br>• Un cliente agrega un producto al carrito<br>• Se inicia un pedido pero no se confirma<br><em>Si el pedido no se concreta, este stock se libera automáticamente.</em>',
                    placement: 'top',
                    icon: 'fas fa-pause-circle'
                },
                'STOCK EXCLUIDO': {
                    title: '<i class="fas fa-ban context-icon" style="color: #dc3545;"></i><strong>Stock Excluido:</strong><br>Stock no disponible para venta por:<br>• Productos dañados<br>• En proceso de revisión<br>• Reservado para uso interno',
                    placement: 'top',
                    icon: 'fas fa-ban'
                },
                'STOCK DE SEGURIDAD': {
                    title: '<i class="fas fa-shield-alt context-icon" style="color: #17a2b8;"></i><strong>Stock de Seguridad:</strong><br>Stock mínimo que debe mantenerse como reserva para evitar quiebres.<br><em>No se descuenta del disponible, pero sirve como alerta.</em>',
                    placement: 'top',
                    icon: 'fas fa-shield-alt'
                },
                'DEPOSITO': {
                    title: 'Código del depósito donde se encuentra físicamente el stock.',
                    placement: 'top',
                    icon: 'fas fa-building'
                },
                'RUBRO': {
                    title: 'Categoría o rubro al que pertenece el producto según clasificación Tango.',
                    placement: 'top',
                    icon: 'fas fa-tags'
                }
            },
            
            // Configuración de resaltado de filas
            rowHighlighting: {
                enabled: true,
                rules: [
                    {
                        condition: (data) => parseFloat(data[2]) <= 0,
                        className: 'table-danger',
                        title: 'Sin stock disponible - Revisar reposición urgente',
                        priority: 1
                    },
                    {
                        condition: (data) => {
                            const disponible = parseFloat(data[2]) || 0;
                            const stockSeguridad = parseFloat(data[8]) || 0;
                            return disponible > 0 && disponible <= stockSeguridad;
                        },
                        className: 'table-warning',
                        title: (data) => `Alerta: Stock por debajo del nivel de seguridad (${parseFloat(data[8]) || 0})`,
                        priority: 2
                    },
                    {
                        condition: (data) => {
                            const reservaEcommerce = parseFloat(data[5]) || 0;
                            const reservaVtex = parseFloat(data[6]) || 0;
                            return reservaEcommerce > 0 || reservaVtex > 0;
                        },
                        className: 'table-info',
                        title: 'Producto con reservas activas en canales Ecommerce',
                        priority: 3
                    }
                ]
            },
            
            // Configuración del modal de ayuda
            helpModal: {
                title: 'Información de la Tabla de Stock Ecommerce',
                sections: [
                    {
                        title: 'Descripción de Columnas',
                        icon: 'fas fa-table',
                        type: 'table'
                    },
                    {
                        title: 'Cálculos Importantes',
                        icon: 'fas fa-calculator',
                        type: 'calculations'
                    },
                    {
                        title: 'Consideraciones Importantes',
                        icon: 'fas fa-exclamation-triangle',
                        type: 'warnings'
                    },
                    {
                        title: 'Atajos de Teclado',
                        icon: 'fas fa-keyboard',
                        type: 'shortcuts'
                    }
                ]
            }
        },
        
        // Se pueden agregar configuraciones para otras tablas aquí
        stockUY: {
            tooltips: {
                // Configuración similar para tabla de stock UY
            }
        }
    },
    
    // Configuraciones globales del sistema
    global: {
        
        // Configuración de tooltips
        tooltip: {
            container: 'body',
            trigger: 'hover focus',
            html: true,
            delay: { show: 300, hide: 100 },
            animation: true
        },
        
        // Configuración de modales
        modal: {
            backdrop: true,
            keyboard: true,
            focus: true,
            show: false
        },
        
        // Atajos de teclado globales
        keyboardShortcuts: {
            help: 'ctrl+72', // Ctrl + H
            closeModal: '27'  // Esc
        },
        
        // Configuración de DataTables
        dataTable: {
            pageLength: 25,
            responsive: true,
            lengthChange: true,
            autoWidth: false,
            language: {
                search: "Buscar:",
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "No se encontraron registros que coincidan con la búsqueda",
                info: "Mostrando página _PAGE_ de _PAGES_ (_TOTAL_ registros en total)",
                infoEmpty: "No hay registros disponibles",
                infoFiltered: "(filtrado de _MAX_ registros totales)",
                paginate: {
                    first: "Primero",
                    last: "Último",
                    next: "Siguiente",
                    previous: "Anterior"
                },
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                emptyTable: "No hay datos disponibles en la tabla"
            }
        },
        
        // Configuración de animaciones
        animations: {
            enabled: true,
            duration: 300,
            easing: 'ease-in-out'
        },
        
        // Configuración de debugging
        debug: {
            enabled: false, // Cambiar a true para modo desarrollo
            logLevel: 'info' // 'error', 'warn', 'info', 'debug'
        }
    },
    
    // Mensajes del sistema
    messages: {
        loading: 'Cargando información...',
        noData: 'No hay datos disponibles',
        error: 'Error al cargar la información',
        helpLoaded: 'Sistema de ayuda cargado correctamente',
        tooltipError: 'Error al mostrar tooltip'
    },
    
    // Configuración de iconos por contexto
    icons: {
        help: 'fas fa-question-circle',
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle',
        error: 'fas fa-exclamation-circle',
        success: 'fas fa-check-circle',
        ecommerce: 'fas fa-shopping-cart',
        vtex: 'fas fa-pause-circle',
        excluded: 'fas fa-ban',
        security: 'fas fa-shield-alt',
        calculator: 'fas fa-calculator',
        keyboard: 'fas fa-keyboard',
        table: 'fas fa-table'
    },
    
    // Configuración de colores
    colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8',
        light: '#f8f9fa',
        dark: '#343a40'
    },
    
    // Métodos de utilidad
    utils: {
        
        /**
         * Obtener configuración de tabla específica
         */
        getTableConfig: function(tableName) {
            return this.tables[tableName] || {};
        },
        
        /**
         * Obtener configuración de tooltip para columna específica
         */
        getColumnTooltip: function(tableName, columnName) {
            const tableConfig = this.getTableConfig(tableName);
            return tableConfig.tooltips ? tableConfig.tooltips[columnName] : null;
        },
        
        /**
         * Validar configuración antes de usar
         */
        validateConfig: function() {
            const required = ['tables', 'global', 'messages'];
            return required.every(key => this.hasOwnProperty(key));
        },
        
        /**
         * Log de debugging según configuración
         */
        log: function(level, message, data = null) {
            if (!this.global.debug.enabled) return;
            
            const levels = ['error', 'warn', 'info', 'debug'];
            const configLevel = levels.indexOf(this.global.debug.logLevel);
            const messageLevel = levels.indexOf(level);
            
            if (messageLevel <= configLevel) {
                console[level](`[StockHelpSystem] ${message}`, data || '');
            }
        }
    }
};

// Validar configuración al cargar
if (window.StockHelpConfig.utils.validateConfig()) {
    window.StockHelpConfig.utils.log('info', 'Configuración del sistema de ayuda cargada correctamente');
} else {
    console.error('[StockHelpSystem] Error: Configuración incompleta');
}