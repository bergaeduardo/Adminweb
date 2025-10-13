/**
 * Sistema de Ayuda para Tablas de Stock
 * Funcionalidades para tooltips y modales de ayuda en tablas de inventario
 * 
 * @author Sistema Adminweb
 * @version 1.0
 */

class StockHelpSystem {
    constructor(options = {}) {
        this.options = {
            tooltipContainer: 'body',
            tooltipTrigger: 'hover focus',
            modalId: '#helpModal',
            tableId: '#example1',
            enableKeyboardShortcuts: true,
            enableRowHighlighting: true,
            ...options
        };
        
        this.init();
    }
    
    /**
     * Inicializar el sistema de ayuda
     */
    init() {
        this.initTooltips();
        this.initModal();
        this.initKeyboardShortcuts();
        this.initRowHighlighting();
        
        console.log('Stock Help System initialized');
    }
    
    /**
     * Inicializar tooltips de Bootstrap
     */
    initTooltips() {
        $('[data-toggle="tooltip"]').tooltip({
            container: this.options.tooltipContainer,
            trigger: this.options.tooltipTrigger,
            html: true,
            delay: { show: 300, hide: 100 }
        });
        
        // Ocultar tooltips cuando se abre el modal
        $(this.options.modalId).on('show.bs.modal', () => {
            $('[data-toggle="tooltip"]').tooltip('hide');
        });
    }
    
    /**
     * Configurar comportamiento del modal
     */
    initModal() {
        const modal = $(this.options.modalId);
        
        // Animación de entrada
        modal.on('show.bs.modal', function (e) {
            $(this).find('.modal-dialog').addClass('animate__animated animate__fadeInDown');
        });
        
        // Cleanup al cerrar
        modal.on('hidden.bs.modal', function (e) {
            $(this).find('.modal-dialog').removeClass('animate__animated animate__fadeInDown');
        });
    }
    
    /**
     * Configurar atajos de teclado
     */
    initKeyboardShortcuts() {
        if (!this.options.enableKeyboardShortcuts) return;
        
        $(document).keydown((e) => {
            // ESC para cerrar modal
            if (e.keyCode === 27) {
                $(this.options.modalId).modal('hide');
            }
            
            // Ctrl + H para abrir ayuda
            if (e.ctrlKey && e.keyCode === 72) {
                e.preventDefault();
                this.showHelp();
            }
        });
    }
    
    /**
     * Configurar resaltado de filas según stock
     */
    initRowHighlighting() {
        if (!this.options.enableRowHighlighting) return;
        
        // Se aplica en la configuración createdRow de DataTable
        // Ver implementación en el archivo HTML principal
    }
    
    /**
     * Mostrar modal de ayuda
     */
    showHelp() {
        $(this.options.modalId).modal('show');
    }
    
    /**
     * Agregar tooltip a elemento específico
     */
    addTooltip(selector, title, placement = 'top') {
        $(selector).attr({
            'data-toggle': 'tooltip',
            'data-placement': placement,
            'title': title
        }).tooltip({
            container: this.options.tooltipContainer,
            trigger: this.options.tooltipTrigger,
            html: true
        });
    }
    
    /**
     * Actualizar contenido de tooltip
     */
    updateTooltip(selector, newTitle) {
        $(selector).attr('data-original-title', newTitle);
    }
    
    /**
     * Remover tooltip
     */
    removeTooltip(selector) {
        $(selector).tooltip('dispose');
    }
    
    /**
     * Configuración específica para tablas de stock ecommerce
     */
    static getEcommerceStockConfig() {
        return {
            columns: {
                'RESERVA ECOMMERCE': 'Stock Exclusivo Ecommerce: Este es el stock físico asignado exclusivamente al canal Ecommerce en el depósito 01.',
                'RESERVA VTEX': 'Stock Reservado por Pedidos Ecommerce: Este es el stock bloqueado temporalmente en la plataforma VTEX cuando un cliente agrega un producto al carrito o inicia un pedido, pero aún no se confirma. Si el pedido no se concreta, este stock se libera nuevamente al disponible.',
                'STOCK EXCLUIDO': 'Stock excluido del cálculo de disponibilidad para la venta (productos dañados, en revisión, etc.).',
                'STOCK DE SEGURIDAD': 'Stock mínimo que debe mantenerse como reserva de seguridad para evitar quiebres.',
                'DISPONIBLE': 'Stock actualmente disponible para la venta (calculado automáticamente).',
                'TOTAL': 'Stock total físico en el depósito.',
                'CANTIDAD COMPROMETIDA': 'Stock comprometido para pedidos confirmados pero no despachados.'
            }
        };
    }
    
    /**
     * Aplicar configuración de tooltips automáticamente
     */
    applyEcommerceStockTooltips() {
        const config = StockHelpSystem.getEcommerceStockConfig();
        
        Object.entries(config.columns).forEach(([columnName, tooltip]) => {
            const headerCell = $(`th:contains("${columnName}")`);
            if (headerCell.length > 0) {
                this.addTooltip(headerCell, tooltip);
                // Agregar icono si no existe
                if (!headerCell.find('.fa-info-circle').length) {
                    headerCell.append(' <i class="fas fa-info-circle text-muted"></i>');
                }
            }
        });
    }
}

// Función de utilidad para crear rápidamente el sistema de ayuda
window.createStockHelpSystem = function(options = {}) {
    return new StockHelpSystem(options);
};

// Auto-inicialización si existe la tabla de stock
$(document).ready(function() {
    if ($('#example1').length > 0 && $('#helpModal').length > 0) {
        window.stockHelpSystem = new StockHelpSystem();
    }
});