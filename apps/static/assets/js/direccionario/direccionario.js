/* ================================================
   DIRECCIONARIO - JS
   Patron: IIFE + objeto App
   ================================================ */
;(function ($) {
  'use strict';

  var CANAL_ICONS = {
    MAYORISTA:    'bi-bag-check-fill',
    FRANQUICIA:   'bi-shop',
    PROPIO:       'bi-building',
    ONLINE:       'bi-globe2',
    DISTRIBUIDOR: 'bi-truck',
  };

  var CANAL_COLOR_CLASSES = [
    'canal-0', 'canal-1', 'canal-2', 'canal-3', 'canal-4', 'canal-5'
  ];

  var App = {

    /* Estado */
    state: {
      sucursales: [],
      filtered:   [],
      view:            'cards',  // 'cards' | 'list'
      canal:           '',
      provincia:       '',
      tipo_local:      '',
      grupo_empresario:'',
      busqueda:        '',
      mostrar_todos:   false,
    },

    canalColorMap: {},
    canalColorIdx: 0,
    ajaxUrl:       '',

    /* -------- INIT -------- */
    init: function () {
      this.ajaxUrl = (window.DIRECCIONARIO_CONFIG || {}).ajaxUrl || '/../Extras/buscarSucursales';
      this._bindEvents();
      this._fetchData();
    },

    /* -------- BIND EVENTS -------- */
    _bindEvents: function () {
      var self = this;

      /* Busqueda con debounce */
      var debouncedSearch = this._debounce(function () {
        self.state.busqueda = $('#dir-search').val();
        self._fetchData();
      }, 300);
      $('#dir-search').on('input', debouncedSearch);

      /* Clear search */
      $('#dir-clear-search').on('click', function () {
        $('#dir-search').val('');
        self.state.busqueda = '';
        self._fetchData();
      });

      /* Filtros canal */
      $(document).on('click', '.dir-filter-btn[data-filter="canal"]', function () {
        self.state.canal = $(this).data('canal');
        $('.dir-filter-btn[data-filter="canal"]').removeClass('active');
        $(this).addClass('active');
        self._fetchData();
      });

      /* Filtros provincia */
      $(document).on('click', '.dir-filter-btn[data-filter="provincia"]', function () {
        self.state.provincia = $(this).data('prov');
        $('.dir-filter-btn[data-filter="provincia"]').removeClass('active');
        $(this).addClass('active');
        self._fetchData();
      });

      /* Filtros tipo local */
      $(document).on('click', '.dir-filter-btn[data-filter="tipo_local"]', function () {
        self.state.tipo_local = $(this).data('tlocal');
        $('.dir-filter-btn[data-filter="tipo_local"]').removeClass('active');
        $(this).addClass('active');
        self._fetchData();
      });

      /* Filtros grupo empresario */
      $(document).on('click', '.dir-filter-btn[data-filter="grupo"]', function () {
        self.state.grupo_empresario = $(this).data('grupo');
        $('.dir-filter-btn[data-filter="grupo"]').removeClass('active');
        $(this).addClass('active');
        self._fetchData();
      });

      /* Toggle mostrar todas vs solo principales */
      $(document).on('click', '#dir-toggle-todas', function () {
        self.state.mostrar_todos = !self.state.mostrar_todos;
        $(this).toggleClass('dir-toggle-todas-on', self.state.mostrar_todos);
        $(this).attr('title', self.state.mostrar_todos
          ? 'Mostrando TODAS las sucursales — click para ver solo principales'
          : 'Mostrando solo sucursales principales — click para ver todas');
        var $label = $('#dir-toggle-todas-label');
        $label.text(self.state.mostrar_todos ? 'Ver solo principales' : 'Ver todas');
        self._fetchData();
      });

      /* Reset all */
      $(document).on('click', '#dir-reset-all, #dir-reset-empty', function () {
        self.resetFilters();
      });

      /* Toggle vista */
      $('#dir-toggle-cards').on('click', function () { self._setView('cards'); });
      $('#dir-toggle-list').on('click',  function () { self._setView('list');  });

      /* Export Excel */
      $('#dir-export-excel').on('click', function () { self._exportExcel(); });

      /* Copy email (delegated) */
      $(document).on('click', '.dir-copy-btn', function () {
        self._copyToClipboard($(this).data('mail'));
      });

      /* Eliminar sucursal */
      $(document).on('click', '.dir-delete-btn', function () {
        var id     = $(this).data('id');
        var nombre = $(this).data('nombre');
        Swal.fire({
          title: '¿Deshabilitar sucursal?',
          html: 'Estás por deshabilitar <strong>#' + id + ' &ndash; ' + nombre + '</strong>.<br>Podrá ser habilitada nuevamente en el futuro.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, deshabilitar',
          cancelButtonText: 'Cancelar',
          confirmButtonColor: '#e53e3e',
        }).then(function (result) {
          if (result.isConfirmed) {
            $.ajax({
              url: '/../Extras/direccionario/eliminarSucursal/' + id,
              type: 'POST',
              data: { csrfmiddlewaretoken: self._getCsrf() },
              headers: { 'X-Requested-With': 'XMLHttpRequest' },
              success: function (res) {
                if (res.ok) {
                  self._toast(res.mensaje || 'Sucursal deshabilitada', 'success');
                  self._fetchData();
                } else {
                  self._toast(res.error || 'Error al deshabilitar', 'error');
                }
              },
              error: function () {
                self._toast('Error al deshabilitar la sucursal', 'error');
              },
            });
          }
        });
      });

      /* Mobile sidebar */
      $('#dir-hamburger').on('click', function () {
        $('#dir-sidebar').addClass('open');
        $('#dir-overlay').addClass('open');
      });
      $(document).on('click', '#dir-sidebar-close, #dir-overlay', function () {
        $('#dir-sidebar').removeClass('open');
        $('#dir-overlay').removeClass('open');
      });

      /* Chevron en filtros colapsables */
      $(document).on('hide.bs.collapse', function (e) {
        $('[data-target="#' + e.target.id + '"]').attr('aria-expanded', 'false');
      });
      $(document).on('show.bs.collapse', function (e) {
        $('[data-target="#' + e.target.id + '"]').attr('aria-expanded', 'true');
      });
    },

    /* -------- FETCH AJAX -------- */
    _fetchData: function () {
      var self = this;
      this._showLoading(true);

      $.ajax({
        url:  this.ajaxUrl,
        type: 'POST',
        data: {
          action:              'buscar',
          busqueda:            this.state.busqueda,
          canal:               this.state.canal,
          provincia:           this.state.provincia,
          tipo_local:          this.state.tipo_local,
          grupo_empresario:    this.state.grupo_empresario,
          mostrar_todos:       this.state.mostrar_todos ? 'true' : 'false',
          csrfmiddlewaretoken: this._getCsrf(),
        },
        success: function (res) {
          self.state.sucursales = res.sucursales || [];
          self.state.filtered   = self.state.sucursales.slice();
          self._buildColorMap();
          self._render();
        },
        error: function () {
          Swal.fire({
            icon: 'error',
            title: 'Error de conexion',
            text: 'No se pudieron cargar los datos. Reintentar mas tarde.',
          });
          self._showLoading(false);
        },
      });
    },

    /* -------- RENDER -------- */
    _render: function () {
      var data = this.state.filtered;
      this._updateCounter(data.length);

      if (!data.length) {
        $('#dir-empty').show();
        $('#dir-view-cards, #dir-view-list').hide();
        this._showLoading(false);
        return;
      }
      $('#dir-empty').hide();

      if (this.state.view === 'cards') {
        this._renderCards(data);
        $('#dir-view-cards').show();
        $('#dir-view-list').hide();
      } else {
        this._renderList(data);
        $('#dir-view-list').show();
        $('#dir-view-cards').hide();
      }
      this._showLoading(false);
    },

    /* -------- RENDER CARDS -------- */
    _renderCards: function (data) {
      var self  = this;
      var $grid = $('#dir-cards-grid').empty();

      $.each(data, function (i, d) {
        var delay      = Math.min(i * 40, 400);
        var colorIdx   = self.canalColorMap[d.canal] || 'canal-0';
        var icon       = self._getCanalIcon(d.canal);
        var mapsHref   = self._mapsUrl(d);
        var cfg        = window.DIRECCIONARIO_CONFIG || {};

        var boolIcon = function(val) {
          return (val === 'SI' || val === 'True' || val === '1' || val === 'true')
            ? '<i class="fas fa-check-circle" style="color:#38a169"></i>'
            : '<i class="fas fa-times-circle" style="color:#e53e3e"></i>';
        };

        /* ── Filas del body ── */
        var bodyRows = '';
        bodyRows += '<div class="sc-info-row">'
          + '<i class="fas fa-map-marker-alt"></i>'
          + '<span>' + self._esc(d.localidad) + (d.provincia ? ', ' + self._esc(d.provincia) : '') + '</span>'
          + '</div>';
        bodyRows += '<div class="sc-info-row">'
          + '<i class="fas fa-road"></i>'
          + '<span>' + self._esc(d.direccion || '-') + '</span>'
          + '</div>';
        if (d.telefono) {
          bodyRows += '<div class="sc-info-row">'
            + '<i class="fas fa-phone"></i>'
            + '<span>' + self._esc(d.telefono) + '</span>'
            + '</div>';
        }
        if (d.mail) {
          bodyRows += '<div class="sc-info-row">'
            + '<i class="fas fa-envelope"></i>'
            + '<a href="mailto:' + self._esc(d.mail) + '">' + self._esc(d.mail) + '</a>'
            + '</div>';
        }
        if (d.horario) {
          bodyRows += '<div class="sc-info-row">'
            + '<i class="fas fa-clock"></i>'
            + '<span>' + self._esc(d.horario) + '</span>'
            + '</div>';
        }

        /* ── Datos adicionales (colapsable) ── */
        var collapseId = 'sc-extra-' + d.nro_sucursal;
        var extraRows  = '';

        if (d.cod_client) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Cod. cliente</span>'
            + '<span>' + self._esc(d.cod_client) + '</span></div>';
        }
        if (d.tipo_local) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Tipo de local</span>'
            + '<span>' + self._esc(d.tipo_local) + '</span></div>';
        }
        if (d.grupo_empresario) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Grupo</span>'
            + '<span>' + self._esc(d.grupo_empresario) + '</span></div>';
        }
        if (d.supervisora) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Supervisora</span>'
            + '<span><i class="fas fa-user-tie mr-1 text-muted"></i>' + self._esc(d.supervisora) + '</span></div>';
        }
        extraRows += '<div class="sc-extra-row">'
          + '<span class="sc-extra-lbl">Tango</span><span>' + boolIcon(d.tango) + '</span>'
          + '<span class="sc-extra-lbl sc-extra-lbl-sep">Tienda</span><span>' + boolIcon(d.tienda) + '</span>'
          + '</div>';
        extraRows += '<div class="sc-extra-row">'
          + '<span class="sc-extra-lbl">Vtex</span><span>' + boolIcon(d.integra_vtex) + '</span>'
          + '<span class="sc-extra-lbl sc-extra-lbl-sep">Depósito</span><span>' + self._esc(d.deposito || '-') + '</span>'
          + '</div>';
        if (d.retiro_expres) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Retiro express</span>'
            + '<span>' + boolIcon(d.retiro_expres) + '</span></div>';
        }
        if (d.nro_sucursal_madre) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Suc. madre</span>'
            + '<span>' + self._esc(d.nro_sucursal_madre) + '</span></div>';
        }
        if (d.nro_sucursal_anterior) {
          extraRows += '<div class="sc-extra-row"><span class="sc-extra-lbl">Suc. anterior</span>'
            + '<span>' + self._esc(d.nro_sucursal_anterior) + '</span></div>';
        }

        // Campos técnicos (admin / soporteExt)
        if (cfg.canVerTecnico) {
          if (d.base_nombre) {
            extraRows += '<div class="sc-extra-row sc-extra-tec"><span class="sc-extra-lbl">'
              + '<i class="fas fa-database mr-1"></i>Base</span>'
              + '<span>' + self._esc(d.base_nombre) + '</span></div>';
          }
          if (d.conexion_dns) {
            extraRows += '<div class="sc-extra-row sc-extra-tec"><span class="sc-extra-lbl">'
              + '<i class="fas fa-network-wired mr-1"></i>DNS</span>'
              + '<span>' + self._esc(d.conexion_dns)
              + ' <button class="dir-copy-btn" data-mail="' + self._esc(d.conexion_dns) + '" title="Copiar">'
              + '<i class="fas fa-copy"></i></button></span></div>';
          }
          if (d.n_llave_tango) {
            extraRows += '<div class="sc-extra-row sc-extra-tec"><span class="sc-extra-lbl">'
              + '<i class="fas fa-key mr-1"></i>Llave</span>'
              + '<span>' + self._esc(d.n_llave_tango)
              + ' <button class="dir-copy-btn" data-mail="' + self._esc(d.n_llave_tango) + '" title="Copiar">'
              + '<i class="fas fa-copy"></i></button></span></div>';
          }
        }

        /* ── Botones de edición según permisos ── */
        var editBtns = '';
        if (cfg.canEdit) {
          editBtns = '<a href="/../Extras/direccionario/editarSucursalCompleta/' + d.nro_sucursal + '"'
            + ' class="sc-btn-icon" title="Editar completo"><i class="fas fa-pencil-alt"></i></a>';
        } else if (cfg.canEditBasic) {
          editBtns = '<a href="/../Extras/direccionario/editarSucursal/' + d.nro_sucursal + '"'
            + ' class="sc-btn-icon" title="Editar"><i class="fas fa-pencil-alt"></i></a>';
        }

        /* ── Botón eliminar (solo admin/Sistemas) ── */
        var deleteBtns = '';
        if (cfg.canDelete) {
          deleteBtns = '<button class="sc-btn-icon sc-btn-delete dir-delete-btn"'
            + ' data-id="' + d.nro_sucursal + '"'
            + ' data-nombre="' + self._esc(d.desc_sucursal) + '"'
            + ' title="Eliminar sucursal" style="color:#e53e3e"><i class="fas fa-trash-alt"></i></button>';
        }

        /* ── Botón de copiar email ── */
        var copyMailBtn = d.mail
          ? '<button class="sc-btn-icon dir-copy-btn" data-mail="' + self._esc(d.mail) + '" title="Copiar email">'
            + '<i class="fas fa-envelope"></i></button>'
          : '';

        /* ── Construir card ── */
        var card = '<div class="sucursal-card" style="animation-delay:' + delay + 'ms">'

          /* Header con gradiente */
          + '<div class="sc-header sc-canal-' + colorIdx + '">'
          +   '<span class="sc-canal-badge">' + self._esc(d.canal || 'S/C') + '</span>'
          +   '<div class="sc-icon-wrap"><i class="bi ' + icon + '"></i></div>'
          +   '<p class="sc-name">' + self._esc(d.desc_sucursal) + '</p>'
          +   '<span class="sc-nro">#' + d.nro_sucursal + '</span>'
          + '</div>'

          /* Body */
          + '<div class="sc-body">'
          +   bodyRows
          + '</div>'

          /* Datos adicionales colapsables */
          + '<div class="sc-collapse collapse" id="' + collapseId + '">'
          +   extraRows
          + '</div>'

          /* Footer */
          + '<div class="sc-footer">'
          +   '<a href="' + mapsHref + '" target="_blank" rel="noopener noreferrer" class="sc-btn-maps">'
          +     '<i class="fas fa-map-marker-alt"></i> Ver en Maps</a>'
          +   '<div class="sc-footer-actions">'
          +     copyMailBtn
          +     '<button class="sc-btn-icon sc-btn-toggle" data-toggle="collapse" data-target="#' + collapseId + '"'
          +       ' aria-expanded="false" title="Ver datos adicionales">'
          +       '<i class="fas fa-chevron-down sc-chevron"></i>'
          +     '</button>'
          +     editBtns
          +     deleteBtns
          +   '</div>'
          + '</div>'

          + '</div>';

        $grid.append(card);
      });
    },

    /* -------- RENDER LIST -------- */
    _renderList: function (data) {
      var self   = this;
      var $tbody = $('#dir-list-tbody').empty();

      $.each(data, function (_, d) {
        var colorClass = self.canalColorMap[d.canal] || 'canal-0';
        var mailCell   = d.mail
          ? '<a href="mailto:' + self._esc(d.mail) + '">' + self._esc(d.mail) + '</a>'
          : '-';
        var mapsHref = self._mapsUrl(d);

        var cfg = window.DIRECCIONARIO_CONFIG || {};
        var editCell = '';
        if (cfg.canEdit) {
          editCell = ' <a href="/../Extras/direccionario/editarSucursalCompleta/' + d.nro_sucursal
            + '" class="dir-btn-maps-sm btn btn-sm" title="Editar"><i class="fas fa-pencil-alt"></i></a>';
        } else if (cfg.canEditBasic) {
          editCell = ' <a href="/../Extras/direccionario/editarSucursal/' + d.nro_sucursal
            + '" class="dir-btn-maps-sm btn btn-sm" title="Editar"><i class="fas fa-pencil-alt"></i></a>';
        }

        var deleteCell = '';
        if (cfg.canDelete) {
          deleteCell = ' <button class="dir-btn-maps-sm btn btn-sm btn-danger dir-delete-btn"'
            + ' data-id="' + d.nro_sucursal + '"'
            + ' data-nombre="' + self._esc(d.desc_sucursal) + '"'
            + ' title="Eliminar"><i class="fas fa-trash-alt"></i></button>';
        }

        // Construir el contenido del collapse para la vista lista
        var trCollapseId = 'dir-tr-extra-' + d.nro_sucursal;
        var boolIcon = function(val) {
          return (val === 'SI' || val === 'True' || val === '1' || val === 'true')
            ? '<i class="fas fa-check-circle text-success"></i>'
            : '<i class="fas fa-times-circle text-danger"></i>';
        };
        var pills = '';
        if (d.tipo_local)       pills += '<span class="dir-pill"><i class="fas fa-store mr-1"></i>' + self._esc(d.tipo_local) + '</span>';
        if (d.grupo_empresario) pills += '<span class="dir-pill"><i class="fas fa-users mr-1"></i>' + self._esc(d.grupo_empresario) + '</span>';
        if (d.supervisora)      pills += '<span class="dir-pill"><i class="fas fa-user-tie mr-1"></i>' + self._esc(d.supervisora) + '</span>';
        pills += '<span class="dir-pill">Tango ' + boolIcon(d.tango) + '</span>';
        pills += '<span class="dir-pill">Tienda ' + boolIcon(d.tienda) + '</span>';
        pills += '<span class="dir-pill">Vtex ' + boolIcon(d.integra_vtex) + '</span>';
        if (d.deposito)        pills += '<span class="dir-pill">Dep. ' + self._esc(d.deposito) + '</span>';
        if (d.retiro_expres)   pills += '<span class="dir-pill">Ret.Exp. ' + boolIcon(d.retiro_expres) + '</span>';
        if (cfg.canVerTecnico) {
          if (d.base_nombre)   pills += '<span class="dir-pill dir-pill-tec"><i class="fas fa-database mr-1"></i>' + self._esc(d.base_nombre) + '</span>';
          if (d.conexion_dns)  pills += '<span class="dir-pill dir-pill-tec"><i class="fas fa-network-wired mr-1"></i>' + self._esc(d.conexion_dns)
            + ' <button class="dir-copy-btn" data-mail="' + self._esc(d.conexion_dns) + '" title="Copiar"><i class="fas fa-copy"></i></button></span>';
          if (d.n_llave_tango) pills += '<span class="dir-pill dir-pill-tec"><i class="fas fa-key mr-1"></i>' + self._esc(d.n_llave_tango)
            + ' <button class="dir-copy-btn" data-mail="' + self._esc(d.n_llave_tango) + '" title="Copiar"><i class="fas fa-copy"></i></button></span>';
        }

        var colspan = 10;
        $tbody.append('<tr>'
          + '<td><strong>#' + d.nro_sucursal + '</strong>'
          + (d.cod_client ? '<br><small class="text-muted">' + self._esc(d.cod_client) + '</small>' : '')
          + '</td>'
          + '<td>' + self._esc(d.desc_sucursal) + '</td>'
          + '<td><span class="dir-badge dir-badge-' + colorClass + '">'
          +   '<i class="bi ' + self._getCanalIcon(d.canal) + '"></i> ' + self._esc(d.canal || '-') + '</span></td>'
          + '<td>' + self._esc(d.localidad)  + '</td>'
          + '<td>' + self._esc(d.provincia)  + '</td>'
          + '<td>' + self._esc(d.direccion || '-') + '</td>'
          + '<td>' + self._esc(d.telefono || '-')  + '</td>'
          + '<td>' + mailCell + '</td>'
          + '<td>' + self._esc(d.horario || '-')   + '</td>'
          + '<td class="text-center" style="white-space:nowrap;">'
          +   '<a href="' + mapsHref + '" target="_blank" rel="noopener noreferrer"'
          +     ' class="dir-btn-maps-sm btn btn-sm" title="Ver en Maps">'
          +     '<i class="fas fa-map"></i></a>'
          +   ' <button class="dir-btn-maps-sm btn btn-sm dir-tr-toggle" data-toggle="collapse"'
          +     ' data-target="#' + trCollapseId + '" title="Ver más datos">'
          +     '<i class="fas fa-chevron-down dir-chevron"></i></button>'
          +   editCell
          +   deleteCell
          + '</td>'
          + '</tr>'
          + '<tr class="dir-tr-extra-row">'
          +   '<td colspan="' + colspan + '" class="p-0">'
          +     '<div id="' + trCollapseId + '" class="collapse dir-tr-extra-body">'
          +       '<div class="dir-pills-wrap">' + pills + '</div>'
          +     '</div>'
          +   '</td>'
          + '</tr>'
        );
      });
    },

    /* -------- HELPERS -------- */
    _setView: function (view) {
      this.state.view = view;
      if (view === 'cards') {
        $('#dir-toggle-cards').addClass('active');
        $('#dir-toggle-list').removeClass('active');
      } else {
        $('#dir-toggle-list').addClass('active');
        $('#dir-toggle-cards').removeClass('active');
      }
      this._render();
    },

    _updateCounter: function (n) {
      $('#dir-count').text(n + ' sucursal' + (n !== 1 ? 'es' : ''));
    },

    _showLoading: function (show) {
      if (show) {
        $('#dir-loading').show();
        $('#dir-content').hide();
      } else {
        $('#dir-loading').hide();
        $('#dir-content').show();
      }
    },

    _buildColorMap: function () {
      this.canalColorMap = {};
      this.canalColorIdx = 0;
      var self = this;
      $.each(this.state.sucursales, function (_, s) {
        if (s.canal && !self.canalColorMap[s.canal]) {
          self.canalColorMap[s.canal] = CANAL_COLOR_CLASSES[self.canalColorIdx % CANAL_COLOR_CLASSES.length];
          self.canalColorIdx++;
        }
      });
    },

    _cleanDireccion: function (str) {
      if (!str) return '';
      return str
        .replace(/\([^)]*\)/g, '')
        .replace(/-\s*LOCAL\s*\w+/gi, '')
        .replace(/L\d+\/\d+\s*$/gi, '')
        .trim();
    },

    _mapsUrl: function (d) {
      var parts = [this._cleanDireccion(d.direccion), d.localidad, d.provincia].filter(Boolean);
      return 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(parts.join(', '));
    },

    _getCanalIcon: function (canal) {
      if (!canal) return 'bi-geo-alt-fill';
      var c = canal.toUpperCase();
      for (var key in CANAL_ICONS) {
        if (c.indexOf(key) !== -1) return CANAL_ICONS[key];
      }
      return 'bi-geo-alt-fill';
    },

    _getCsrf: function () {
      var cookie = document.cookie.split(';').filter(function (c) {
        return c.trim().indexOf('csrftoken=') === 0;
      });
      if (cookie.length) return cookie[0].trim().split('=')[1];
      return $('[name=csrfmiddlewaretoken]').val() || '';
    },

    _copyToClipboard: function (text) {
      var self = this;
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () {
          self._toast('Email copiado al portapapeles', 'success');
        });
      } else {
        var el = document.createElement('textarea');
        el.value = text;
        el.style.cssText = 'position:absolute;left:-9999px';
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        self._toast('Email copiado al portapapeles', 'success');
      }
    },

    _toast: function (title, icon) {
      Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
      }).fire({ icon: icon || 'success', title: title });
    },

    _exportExcel: function () {
      var data = this.state.filtered;
      if (!data.length) {
        this._toast('No hay datos para exportar', 'warning');
        return;
      }
      if (typeof XLSX === 'undefined') {
        this._toast('La libreria de exportacion no esta disponible', 'error');
        return;
      }
      var rows = data.map(function (d) {
        return {
          'Nro Sucursal': d.nro_sucursal,
          'Cod Cliente':  d.cod_client,
          'Nombre':       d.desc_sucursal,
          'Canal':        d.canal,
          'Tipo Local':   d.tipo_local,
          'Direccion':    d.direccion,
          'Localidad':    d.localidad,
          'Provincia':    d.provincia,
          'Telefono':     d.telefono,
          'Email':        d.mail,
          'Horario':      d.horario,
          'Tango':        d.tango,
          'Tienda':       d.tienda,
        };
      });
      var ws = XLSX.utils.json_to_sheet(rows);
      var wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Direccionario');
      XLSX.writeFile(wb, 'Direccionario_Sucursales.xlsx');
    },

    resetFilters: function () {
      this.state.busqueda         = '';
      this.state.canal            = '';
      this.state.provincia        = '';
      this.state.tipo_local       = '';
      this.state.grupo_empresario = '';
      this.state.mostrar_todos    = false;
      $('#dir-search').val('');
      $('.dir-filter-btn[data-filter="canal"]').removeClass('active')
        .filter('[data-canal=""]').addClass('active');
      $('.dir-filter-btn[data-filter="provincia"]').removeClass('active')
        .filter('[data-prov=""]').addClass('active');
      $('.dir-filter-btn[data-filter="tipo_local"]').removeClass('active')
        .filter('[data-tlocal=""]').addClass('active');
      $('.dir-filter-btn[data-filter="grupo"]').removeClass('active')
        .filter('[data-grupo=""]').addClass('active');
      $('#dir-toggle-todas').removeClass('dir-toggle-todas-on')
        .attr('title', 'Mostrando solo sucursales principales — click para ver todas');
      $('#dir-toggle-todas-label').text('Ver todas');
      this._fetchData();
    },

    _esc: function (str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    },

    _debounce: function (fn, ms) {
      var timer;
      return function () {
        var args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () { fn.apply(null, args); }, ms);
      };
    },
  };

  window.DireccionarioApp = App;

  $(function () { App.init(); });

})(jQuery);
