/**
 * Custom Sidebar Behavior - Lakers Labs
 * Maneja el comportamiento fluido del sidebar en todas las páginas
 */

(function($) {
    'use strict';

    // Esperar a que el DOM esté listo
    $(document).ready(function() {
        
        // DESACTIVAR el comportamiento de hover automático de AdminLTE
        $('body').removeClass('sidebar-mini-xs sidebar-mini-md').addClass('sidebar-mini');
        
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
                
                // Si NO hay estado guardado, usar el estado por defecto (colapsado)
                if (!sidebarState) {
                    // Por defecto, el sidebar debe estar colapsado
                    if (!body.hasClass('sidebar-collapse')) {
                        body.addClass('sidebar-collapse');
                    }
                    localStorage.setItem('sidebar-state', 'collapsed');
                } else {
                    // Si hay un estado guardado, aplicarlo SIN transición
                    if (sidebarState === 'collapsed') {
                        if (!body.hasClass('sidebar-collapse')) {
                            body.addClass('sidebar-collapse');
                        }
                    } else if (sidebarState === 'expanded') {
                        body.removeClass('sidebar-collapse');
                    }
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
                
                // Manejar el click en el botón de toggle (si existe)
                $('[data-widget="pushmenu"]').on('click', function(e) {
                    e.preventDefault();
                    
                    // Agregar clase transitioning durante el cambio
                    sidebar.addClass('transitioning');
                    
                    // Esperar un tick para que AdminLTE procese primero
                    setTimeout(function() {
                        // Guardar el nuevo estado
                        if (body.hasClass('sidebar-collapse')) {
                            localStorage.setItem('sidebar-state', 'collapsed');
                        } else {
                            localStorage.setItem('sidebar-state', 'expanded');
                        }
                        
                        // Remover clase transitioning después de la transición
                        setTimeout(function() {
                            sidebar.removeClass('transitioning');
                        }, 300);
                    }, 50);
                });
            }
        }
        
        // Inicializar comportamiento
        initSidebarBehavior();
        
        // Inicializar el plugin Treeview de AdminLTE
        $('[data-widget="treeview"]').Treeview('init');
        
        // Re-inicializar si el DOM cambia (para SPAs o contenido dinámico)
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    var body = $('body');
                    // Actualizar estado solo cuando cambia sidebar-collapse
                    if (body.hasClass('sidebar-collapse')) {
                        localStorage.setItem('sidebar-state', 'collapsed');
                    } else if (body.hasClass('sidebar-mini') && !body.hasClass('sidebar-collapse')) {
                        // Solo guardar como expandido si realmente está expandido
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

/**
 * Funcionalidad del buscador del sidebar
 * El buscador ahora siempre es visible y accesible
 */
(function($) {
    'use strict';
    
    $(document).ready(function() {
        var body = $('body');
        var searchInput = $('#sidebar-search-input');
        var searchBtn = $('.sidebar-search-form .btn-sidebar');
        
        // Cuando se hace click en el botón de búsqueda en sidebar colapsado
        searchBtn.on('click', function(e) {
            // Si el sidebar está colapsado, expandirlo
            if (body.hasClass('sidebar-collapse')) {
                e.preventDefault();
                body.removeClass('sidebar-collapse');
                localStorage.setItem('sidebar-state', 'expanded');
                
                // Enfocar el input después de la transición
                setTimeout(function() {
                    searchInput.focus();
                }, 350);
            }
            // Si está expandido, dejar que funcione normalmente
        });
        
        // Mejorar la experiencia cuando se escribe en el buscador
        searchInput.on('focus', function() {
            $(this).closest('.sidebar-search-form').addClass('search-active');
        });
        
        // Permitir cerrar con ESC
        searchInput.on('keydown', function(e) {
            if (e.key === 'Escape') {
                $(this).blur();
            }
        });
        
        // ========== AUTO-COLAPSAR SIDEBAR - VERSIÓN SIMPLE SIN HOVER ==========
        var autoCollapseTimer;
        var AUTO_COLLAPSE_DELAY = 8000; // 8 segundos
        var sidebar = $('.main-sidebar');
        
        // Función simple para colapsar
        function scheduleAutoCollapse() {
            clearTimeout(autoCollapseTimer);
            autoCollapseTimer = setTimeout(function() {
                if (!searchInput.is(':focus') && !body.hasClass('sidebar-collapse')) {
                    body.addClass('sidebar-collapse');
                    localStorage.setItem('sidebar-state', 'collapsed');
                }
            }, AUTO_COLLAPSE_DELAY);
        }
        
        // Solo manejar foco del input (NO mouseenter/mouseleave)
        searchInput.on('focus', function() {
            clearTimeout(autoCollapseTimer);
        });
        
        searchInput.on('blur', function() {
            setTimeout(function() {
                $('.sidebar-search-form').removeClass('search-active');
                scheduleAutoCollapse();
            }, 200);
        });
        
        // Cancelar auto-colapso si hay interacción directa
        sidebar.on('click', function() {
            clearTimeout(autoCollapseTimer);
        });
        
        // ========== BÚSQUEDA CON HIGHLIGHT ==========
        initSearchHighlight();
        
        // ========== TRANSICIONES SUAVES MEJORADAS (ÚNICO TOP 5 ACTIVO) ==========
        initSmoothTransitions();
    });
    
    // ========== BÚSQUEDA CON DROPDOWN DE RESULTADOS ==========
    function initSearchHighlight() {
        var searchInput = $('#sidebar-search-input');
        var resultsContainer = $('#sidebar-search-results');
        var sidebar = $('.main-sidebar');
        
        // Función para resaltar texto
        function highlightText(text, query) {
            if (!query) return text;
            var regex = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
            return text.replace(regex, '<span class="sidebar-search-highlight">$1</span>');
        }
        
        // Función para buscar en todos los niveles del menú
        function searchMenu(query) {
            var results = [];
            var seenUrls = {}; // Para evitar duplicados
            
            // Buscar en todos los nav-link del sidebar
            sidebar.find('.nav-link').each(function() {
                var $link = $(this);
                var $textElement = $link.find('p').first();
                var text = $textElement.text().trim();
                var href = $link.attr('href');
                
                // Ignorar si no tiene href válido o ya lo vimos
                if (!href || href === '#' || seenUrls[href]) {
                    return;
                }
                
                // Buscar coincidencia (case insensitive)
                if (text.toLowerCase().includes(query.toLowerCase())) {
                    // Determinar si es un item de nivel 1 o subnivel
                    var $parentItem = $link.closest('.nav-item');
                    var isSubItem = $parentItem.parent().hasClass('nav-treeview');
                    var parentText = '';
                    
                    if (isSubItem) {
                        // Es un subitem, obtener el texto del padre
                        var $parentLink = $parentItem.parent().closest('.nav-item').find('> .nav-link p').first();
                        parentText = $parentLink.text().trim();
                    }
                    
                    results.push({
                        text: text,
                        parentText: parentText,
                        href: href,
                        isSubItem: isSubItem,
                        element: $link
                    });
                    
                    seenUrls[href] = true; // Marcar como visto
                }
            });
            
            return results;
        }
        
        // Función para mostrar resultados en dropdown
        function displayResults(results, query) {
            resultsContainer.empty();
            
            if (results.length === 0) {
                resultsContainer.html('<div class="sidebar-search-no-results">No se encontraron resultados</div>');
                resultsContainer.show();
                return;
            }
            
            var resultsList = $('<ul class="nav nav-pills nav-sidebar flex-column"></ul>');
            
            results.forEach(function(result) {
                var highlightedText = highlightText(result.text, query);
                var itemHtml = '<li class="nav-item">';
                itemHtml += '<a href="' + result.href + '" class="nav-link">';
                itemHtml += '<i class="nav-icon fas fa-circle" style="font-size: 0.5rem;"></i>';
                itemHtml += '<p>';
                
                // Si es subitem, mostrar el padre
                if (result.isSubItem && result.parentText) {
                    itemHtml += '<span style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">' + result.parentText + ' / </span>';
                }
                
                itemHtml += highlightedText;
                itemHtml += '</p>';
                itemHtml += '</a>';
                itemHtml += '</li>';
                
                resultsList.append(itemHtml);
            });
            
            resultsContainer.html(resultsList);
            resultsContainer.show();
        }
        
        // Escuchar cambios en el input de búsqueda
        searchInput.on('input', function() {
            var query = $(this).val().trim();
            
            if (query.length > 0) {
                var results = searchMenu(query);
                displayResults(results, query);
            } else {
                resultsContainer.hide();
                resultsContainer.empty();
            }
        });
        
        // Cerrar dropdown cuando pierde foco y limpiar input
        searchInput.on('blur', function() {
            setTimeout(function() {
                resultsContainer.hide();
                resultsContainer.empty();
                searchInput.val('');
            }, 200);
        });
        
        // Evitar que el blur se dispare al hacer click en el dropdown
        resultsContainer.on('mousedown', function(e) {
            e.preventDefault();
        });
        
        // Mostrar dropdown cuando obtiene foco y hay texto
        searchInput.on('focus', function() {
            var query = $(this).val().trim();
            if (query.length > 0) {
                var results = searchMenu(query);
                displayResults(results, query);
            }
        });
        
        // Cerrar dropdown al hacer click en un resultado
        resultsContainer.on('click', 'a', function() {
            searchInput.val('');
            resultsContainer.hide();
            resultsContainer.empty();
        });
    }
    
    // ========== TRANSICIONES SUAVES MEJORADAS ==========
    function initSmoothTransitions() {
        var body = $('body');
        var sidebar = $('.main-sidebar');
        
        // Observar cambios en sidebar-collapse
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    if (body.hasClass('sidebar-collapse')) {
                        sidebar.addClass('sidebar-collapsing');
                        setTimeout(function() {
                            sidebar.removeClass('sidebar-collapsing');
                        }, 400);
                    } else {
                        sidebar.addClass('sidebar-expanding');
                        setTimeout(function() {
                            sidebar.removeClass('sidebar-expanding');
                        }, 400);
                    }
                }
            });
        });
        
        observer.observe(body[0], {
            attributes: true,
            attributeFilter: ['class']
        });
    }
    
})(jQuery);
