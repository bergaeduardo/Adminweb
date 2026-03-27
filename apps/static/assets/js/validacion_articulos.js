/* ═══════════════════════════════════════════════════════════════════
   Validación de Artículos — Lógica JavaScript
   apps/static/assets/js/validacion_articulos.js

   Requiere que el template defina VA_CONFIG antes de cargar este archivo:
     var VA_CONFIG = {
       accionesConfig:    <JSON del archivo acciones_validacion.json>,
       urlValidacion:     "<URL del endpoint AJAX>",
       fechaDesdeDefault: "<YYYY-MM-DD>",
     };
   ══════════════════════════════════════════════════════════════════ */
'use strict';

// ── Utilidades ─────────────────────────────────────────────────────
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function spinnerShow(tipo) {
  var msg = document.getElementById('va-spinner-msg');
  if (tipo === 'export') {
    msg.innerHTML = 'Generando archivo Excel, por favor espere\u2026' +
      '<br><small class="text-muted">El archivo se descargar\u00e1 autom\u00e1ticamente al finalizar.</small>';
  } else {
    msg.innerHTML = 'Ejecutando validaci\u00f3n, por favor espere\u2026' +
      '<br><small class="text-muted">Esta operaci\u00f3n puede demorar varios minutos.</small>';
  }
  document.getElementById('va-spinner').classList.add('active');
}

function spinnerHide() {
  document.getElementById('va-spinner').classList.remove('active');
}

// ── Instancia DataTable (se inicializa una sola vez) ───────────────
let dtTable = null;

function initDataTable() {
  if (dtTable) { dtTable.destroy(); }
  dtTable = $('#va-tabla').DataTable({
    responsive: true,
    autoWidth: false,
    pageLength: 50,
    order: [[0, 'desc']],
    language: {
      url: '/static/assets/plugins/datatables/i18n/Spanish.json',
      emptyTable: 'No se encontraron art\u00edculos con los filtros seleccionados.',
      zeroRecords: 'No hay coincidencias.',
    },
    columnDefs: [
      { targets: [1], width: '220px' },
      { targets: [7], orderable: false, className: 'text-center align-middle' },
      { targets: '_all', className: 'align-middle' },
    ],
  });
}

// ── Badge por estado / severidad ───────────────────────────────────
function badgeEstado(estado, severidad) {
  if (estado === 'OK') {
    return '<span class="badge badge-ok"><i class="fas fa-check-circle mr-1"></i>OK</span>';
  }
  if (severidad === 3) {
    return '<span class="badge badge-critico"><i class="fas fa-times-circle mr-1"></i>Cr\u00edtico</span>';
  }
  if (severidad === 2) {
    return '<span class="badge badge-advert"><i class="fas fa-exclamation-triangle mr-1"></i>Advertencia</span>';
  }
  return '<span class="badge badge-info"><i class="fas fa-info-circle mr-1"></i>Info</span>';
}

// ── Clase CSS de fila ───────────────────────────────────────────────
function rowClass(estado, severidad) {
  if (estado === 'OK')  return 'row-ok';
  if (severidad === 3)  return 'row-crit';
  if (severidad === 2)  return 'row-adv';
  return 'row-info';
}

// ── Acción sugerida según código de error y campo ──────────────────
// Textos configurables en herramientas/acciones_validacion.json
function accionSugerida(codigoError, campoValidacion) {
  var codigo = (!codigoError || codigoError === 'OK') ? 'OK' : codigoError;
  var campo  = (campoValidacion || '').trim();
  var errCfg = VA_CONFIG.accionesConfig[codigo] || VA_CONFIG.accionesConfig['*'] || {};
  return errCfg[campo] || errCfg['*'] || 'Revisar el error indicado y corregir seg\u00fan corresponda.';
}

// ── Convierte texto plano (con URLs) a HTML seguro con links ───────
function textoAHtml(str) {
  var escaped = str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
  return escaped.replace(
    /(https?:\/\/[^\s&"<>]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  );
}

// ── Poblar tabla con datos del SP ───────────────────────────────────
function poblarTabla(data) {
  if (dtTable) { dtTable.destroy(); dtTable = null; }

  const tbody = document.getElementById('va-tbody');
  tbody.innerHTML = '';

  data.forEach(function (fila) {
    const estado    = (fila.Estado || '').toUpperCase();
    const severidad = parseInt(fila.NivelSeveridad || 1, 10);
    const tr = document.createElement('tr');
    tr.className = rowClass(estado, severidad);

    var visibles = [
      fila.COD_ARTICU,
      fila.DESCRIPCION,
      fila.RUBRO,
      fila.PROVEEDOR,
      fila.TEMPORADA,
      fila.FAMILIA,
    ];
    tr.innerHTML = visibles.map(function (v) {
      return '<td>' + (v == null ? '' : String(v).replace(/</g, '&lt;').replace(/>/g, '&gt;')) + '</td>';
    }).join('');

    var tdEstado = document.createElement('td');
    tdEstado.innerHTML = badgeEstado(estado, severidad);
    tr.appendChild(tdEstado);

    var tdBtn = document.createElement('td');
    tdBtn.className = 'text-center';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-xs btn-outline-secondary va-btn-detalle';
    btn.title = 'Ver detalle';
    btn.innerHTML = '<i class="fas fa-search"></i>';
    btn.dataset.cod         = fila.COD_ARTICU || '';
    btn.dataset.descripcion = fila.DESCRIPCION || '';
    btn.dataset.fecha       = fila.FECHA_ALTA ? String(fila.FECHA_ALTA).substring(0, 10) : '';
    btn.dataset.tabla       = fila.TablaValidacion || '';
    btn.dataset.campo       = fila.CampoValidacion || '';
    btn.dataset.mensaje     = fila.MensajeValidacion || '';
    btn.dataset.codError    = fila.CodigoError || '';
    btn.dataset.estado      = estado;
    btn.dataset.severidad   = severidad;
    tdBtn.appendChild(btn);
    tr.appendChild(tdBtn);

    tbody.appendChild(tr);
  });

  initDataTable();

  // Delegación de eventos para el botón detalle (funciona con DataTables)
  $('#va-tbody').off('click', '.va-btn-detalle').on('click', '.va-btn-detalle', function () {
    var d = this.dataset;
    var estado    = d.estado;
    var severidad = parseInt(d.severidad, 10);
    document.getElementById('va-modal-cod').textContent         = d.cod;
    document.getElementById('va-modal-descripcion').textContent  = d.descripcion;
    document.getElementById('va-modal-fecha').textContent        = d.fecha;
    document.getElementById('va-modal-tabla').textContent        = d.tabla;
    document.getElementById('va-modal-campo').textContent        = d.campo;
    document.getElementById('va-modal-mensaje').textContent      = d.mensaje;
    document.getElementById('va-modal-cod-error').textContent    = d.codError || '\u2014';
    document.getElementById('va-modal-estado').innerHTML         = badgeEstado(estado, severidad);
    document.getElementById('va-modal-accion').innerHTML         = textoAHtml(accionSugerida(d.codError, d.campo));

    var bloqueMsg = document.getElementById('va-modal-bloque-mensaje');
    bloqueMsg.className = 'callout mb-3';
    if (estado === 'OK') {
      bloqueMsg.classList.add('callout-success');
    } else if (severidad === 3) {
      bloqueMsg.classList.add('callout-danger');
    } else if (severidad === 2) {
      bloqueMsg.classList.add('callout-warning');
    } else {
      bloqueMsg.classList.add('callout-info');
    }

    $('#va-modal-detalle').modal('show');
  });

  document.getElementById('va-total-badge').textContent = data.length + ' registros';
  document.getElementById('va-resultado').style.display = 'block';
  document.getElementById('va-resultado').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Recoger filtros del formulario ──────────────────────────────────
function recogerFiltros() {
  return {
    fecha_desde:      document.getElementById('va-fecha-desde').value,
    fecha_hasta:      document.getElementById('va-fecha-hasta').value,
    rubro:            document.getElementById('va-rubro').value,
    proveedor:        document.getElementById('va-proveedor').value,
    temporada:        document.getElementById('va-temporada').value,
    familia:          document.getElementById('va-familia').value,
    codigo_articulo:  document.getElementById('va-cod-art').value.trim(),
    solo_con_errores: document.getElementById('va-solo-errores').checked,
  };
}

// ── Validar segundo filtro obligatorio ──────────────────────────────
function segundoFiltroValido(filtros) {
  return (
    filtros.rubro           !== '' ||
    filtros.proveedor       !== '' ||
    filtros.temporada       !== '' ||
    filtros.familia         !== '' ||
    filtros.codigo_articulo !== ''
  );
}

// ── Poblar el form de exportación con los filtros activos ──────────
function sincronizarExportForm(filtros) {
  document.getElementById('exp-rubro').value           = filtros.rubro;
  document.getElementById('exp-proveedor').value       = filtros.proveedor;
  document.getElementById('exp-temporada').value       = filtros.temporada;
  document.getElementById('exp-familia').value         = filtros.familia;
  document.getElementById('exp-fecha-desde').value     = filtros.fecha_desde;
  document.getElementById('exp-fecha-hasta').value     = filtros.fecha_hasta;
  document.getElementById('exp-cod-art').value         = filtros.codigo_articulo;
  document.getElementById('exp-solo-errores').value    = filtros.solo_con_errores ? '1' : '0';
}

// ── Submit del formulario de búsqueda ───────────────────────────────
document.getElementById('va-form').addEventListener('submit', function (e) {
  e.preventDefault();

  const filtros = recogerFiltros();

  if (!segundoFiltroValido(filtros)) {
    document.getElementById('va-alerta-filtro').style.display = 'block';
    document.getElementById('va-alerta-filtro').scrollIntoView({ behavior: 'smooth' });
    return;
  }

  document.getElementById('va-alerta-filtro').style.display = 'none';
  spinnerShow('query');

  fetch(VA_CONFIG.urlValidacion, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(filtros),
  })
  .then(function (res) {
    if (!res.ok) { throw new Error('Error HTTP ' + res.status); }
    return res.json();
  })
  .then(function (resp) {
    spinnerHide();
    if (!resp.ok) {
      alert('Error al ejecutar la validaci\u00f3n:\n' + resp.error);
      return;
    }
    poblarTabla(resp.data);
    sincronizarExportForm(filtros);
  })
  .catch(function (err) {
    spinnerHide();
    alert('Error de comunicaci\u00f3n con el servidor:\n' + err.message);
  });
});

// ── Submit del formulario de exportación (con spinner de descarga) ──
// Técnica: el servidor setea la cookie "va_export_done=1" al finalizar.
// El cliente la detecta por polling y oculta el spinner.
document.getElementById('va-export-form').addEventListener('submit', function () {
  // Limpiar cookie previa
  document.cookie = 'va_export_done=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  spinnerShow('export');

  var pollInterval = setInterval(function () {
    if (document.cookie.indexOf('va_export_done=1') !== -1) {
      clearInterval(pollInterval);
      clearTimeout(fallbackTimeout);
      document.cookie = 'va_export_done=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
      spinnerHide();
    }
  }, 500);

  // Timeout de seguridad: 2 minutos
  var fallbackTimeout = setTimeout(function () {
    clearInterval(pollInterval);
    spinnerHide();
  }, 120000);
});

// ── Botón Limpiar ───────────────────────────────────────────────────
document.getElementById('va-btn-limpiar').addEventListener('click', function () {
  document.getElementById('va-fecha-desde').value = VA_CONFIG.fechaDesdeDefault;
  document.getElementById('va-fecha-hasta').value = '';
  $('#va-rubro').val('').trigger('change');
  $('#va-proveedor').val('').trigger('change');
  $('#va-temporada').val('').trigger('change');
  $('#va-familia').val('').trigger('change');
  document.getElementById('va-cod-art').value = '';
  document.getElementById('va-solo-errores').checked = false;
  document.getElementById('va-alerta-filtro').style.display = 'none';
  document.getElementById('va-resultado').style.display = 'none';
});

// ── Inicializar Select2 ─────────────────────────────────────────────
$(document).ready(function () {
  $('.select2').select2({
    theme: 'bootstrap4',
    allowClear: true,
    placeholder: '\u2014 Seleccionar \u2014',
    width: '100%',
  });
});
