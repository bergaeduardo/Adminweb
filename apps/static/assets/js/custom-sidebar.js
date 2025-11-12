/**
 * Custom Sidebar Behavior - Lakers Labs
 * Maneja el comportamiento fluido del sidebar en todas las páginas
 */

(function($) {
    'use strict';

    // Esperar a que el DOM esté listo
    $(document).ready(function() {
        
        // Función para manejar el estado del sidebar
        function initSidebarBehavior() {
            var body = $('body');
            var sidebar = $('.main-sidebar');
            
            // Si el sidebar existe
            if (sidebar.length) {
                
                // Asegurar que tenga las clases necesarias si no están
                if (!body.hasClass('sidebar-mini')) {
                    body.addClass('sidebar-mini');
                }
                
                // Guardar estado en localStorage
                var sidebarState = localStorage.getItem('sidebar-state');
                
                // Si hay un estado guardado, aplicarlo SIN transición
                if (sidebarState === 'collapsed') {
                    if (!body.hasClass('sidebar-collapse')) {
                        body.addClass('sidebar-collapse');
                    }
                } else if (sidebarState === 'expanded') {
                    body.removeClass('sidebar-collapse');
                }
                
                // Después de aplicar el estado, habilitar transiciones
                setTimeout(function() {
                    body.addClass('sidebar-loaded');
                }, 50);
                
                // Manejar el click en el botón de toggle
                $('[data-widget="pushmenu"]').on('click', function(e) {
                    e.preventDefault();
                    
                    // Esperar un tick para que AdminLTE procese primero
                    setTimeout(function() {
                        // Guardar el nuevo estado
                        if (body.hasClass('sidebar-collapse')) {
                            localStorage.setItem('sidebar-state', 'collapsed');
                        } else {
                            localStorage.setItem('sidebar-state', 'expanded');
                        }
                    }, 50);
                });
                
                // Manejar hover en sidebar colapsado
                if (body.hasClass('sidebar-collapse')) {
                    var hoverTimer;
                    
                    sidebar.on('mouseenter', function() {
                        clearTimeout(hoverTimer);
                        // Pequeño delay para evitar activación accidental
                        hoverTimer = setTimeout(function() {
                            sidebar.addClass('sidebar-hover');
                        }, 100);
                    });
                    
                    sidebar.on('mouseleave', function() {
                        clearTimeout(hoverTimer);
                        sidebar.removeClass('sidebar-hover');
                    });
                }
            }
        }
        
        // Inicializar comportamiento
        initSidebarBehavior();
        
        // Re-inicializar si el DOM cambia (para SPAs o contenido dinámico)
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    var body = $('body');
                    // Actualizar estado cuando cambian las clases del body
                    if (body.hasClass('sidebar-collapse')) {
                        localStorage.setItem('sidebar-state', 'collapsed');
                    } else if (body.hasClass('sidebar-mini')) {
                        localStorage.setItem('sidebar-state', 'expanded');
                    }
                }
            });
        });
        
        // Observar cambios en el body
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });
        
        // Asegurar transiciones suaves en navegación
        $(window).on('beforeunload', function() {
            // Guardar estado actual antes de navegar
            if ($('body').hasClass('sidebar-collapse')) {
                localStorage.setItem('sidebar-state', 'collapsed');
            } else {
                localStorage.setItem('sidebar-state', 'expanded');
            }
        });
    });
    
})(jQuery);
