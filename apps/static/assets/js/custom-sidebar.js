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
    
    // ========== HIGHLIGHT DE BÚSQUEDA ==========
    function initSearchHighlight() {
        var searchInput = $('#sidebar-search-input');
        var sidebar = $('.main-sidebar');
        var originalContent = {};
        
        // Guardar contenido original de cada link
        sidebar.find('.nav-link p').each(function() {
            var $p = $(this);
            var id = 'nav-text-' + Math.random().toString(36).substr(2, 9);
            $p.attr('data-original-id', id);
            originalContent[id] = $p.html();
        });
        
        // Función para resaltar texto
        function highlightText(text, query) {
            if (!query) return text;
            
            var regex = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
            return text.replace(regex, '<span class="sidebar-search-highlight">$1</span>');
        }
        
        // Función para restaurar contenido original
        function restoreOriginalContent() {
            sidebar.find('.nav-link p[data-original-id]').each(function() {
                var $p = $(this);
                var id = $p.attr('data-original-id');
                if (originalContent[id]) {
                    $p.html(originalContent[id]);
                }
            });
        }
        
        // Escuchar cambios en el input de búsqueda
        searchInput.on('input', function() {
            var query = $(this).val().trim();
            
            if (query.length > 0) {
                // Aplicar highlight a los resultados
                sidebar.find('.nav-link').each(function() {
                    var $link = $(this);
                    var $p = $link.find('p').first();
                    var id = $p.attr('data-original-id');
                    
                    if (id && originalContent[id]) {
                        var originalText = $('<div>').html(originalContent[id]).text();
                        
                        if (originalText.toLowerCase().includes(query.toLowerCase())) {
                            $p.html(highlightText(originalContent[id], query));
                            $link.show();
                            
                            // Scroll suave al primer resultado
                            if (sidebar.find('.sidebar-search-highlight').length === 1) {
                                var firstResult = sidebar.find('.sidebar-search-highlight').first().closest('.nav-item');
                                if (firstResult.length) {
                                    sidebar.find('.sidebar').animate({
                                        scrollTop: firstResult.position().top - 100
                                    }, 300);
                                }
                            }
                        } else {
                            $p.html(originalContent[id]);
                            $link.parent().hide();
                        }
                    }
                });
            } else {
                // Restaurar todo si no hay query
                restoreOriginalContent();
                sidebar.find('.nav-item').show();
            }
        });
        
        // Limpiar highlight cuando pierde foco
        searchInput.on('blur', function() {
            setTimeout(function() {
                restoreOriginalContent();
                sidebar.find('.nav-item').show();
            }, 300);
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
        
        if (dropdownToggle.length && dropdownMenu.length) {
            dropdownToggle.on('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                dropdownMenu.toggleClass('show');
                dropdownToggle.toggleClass('active');
            });
            
            // Cerrar dropdown al hacer click fuera
            $(document).on('click', function(e) {
                if (!$(e.target).closest('.user-profile-wrapper').length) {
                    dropdownMenu.removeClass('show');
                    dropdownToggle.removeClass('active');
                }
            });
        }
    }
    
    // ========== TEMA CLARO/OSCURO ==========
    function initThemeToggle() {
        var themeToggle = $('#themeToggle');
        var themeIcon = $('#themeIcon');
        var themeText = $('#themeText');
        var currentTheme = localStorage.getItem('sidebar-theme') || 'dark';
        
        // Aplicar tema guardado
        if (currentTheme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
            themeIcon.removeClass('fa-moon').addClass('fa-sun');
            themeText.text('Tema Claro');
        }
        
        themeToggle.on('click', function(e) {
            e.preventDefault();
            var html = document.documentElement;
            var currentTheme = html.getAttribute('data-theme');
            
            if (currentTheme === 'light') {
                html.removeAttribute('data-theme');
                themeIcon.removeClass('fa-sun').addClass('fa-moon');
                themeText.text('Tema Oscuro');
                localStorage.setItem('sidebar-theme', 'dark');
            } else {
                html.setAttribute('data-theme', 'light');
                themeIcon.removeClass('fa-moon').addClass('fa-sun');
                themeText.text('Tema Claro');
                localStorage.setItem('sidebar-theme', 'light');
            }
        });
    }
    
    // ========== FAVORITOS ==========
    function initFavorites() {
        var favoritesSection = $('#favoritesSection');
        var favoritesList = $('#favoritesList');
        var favorites = JSON.parse(localStorage.getItem('sidebar-favorites') || '[]');
        
        // Cargar favoritos guardados
        function loadFavorites() {
            favoritesList.empty();
            
            if (favorites.length > 0) {
                favoritesSection.show();
                
                favorites.forEach(function(fav) {
                    var item = $('<li class="nav-item"></li>');
                    var link = $('<a href="' + fav.url + '" class="nav-link"></a>');
                    link.html('<i class="nav-icon ' + fav.icon + '"></i><p>' + fav.title + '</p>');
                    item.append(link);
                    favoritesList.append(item);
                });
            } else {
                favoritesSection.hide();
            }
        }
        
        // Agregar estrellas a todos los items del menú
        $('.main-sidebar .nav-link').each(function() {
            var $link = $(this);
            var href = $link.attr('href');
            var title = $link.find('p').first().text().trim();
            var icon = $link.find('.nav-icon').attr('class') || 'fas fa-circle';
            
            // No agregar estrella si es un menú desplegable o no tiene href válido
            if (!href || href === '#' || $link.find('.right').length > 0) {
                return;
            }
            
            // Verificar si ya está en favoritos
            var isFavorite = favorites.some(f => f.url === href);
            var star = $('<i class="fas fa-star favorite-star' + (isFavorite ? ' active' : '') + '"></i>');
            
            $link.append(star);
            
            star.on('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (star.hasClass('active')) {
                    // Remover de favoritos
                    favorites = favorites.filter(f => f.url !== href);
                    star.removeClass('active');
                } else {
                    // Agregar a favoritos
                    favorites.push({
                        url: href,
                        title: title,
                        icon: icon
                    });
                    star.addClass('active');
                }
                
                localStorage.setItem('sidebar-favorites', JSON.stringify(favorites));
                loadFavorites();
            });
        });
        
        loadFavorites();
    }
    
    // ========== ATAJOS DE TECLADO ==========
    function initKeyboardShortcuts() {
        var keyboardHint = $('#keyboardHint');
        var searchInput = $('#sidebar-search-input');
        var body = $('body');
        
        // Ocultar hint después de 10 segundos
        setTimeout(function() {
            keyboardHint.addClass('hidden');
        }, 10000);
        
        // Mostrar modal con todos los atajos
        $('#keyboardShortcuts').on('click', function(e) {
            e.preventDefault();
            showKeyboardShortcutsModal();
        });
        
        // Detectar atajos de teclado
        $(document).on('keydown', function(e) {
            // Ctrl+K: Abrir búsqueda
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                if (body.hasClass('sidebar-collapse')) {
                    body.removeClass('sidebar-collapse');
                    setTimeout(function() {
                        searchInput.focus();
                    }, 300);
                } else {
                    searchInput.focus();
                }
            }
            
            // Ctrl+B: Toggle sidebar
            if (e.ctrlKey && e.key === 'b') {
                e.preventDefault();
                body.toggleClass('sidebar-collapse');
                localStorage.setItem('sidebar-state', body.hasClass('sidebar-collapse') ? 'collapsed' : 'expanded');
            }
            
            // ESC: Cerrar búsqueda
            if (e.key === 'Escape' && searchInput.is(':focus')) {
                searchInput.blur();
                searchInput.val('');
            }
        });
        
        function showKeyboardShortcutsModal() {
            var modal = `
                <div id="keyboardModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 9999; display: flex; align-items: center; justify-content: center;">
                    <div style="background: #fff; padding: 30px; border-radius: 12px; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
                        <h4 style="margin-bottom: 20px; color: #333;">⌨️ Atajos de Teclado</h4>
                        <table style="width: 100%; color: #555;">
                            <tr><td style="padding: 8px;"><kbd>Ctrl + K</kbd></td><td style="padding: 8px;">Abrir búsqueda</td></tr>
                            <tr><td style="padding: 8px;"><kbd>Ctrl + B</kbd></td><td style="padding: 8px;">Mostrar/Ocultar sidebar</td></tr>
                            <tr><td style="padding: 8px;"><kbd>ESC</kbd></td><td style="padding: 8px;">Cerrar búsqueda</td></tr>
                        </table>
                        <button id="closeModal" style="margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer;">Cerrar</button>
                    </div>
                </div>
            `;
            
            $('body').append(modal);
            
            $('#closeModal, #keyboardModal').on('click', function(e) {
                if (e.target.id === 'closeModal' || e.target.id === 'keyboardModal') {
                    $('#keyboardModal').remove();
                }
            });
        }
    }
    
    // ========== TRANSICIONES MEJORADAS ==========
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
