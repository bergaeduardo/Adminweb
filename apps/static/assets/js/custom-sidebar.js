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
                
                // Agregar data-title a los links para tooltips
                $('.main-sidebar .nav-link').each(function() {
                    var $link = $(this);
                    var title = $link.find('p').first().text().trim();
                    if (title && !$link.attr('data-title')) {
                        $link.attr('data-title', title);
                    }
                });
                
                // Mejorar la detección de items activos (evitar marcado múltiple)
                fixActiveMenuItems();
                
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
    
    /**
     * Función para corregir items activos múltiples en el sidebar
     * Evita que el menú padre y el hijo estén marcados como activos simultáneamente
     */
    function fixActiveMenuItems() {
        var currentPath = window.location.pathname;
        
        // Encontrar todos los links activos
        var $activeLinks = $('.main-sidebar .nav-link.active');
        
        if ($activeLinks.length > 1) {
            // Si hay múltiples activos, mantener solo el más específico
            var mostSpecificLink = null;
            var longestMatch = 0;
            
            $activeLinks.each(function() {
                var $link = $(this);
                var href = $link.attr('href');
                
                if (href && href !== '#') {
                    // Obtener la longitud de la coincidencia
                    if (currentPath.includes(href) && href.length > longestMatch) {
                        longestMatch = href.length;
                        mostSpecificLink = $link;
                    }
                }
            });
            
            // Remover clase active de todos
            $activeLinks.removeClass('active');
            
            // Agregar solo al más específico
            if (mostSpecificLink) {
                mostSpecificLink.addClass('active');
                
                // Si es un subitem, marcar el padre como abierto pero no activo
                var $parentItem = mostSpecificLink.closest('.nav-treeview').siblings('.nav-link');
                if ($parentItem.length) {
                    $parentItem.removeClass('active'); // NO marcar como activo
                    $parentItem.closest('.nav-item').addClass('menu-open'); // Solo abierto
                }
            }
        }
        
        // Mejorar la visualización de items activos en submenús
        $('.main-sidebar .nav-treeview .nav-link.active').each(function() {
            var $this = $(this);
            var $parentNavItem = $this.closest('.nav-item').parent().closest('.nav-item');
            
            // Asegurar que el menú padre esté abierto
            $parentNavItem.addClass('menu-open');
            
            // Remover active del link padre si existe
            $parentNavItem.children('.nav-link').removeClass('active');
        });
    }
    
})(jQuery);
