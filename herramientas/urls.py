# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "herramientas"
urlpatterns = [
    # Logistica

    path("Calendario/TurnoListView", views.Listar_turno, name="herramientas_listar_turno"),
    path('Calendario/NuevoTurnoProveedor', views.Crear_turno, name='herramientas_crear_turno'),
    path('Calendario/EditarTurnoProveedor/<int:IdTurno>', views.Editar_Turno, name='herramientas_editar_turno_calendario'),
    path('Gestion_cronograma', views.Gestion_cronograma, name='herramientas_gestion_cronograma'),
    path('Gestion_guias_mayoristas', views.Gestion_guias_mayoristas, name='herramientas_gestion_guias_mayoristas'),
    path('registro', views.registro_turno, name='herramientas_registro_turno'),
    path('get_nombre_proveedor', views.get_nombre_proveedor, name='herramientas_get_nombre_proveedor'),
    path('listado', views.listado_turnos, name='herramientas_listado_turnos'),
    path('eliminar/<int:turno_id>', views.eliminar_turno, name='herramientas_eliminar_turno'),
    path('ver/<int:turno_id>', views.ver_turno, name='herramientas_ver_turno'),
    path('editar/<int:turno_id>', views.editar_turno, name='herramientas_editar_turno'),
    path('lista_codigos_error', views.lista_codigos_error, name='herramientas_lista_codigos_error'),
    path('crear_codigo_error', views.crear_codigo_error, name='herramientas_crear_codigo_error'),
    path('editar_codigo_error/<int:codigo_id>', views.editar_codigo_error, name='herramientas_editar_codigo_error'),
    path('eliminar_codigo_error/<int:codigo_id>', views.eliminar_codigo_error, name='herramientas_eliminar_codigo_error'),
    
    # Nuevas URLs para Calendario de Reservas
    path('calendario_reservas', views.calendario_reservas, name='herramientas_calendario_reservas'),
    path('obtener_turnos_calendario', views.obtener_turnos_calendario, name='herramientas_obtener_turnos_calendario'),
    path('obtener_slots_disponibles', views.obtener_slots_disponibles, name='herramientas_obtener_slots_disponibles'),
    path('nueva_reserva', views.nueva_reserva_turno, name='herramientas_nueva_reserva_turno'),
    path('editar_reserva/<int:turno_id>', views.editar_reserva_turno, name='herramientas_editar_reserva_turno'),
    path('eliminar_reserva/<int:turno_id>', views.eliminar_reserva_turno, name='herramientas_eliminar_reserva_turno'),
    path('detalle_reserva/<int:turno_id>', views.detalle_reserva_turno, name='herramientas_detalle_reserva_turno'),
    path('listado_reservas', views.listado_reservas, name='herramientas_listado_reservas'),
    
    # URLs para Gestión de Estados de Turnos (Admin y Logistica_Sup)
    path('estados_turno/listado', views.listado_estados_turno, name='herramientas_listado_estados_turno'),
    path('estados_turno/crear', views.crear_estado_turno, name='herramientas_crear_estado_turno'),
    path('estados_turno/editar/<int:estado_id>', views.editar_estado_turno, name='herramientas_editar_estado_turno'),
    path('estados_turno/eliminar/<int:estado_id>', views.eliminar_estado_turno, name='herramientas_eliminar_estado_turno'),
    path('estados_turno/reordenar', views.reordenar_estados_turno, name='herramientas_reordenar_estados_turno'),
    path('estados_turno/marcar_no_confirmados', views.ejecutar_marcar_no_confirmados, name='herramientas_marcar_no_confirmados'),
    
    path("cargaAnticipoGrupo", views.CargaAnticipoGrupo, name="herramientas_carga_anticipo_grupo"),
    path("ImpRotulos", views.ImpRotulos, name="herramientas_imprimir_rotulos"),
    path("ImpRemEcom", views.ImpRemEcom, name="herramientas_importar_rem_ecom"),
    path("ImprimirEtiquetasBultos", views.ImprimirEtiquetasBultos, name="herramientas_imprimir_etiquetas_bultos"),
    path("RemisionMasiva", views.RemisionMasiva, name="herramientas_remision_masiva"),

    # Abastecimiento
    path('Stock_excluido', views.Stock_excluido, name='herramientas_stock_excluido'),
    path('Carga_de_orden', views.Carga_de_orden, name='herramientas_carga_orden'),
    path('Activar_orden', views.Activar_orden, name='herramientas_activar_orden'),
    path('Desactivar_orden', views.Desactivar_orden, name='herramientas_desactivar_orden'),
    path('Recodificacion', views.Recodificacion, name='herramientas_recodificacion'),
    path('MaestroDestinos', views.MaestroDestinos, name='herramientas_maestro_destinos'),
    path('GestionEquivalentes', views.GestionEquivalentes, name='herramientas_gestion_equivalentes'),
    path('StockBase', views.StockBase, name='herramientas_stock_base'),
    # Comercial
    path('GestionCategoriaProductos', views.Gestion_categoria_productos, name='herramientas_gestion_categoria_productos'),
    path('AdministrarCuotas', views.AdministrarCuotas, name='herramientas_administrar_cuotas'),
    path('AdministrarInternos', views.AdministrarInternos, name='herramientas_administrar_internos'),
    path('PromoBancos', views.PromoBancos, name='herramientas_promo_bancos'),
    path('AltaNuevosLocales', views.AltaNuevosLocales, name='herramientas_alta_nuevos_locales'),
    path('UsuariosFranquicias', views.UsuariosFranquicias, name='herramientas_usuarios_franquicias'),
    path('ObjetivosVentaFranquicias', views.ObjetivosVentaFranquicias, name='herramientas_objetivos_venta_franquicias'),
    path('gestionKits', views.gestionKits, name='herramientas_gestion_kits'),
    # Mayoristas
    path('Adm_Pedido', views.Adm_Pedido, name='herramientas_adm_pedido'),
    # Ecommerce
    path('Control_pedidos', views.Control_pedidos, name='herramientas_control_pedidos'),
    path('StockSegVtex', views.StockSegVtex, name='herramientas_stock_seguridad_vtex'),
    path('actNovICBC', views.novICBC, name='herramientas_actualizar_novedades_icbc'),
    path('uploadImg', views.ImageUploadView.as_view(), name='herramientas_upload_img'),
    path('success', views.upload_success, name='herramientas_upload_success'),
    path('importartvtex', views.import_art_vtex, name='herramientas_importar_articulos_vtex'),
    # --- Categorías ---
    path('categorias/list', views.categoria_list, name='herramientas_categoria_list'),
    path('categorias/create', views.categoria_create, name='herramientas_categoria_create'),
    path('categorias/update/<int:id_categoria>', views.categoria_update, name='herramientas_categoria_update'),
    path('categorias/delete/<int:id_categoria>', views.categoria_delete, name='herramientas_categoria_delete'),
    # --- Subcategorías ---
    path('subcategorias/list', views.subcategoria_list, name='herramientas_subcategoria_list'),
    path('subcategorias/create', views.subcategoria_create, name='herramientas_subcategoria_create'),
    path('subcategorias/update/<int:id_subcategoria>', views.subcategoria_update, name='herramientas_subcategoria_update'),
    path('subcategorias/delete/<int:id_subcategoria>', views.subcategoria_delete, name='herramientas_subcategoria_delete'),
    # --- Relaciones ---
    path('relaciones/list', views.relacion_list, name='herramientas_relacion_list'),
    path('relaciones/create', views.relacion_create, name='herramientas_relacion_create'),
     path('relaciones/update/<str:id_categoria_tango>/<int:id_subcategoria>', views.relacion_update, name='herramientas_relacion_update'),
    path('relaciones/delete/<str:id_categoria_tango>/<int:id_subcategoria>', views.relacion_delete, name='herramientas_relacion_delete'),
    # Gerencia
    path('rendircobranzas/<str:UserName>', views.rendircobranzas, name='herramientas_rendir_cobranzas'),
    path('GestionarCobro/<str:UserName>', views.GestionarCobro, name='herramientas_gestionar_cobro'),
    # path('RegistrarEfectivo/<str:UserName>', views.RegistrarEfectivo, name='herramientas_registrar_efectivo'),
    path('gestionPremiosComercial', views.gestionPremiosComercial, name='herramientas_gestion_premios_comercial'),
    # Administracion
    path('ControlGastosSupervision', views.ControlGastosSupervision, name='herramientas_control_gastos_supervision'),
    path('Controlgastos', views.Controlgastos, name='herramientas_control_gastos'),
    path('Cargargastos', views.Cargargastos, name='herramientas_cargar_gastos'),
    path('Controlcajasdiario', views.Controlcajasdiario, name='herramientas_control_cajas_diario'),
    path('GestionDeAlquileres', views.GestionDeAlquileres, name='herramientas_gestion_alquileres'),
    path('CargaGastosAlquileres', views.CargaGastosAlquileres, name='herramientas_carga_gastos_alquileres'),
    path('ControlEgresosDeCaja/<str:UserName>', views.ControlEgresosDeCaja, name='herramientas_control_egresos_caja'),
    path('ControlMasivoCobranza', views.ControlMasivoCobranza, name='herramientas_control_masivo_cobranza'),
    path('CargarContratosDeAlquiler', views.CargarContratosDeAlquiler, name='herramientas_cargar_contratos_alquiler'),
    path('RelacionesCtaCont', views.RelacionesCtaCont, name='herramientas_relaciones_cuenta_contable'),
    path('ContratosFrCarga', views.CargaContratosFr, name='herramientas_carga_contratos_franquicias'),
    path('CargaFacturasSuc', views.CargaFacturasSuc, name='herramientas_carga_facturas_sucursales'),
    path('EgresosCajaTesoreria', views.EgresosCajaTesoreria, name='herramientas_egresos_caja_tesoreria'),
    path('GestionDeProveedores',views.GestionDeProveedores, name='herramientas_gestion_proveedores'),
    path('MedidasLocales', views.MedidasLocales, name='herramientas_medidas_locales'),
    path('VentasLocatarios', views.VentasLocatarios, name='herramientas_ventas_locatarios'),
    path('FacturasDirectores', views.FacturasDirectores, name='herramientas_facturas_directores'),
    path('RegistroPagoServicios', views.RegistroPagoServicios, name='herramientas_registro_pago_servicios'),


    # Administracion_CE             ***Comercio Exterior***
    path('Cargarcontenedor', views.Cargarcontenedor, name='herramientas_cargar_contenedor'),
    path('EditarContenedor', views.EditarContenedor, name='herramientas_editar_contenedor'),

    # RRHH
    # path('adminEmpleados', views.adminEmpleados, name='herramientas_admin_empleados'),
    path('altaVendedores', views.altaVendedores, name='herramientas_alta_vendedores'),
    path('grupoVendedores', views.listarGrupos, name='herramientas_listar_grupos'),
    path('gestionarVendedores', views.gestionarVendedores, name='herramientas_gestionar_vendedores'),
    path('cargaAnticipo', views.CargaAnticipo, name='herramientas_carga_anticipo'),

    # Tesoreria
    path('ControlDeEfectivo', views.ControlDeEfectivo, name='herramientas_control_efectivo'),
    path('PagosDirectores', views.PagosDirectores, name='herramientas_pagos_directores'),

    # Supervisores
     path('CargaProyecto', views.CargaProyecto, name='carga_proyecto'),

    # Admin
    path('AdminNotificaciones', views.AdminNotificaciones, name='herramientas_admin_notificaciones'),

    # --- URLs for views moved from viewsExtras.py ---
    path('import_file_etiquetas', views.import_file_etiquetas, name='herramientas_import_file_etiquetas'),
    path('import_file_cierrePedidos', views.import_file_cierrePedidos, name='herramientas_import_file_cierre_pedidos'),
    path('import_file_cierrePedidosUY', views.import_file_cierrePedidosUY, name='herramientas_import_file_cierre_pedidos_uy'),
    path('import_file_ubi', views.import_file_ubi, name='herramientas_import_file_ubi'),

    # EB_sincArt_volumen - URLs específicas PRIMERO (antes de las dinámicas)
    path('eb-sinc-art-volumen/', views.eb_sinc_art_volumen_list, name='eb_sinc_art_volumen_list'),
    # Excel URLs específicas
    path('eb-sinc-art-volumen/descargar-plantilla/', views.eb_sinc_art_volumen_descargar_plantilla, name='eb_sinc_art_volumen_descargar_plantilla'),
    path('eb-sinc-art-volumen/carga-masiva/', views.eb_sinc_art_volumen_carga_masiva, name='eb_sinc_art_volumen_carga_masiva'),
    path('eb-sinc-art-volumen/carga-masiva/form/', views.eb_sinc_art_volumen_carga_masiva_form, name='eb_sinc_art_volumen_carga_masiva_form'),
    # URLs dinámicas DESPUÉS
    path('eb-sinc-art-volumen/<str:cod_articulo>/', views.eb_sinc_art_volumen_detail, name='eb_sinc_art_volumen_detail'),
    path('eb-sinc-art-volumen/<str:cod_articulo>/edit/', views.eb_sinc_art_volumen_edit, name='eb_sinc_art_volumen_edit'),
    path('eb-sinc-art-volumen/<str:cod_articulo>/delete/', views.eb_sinc_art_volumen_delete, name='eb_sinc_art_volumen_delete'),
    
    # Vista de prueba para Excel
    path('test-excel/', views.test_excel_download, name='test_excel_download'),
    path('test-plantilla-step/', views.test_plantilla_step_by_step, name='test_plantilla_step'),
    path('test-plantilla-simple/', views.test_plantilla_simplificada, name='test_plantilla_simple'),
    
    # URL alternativa para plantilla
    path('plantilla-download/', views.eb_sinc_art_volumen_descargar_plantilla, name='plantilla_download_alt'),

    # Gestión de Sucursales E-commerce
    path('gestion-sucursales-ecommerce/', views.gestion_sucursales_ecommerce, name='gestion_sucursales_ecommerce'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
