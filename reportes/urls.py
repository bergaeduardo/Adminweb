# -*- encoding: utf-8 -*-

from django.urls import path
from apps.home import views as viewsApp
from . import views

app_name = "reportes"
urlpatterns = [
    # RRHH
    path('RRHH/reporteAnticipos', views.reporteAnticipos, name='reportes_rrhh_anticipos'),
    path('RRHH/gestionClientes', views.gestionClientes, name='reportes_rrhh_gestion_clientes'),

    # Logistica
    path('Logistica/stockcentral', views.stockcentral, name='reportes_logistica_stockcentral'),
    path('Logistica/stockcUY', views.stockcUY, name='reportes_logistica_stock_cuy'),
    path('Logistica/pendiente_despacho', views.Pedidos_pendiente_despacho, name='reportes_logistica_pedidos_pendiente_despacho'),
    path('Logistica/MovimientosWms', views.MovimientosWms, name='reportes_logistica_movimientos_wms'),
    path('Logistica/ConsultaDestino', views.ConsultaDestino, name='reportes_logistica_consulta_destino'),

    # Abastecimiento
    path('Abastecimiento/Auditoria_orden', views.Auditoria_orden, name='reportes_abastecimiento_auditoria_orden'),
    path('Abastecimiento/CategoriasDeProductos', views.CategoriasDeProductos, name='reportes_abastecimiento_categorias_productos'),
    path('Abastecimiento/HRecodificaciones', views.HRecodificaciones, name='reportes_abastecimiento_historial_recodificaciones'),
    path('Abastecimiento/Eficiencia_pedidos', views.Eficiencia_pedidos, name='reportes_abastecimiento_eficiencia_pedidos'),
    path('Abastecimiento/stockSupply', views.stockcentral_pivot, name='reportes_logistica_stock_supply'),
    path('Abastecimiento/stockSupplyUY', views.stockcentral_pivotUY, name='reportes_logistica_stock_supply_uy'),
    path('Abastecimiento/AnalisisProductos', views.AnalisisProductos, name='reportes_comercial_analisis_productos'),

    # Comercial
    path('Comercial/stockSucursalesLakers', views.stockSucursalesLakers, name='reportes_comercial_stock_sucursales_lakers'),
    path('Comercial/Stock_Suc_Articulos', views.Stock_Sucursales, name='reportes_comercial_stock_sucursales_articulos'),
    path('Comercial/stockSucursalesTasky', views.stockSucursalesTasky, name='reportes_comercial_stock_sucursales_tasky'),
    path('Comercial/VentasXcanal', views.VentasXcanal, name='reportes_comercial_ventas_por_canal'),
    # path('Comercial/AdmEmpleados', views.AdmEmpleados, name='reportes_comercial_adm_empleados'),
    path('Comercial/compararStock/', views.compararStock, name='reportes_comercial_comparar_stock'),
    path('Comercial/compararVentas/', views.compararVentas, name='reportes_comercial_comparar_ventas'),
    path('Comercial/PresupuestoComercial/', views.PresupuestoComercial, name='reportes_comercial_presupuesto_comercial'),
    path('Comercial/auditoriaDiferenciaPrecio/', views.auditoriaDiferenciaPrecio, name='reportes_comercial_auditoria_diferencia_precio'),

    # Mayoristas
    path('Mayoristas/Tracking_pedidos_mayoristas', views.Tracking_pedidos_mayoristas, name='reportes_mayoristas_tracking_pedidos_mayoristas'),

    # Ecommerce
    path('Ecommerce/stock_ecommerce', views.stockcentral_ecommerce, name='reportes_ecommerce_stock_ecommerce'),
    path('Ecommerce/Tracking_Ecommerce', views.Tracking_Ecommerce, name='reportes_ecommerce_tracking_ecommerce'),
    path('Ecommerce/stockUY_ecommerce', views.stockUY_ecommerce, name='reportes_ecommerce_stock_uy_ecommerce'),
    path('Ecommerce/Pedidos', views.Pedidos, name='reportes_ecommerce_pedidos'),
    path('Ecommerce/PedidosUY', views.PedidosUY, name='reportes_ecommerce_pedidos_uy'),
    path('Ecommerce/Auditoria_Ecommerce', views.Auditoria_Ecommerce, name='reportes_ecommerce_auditoria_ecommerce'),
    path('Ecommerce/Auditoria_Prisma', views.Auditoria_Prisma, name='reportes_ecommerce_auditoria_prisma'),
    path('Ecommerce/Segmentacion_clientes', views.Segmentacion_clientes, name='reportes_ecommerce_segmentacion_clientes'),
    path('Ecommerce/TableroDeControl', views.TableroDeControl, name='reportes_ecommerce_tablero_control'),

    # Gerencia
    # Note: Paths with parameters like <str:UserName> require careful handling in template checks
    path('Gerencia/DetalleRemitos599/<str:UserName>', views.DetalleRemitos599, name='reportes_gerencia_detalle_remitos_599'),
    path('Gerencia/ChequesRecibidos/<str:UserName>', views.ChequesRecibidos, name='reportes_gerencia_cheques_recibidos'),

    # Administracion
    path('Administracion/VentasXmedio_pago', views.VentasXmedio_pago, name='reportes_administracion_ventas_por_medio_pago'),
    path('Administracion/Consultagastos', views.Consultagastos, name='reportes_administracion_consulta_gastos'),
    path('Administracion/integridadVentas', views.integridadVentas, name='reportes_administracion_integridad_ventas'),
    path('Administracion/Controlcajasmensual', views.Controlcajasmensual, name='reportes_administracion_control_cajas_mensual'),
    path('Administracion/CargaGastosTesoreria', views.CargaGastosTesoreria, name='reportes_administracion_carga_gastos_tesoreria'),
    path('Administracion/DetalleContratosDeAlquiler', views.DetalleContratosDeAlquiler, name='reportes_administracion_detalle_contratos_alquiler'),
    path('Administracion/FacturaManualLista', viewsApp.facturas_por_fecha, name='reportes_administracion_factura_manual_lista'), # View not found in source
    path('Administracion/ContratosFranquicias', views.ContratosFranquicias, name='reportes_administracion_contratos_franquicias'),
    path('Administracion/GastosSupervision', views.GastosSupervision, name='reportes_administracion_gastos_supervision'),
    path('Administracion/controlVentasSucursales', views.controlVentasSucursales, name='reportes_administracion_control_ventas_sucursales'),
    path('Administracion/saldoCaja', views.saldoCaja, name='saldo_caja_tesoreria'),
    path('Administracion/costoOcupacion', views.costoOcupacion, name='costo_ocupacion'),
    path('Administracion/cuentasParticulares', views.cuentasParticulares, name='cuentas_particulares'),

    # Supervisores
    path('Supervisores/Proyectos', views.Proyectos, name='reportes_supervisores_proyectos'),

    # Handle the root /Reportes/ path if needed, maybe redirect or show a landing page
    # path('', views.reportes_index, name='reportes_index'), # Example: add a view for the root
]
