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
    path('Calendario/EditarTurnoProveedor/<int:IdTurno>', views.Editar_Turno, name='herramientas_editar_turno'),
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
    path("cargaAnticipoGrupo", views.CargaAnticipoGrupo, name="herramientas_carga_anticipo_grupo"),
    path("ImpRotulos", views.ImpRotulos, name="herramientas_imprimir_rotulos"),
    path("ImpRemEcom", views.ImpRemEcom, name="herramientas_importar_rem_ecom"),
    path("ImprimirEtiquetasBultos", views.ImprimirEtiquetasBultos, name="herramientas_imprimir_etiquetas_bultos"),

    # Abastecimiento
    path('Stock_excluido', views.Stock_excluido, name='herramientas_stock_excluido'),
    path('Carga_de_orden', views.Carga_de_orden, name='herramientas_carga_orden'),
    path('Activar_orden', views.Activar_orden, name='herramientas_activar_orden'),
    path('Desactivar_orden', views.Desactivar_orden, name='herramientas_desactivar_orden'),
    path('Recodificacion', views.Recodificacion, name='herramientas_recodificacion'),
    path('AltaPromoBancaria', views.AltaPromoBancaria, name='herramientas_alta_promo_bancaria'),
    path('CrearGrupoPromo', views.CrearGrupoPromo, name='herramientas_crear_grupo_promo'),
    path('EditarGrupoPromo', views.EditarGrupoPromo, name='herramientas_editar_grupo_promo'),
    path('MaestroDestinos', views.MaestroDestinos, name='herramientas_maestro_destinos'),
    path('GestionEquivalentes', views.GestionEquivalentes, name='herramientas_gestion_equivalentes'),
    # Comercial
    path('GestionCategoriaProductos', views.Gestion_categoria_productos, name='herramientas_gestion_categoria_productos'),
    path('AdministrarCuotas', views.AdministrarCuotas, name='herramientas_administrar_cuotas'),
    path('AdministrarInternos', views.AdministrarInternos, name='herramientas_administrar_internos'),
    path('PromoBancos', views.PromoBancos, name='herramientas_promo_bancos'),
    path('AltaNuevosLocales', views.AltaNuevosLocales, name='herramientas_alta_nuevos_locales'),
    path('UsuariosFranquicias', views.UsuariosFranquicias, name='herramientas_usuarios_franquicias'),
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
    path('RegistrarEfectivo/<str:UserName>', views.RegistrarEfectivo, name='herramientas_registrar_efectivo'),
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

    # Administracion_CE             ***Comercio Exterior***
    path('Cargarcontenedor', views.Cargarcontenedor, name='herramientas_cargar_contenedor'),
    path('EditarContenedor', views.EditarContenedor, name='herramientas_editar_contenedor'),

    # RRHH
    path('adminEmpleados', views.adminEmpleados, name='herramientas_admin_empleados'),
    path('altaVendedores', views.altaVendedores, name='herramientas_alta_vendedores'),
    path('grupoVendedores', views.listarGrupos, name='herramientas_listar_grupos'),
    path('gestionarVendedores', views.gestionarVendedores, name='herramientas_gestionar_vendedores'),
    path('cargaAnticipo', views.CargaAnticipo, name='herramientas_carga_anticipo'),

    # Tesoreria
    path('ControlDeEfectivo', views.ControlDeEfectivo, name='herramientas_control_efectivo'),

    # Supervisores
     path('CargaProyecto', views.CargaProyecto, name='carga_proyecto'),

    # --- URLs for views moved from viewsExtras.py ---
    path('import_file_etiquetas', views.import_file_etiquetas, name='herramientas_import_file_etiquetas'),
    path('import_file_cierrePedidos', views.import_file_cierrePedidos, name='herramientas_import_file_cierre_pedidos'),
    path('import_file_cierrePedidosUY', views.import_file_cierrePedidosUY, name='herramientas_import_file_cierre_pedidos_uy'),
    path('import_file_ubi', views.import_file_ubi, name='herramientas_import_file_ubi'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
