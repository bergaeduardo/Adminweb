# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "Herramientas"
urlpatterns = [
    # Logistica
    
    path("Calendario/TurnoListView", views.Listar_turno, name="Herramientas"),
    path('Calendario/NuevoTurnoProveedor', views.Crear_turno, name='Herramientas'),
    path('Calendario/EditarTurnoProveedor/<int:IdTurno>', views.Editar_Turno, name='Herramientas'),
    path('Gestion_cronograma', views.Gestion_cronograma, name='Herramientas'),
    path('Gestion_guias_mayoristas', views.Gestion_guias_mayoristas, name='Herramientas'),
    path('registro', views.registro_turno, name='registro_turno'),
    path('get_nombre_proveedor', views.get_nombre_proveedor, name='get_nombre_proveedor'),
    path('listado', views.listado_turnos, name='listado_turnos'),
    path('eliminar/<int:turno_id>', views.eliminar_turno, name='eliminar_turno'),
    path('ver/<int:turno_id>', views.ver_turno, name='ver_turno'),
    path('editar/<int:turno_id>', views.editar_turno, name='editar_turno'),
    # Abastecimiento
    path('Stock_excluido', views.Stock_excluido, name='Herramientas'),
    path('Carga_de_orden', views.Carga_de_orden, name='Herramientas'),
    path('Activar_orden', views.Activar_orden, name='Herramientas'),
    path('Desactivar_orden', views.Desactivar_orden, name='Herramientas'),
    path('Recodificacion', views.Recodificacion, name='Herramientas'),
    path('AltaPromoBancaria', views.AltaPromoBancaria, name='Herramientas'),
    path('CrearGrupoPromo', views.CrearGrupoPromo, name='Herramientas'),
    path('EditarGrupoPromo', views.EditarGrupoPromo, name='Herramientas'),
    # Comercial
    path('Ventas_sucursales', views.Ventas_sucursales, name='Herramientas'),
    path('GestionCategoriaProductos', views.Gestion_categoria_productos, name='Herramientas'),
    path('AdministrarCuotas', views.AdministrarCuotas, name='Herramientas'),
    path('AdministrarInternos', views.AdministrarInternos, name='Herramientas'),
    # Mayoristas
    path('Adm_Pedido', views.Adm_Pedido, name='Herramientas'),
    # Ecommerce
    path('Control_pedidos', views.Control_pedidos, name='Herramientas'),
    path('StockSegVtex', views.StockSegVtex, name='Herramientas'),
    path('actNovICBC', views.novICBC, name='Herramientas'),
    path('uploadImg', views.ImageUploadView.as_view(), name='uploadImg'),
    path('success', views.upload_success, name='upload_success'),
    path('importartvtex', views.import_art_vtex, name='importartvtex'),
    # --- Categorías ---
    path('categorias/list', views.categoria_list, name='categoria_list'),
    path('categorias/create', views.categoria_create, name='categoria_create'),
    path('categorias/update/<int:id_categoria>', views.categoria_update, name='categoria_update'),
    path('categorias/delete/<int:id_categoria>', views.categoria_delete, name='categoria_delete'),
    # --- Subcategorías ---
    path('subcategorias/list', views.subcategoria_list, name='subcategoria_list'),
    path('subcategorias/create', views.subcategoria_create, name='subcategoria_create'),
    path('subcategorias/update/<int:id_subcategoria>', views.subcategoria_update, name='subcategoria_update'),
    path('subcategorias/delete/<int:id_subcategoria>', views.subcategoria_delete, name='subcategoria_delete'),
    # --- Relaciones ---
    path('relaciones/list', views.relacion_list, name='relacion_list'),
    path('relaciones/create', views.relacion_create, name='relacion_create'),
     path('relaciones/update/<str:id_categoria_tango>/<int:id_subcategoria>', views.relacion_update, name='relacion_update'),
    path('relaciones/delete/<str:id_categoria_tango>/<int:id_subcategoria>', views.relacion_delete, name='relacion_delete'),
    # Gerencia
    path('rendircobranzas/<str:UserName>', views.rendircobranzas, name='Herramientas'),
    path('GestionarCobro/<str:UserName>', views.GestionarCobro, name='Herramientas'),
    path('RegistrarEfectivo/<str:UserName>', views.RegistrarEfectivo, name='Herramientas'),
    path('gestionPremiosComercial', views.gestionPremiosComercial, name='Herramientas'),
    # Administracion
    path('ControlGastosSupervision', views.ControlGastosSupervision, name='Herramientas'),
    path('Controlgastos', views.Controlgastos, name='Herramientas'),
    path('Cargargastos', views.Cargargastos, name='Herramientas'),
    path('Controlcajasdiario', views.Controlcajasdiario, name='Herramientas'),
    path('GestionDeAlquileres', views.GestionDeAlquileres, name='Herramientas'),
    path('CargaGastosAlquileres', views.CargaGastosAlquileres, name='Herramientas'),
    path('ControlEgresosDeCaja/<str:UserName>', views.ControlEgresosDeCaja, name='Herramientas'),
    path('ControlMasivoCobranza', views.ControlMasivoCobranza, name='Herramientas'),
    path('CargarContratosDeAlquiler', views.CargarContratosDeAlquiler, name='Herramientas'),
    path('RelacionesCtaCont', views.RelacionesCtaCont, name='Herramientas'),
    path('ContratosFrCarga', views.CargaContratosFr, name='Herramientas'),
    path('CargaFacturasSuc', views.CargaFacturasSuc, name='Herramientas'),
    path('EgresosCajaTesoreria', views.EgresosCajaTesoreria, name='Herramientas'),

    # Administracion_CE             ***Comercio Exterior***
    path('Cargarcontenedor', views.Cargarcontenedor, name='Herramientas'),
    path('EditarContenedor', views.EditarContenedor, name='Herramientas'),

    # RRHH
    path('adminEmpleados', views.adminEmpleados, name='Herramientas'),
    path('altaVendedores', views.altaVendedores, name='Herramientas'),
    path('grupoVendedores', views.listarGrupos, name='Herramientas'),
    path('gestionarVendedores', views.gestionarVendedores, name='Herramientas'),

    # Tesoreria
    path('ControlDeEfectivo', views.ControlDeEfectivo, name='Herramientas'),


]

if settings.DEBUG:   
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
