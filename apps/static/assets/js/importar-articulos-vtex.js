/**
 * ============================================
 * Scripts personalizados para Importar Artículos VTEX
 * ============================================
 */

/**
 * Función para cerrar el modal de éxito después de descargar
 */
function closeSuccessModal() {
  setTimeout(function() {
    $('#successModal').modal('hide');
  }, 1000);
}

/**
 * Función para recargar la página completamente
 */
function reloadPage() {
  // Mostrar indicador de carga
  $('body').append('<div id="loadingOverlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; display: flex; justify-content: center; align-items: center;"><div style="text-align: center; color: white;"><i class="fas fa-spinner fa-spin" style="font-size: 3rem; margin-bottom: 1rem;"></i><h4>Preparando nueva carga...</h4></div></div>');
  
  // Cerrar todos los modales abiertos
  $('.modal').modal('hide');
  
  // Esperar a que los modales se cierren y recargar
  setTimeout(function() {
    // Recargar la página forzando desde el servidor (sin parámetros en URL)
    location.reload(true);
  }, 500);
}

/**
 * Inicialización al cargar el documento
 */
$(document).ready(function() {
  
  // Inicializar tooltips de Bootstrap
  $('[data-toggle="tooltip"]').tooltip();
  
  // ============================================
  // RESALTAR FILAS CON ERRORES
  // ============================================
  
  // Marcar en rojo las filas con artículos inválidos (que contienen *)
  $("td:nth-of-type(1):contains('*')").parent().css({
    "background-color": "#F1948A",
    "font-weight": "bold"
  });

  // Añadir icono de advertencia a celdas con asterisco
  $("td:contains('*')").each(function() {
    if ($(this).text().indexOf('*') !== -1) {
      $(this).prepend('<i class="fas fa-exclamation-triangle text-danger mr-1"></i>');
    }
  });

  // ============================================
  // VALIDACIÓN DE ARCHIVO ANTES DE ENVIAR
  // ============================================
  
  $('form').on('submit', function(e) {
    var fileInput = $('#exampleInputFile');
    var file = fileInput[0].files[0];
    
    if (file) {
      // Verificar extensión
      var fileName = file.name;
      var fileExt = fileName.split('.').pop().toLowerCase();
      
      if (fileExt !== 'xlsx') {
        e.preventDefault();
        toastr.error('El archivo debe ser formato .xlsx (Excel 2007 o superior)', 'Error de formato', {
          "closeButton": true,
          "progressBar": true
        });
        return false;
      }
      
      // Verificar espacios en el nombre
      if (fileName.indexOf(' ') !== -1) {
        toastr.warning('El nombre del archivo contiene espacios. Se eliminarán automáticamente.', 'Advertencia', {
          "closeButton": true,
          "progressBar": true,
          "timeOut": "3000"
        });
      }

      // Mostrar indicador de carga
      $('#botonCargar').html('<i class="fas fa-spinner fa-spin"></i> Procesando...').prop('disabled', true);
    }
  });
  
  // NOTA: El plugin bs-custom-file-input ya maneja la actualización del label del archivo
  // No es necesario agregar otro evento 'change' aquí para evitar duplicación
  
});
