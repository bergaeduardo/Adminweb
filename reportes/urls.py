# -*- encoding: utf-8 -*-

from django.urls import path
from apps.home import views as viewsApp
from . import views

app_name = "reportes"
urlpatterns = [
        # RRHH
            path('AsistenciasSuc', views.AsistenciasSuc, name='reportes_asistencias_suc'),
            path('reporteAnticipos', views.reporteAnticipos, name='reportes_anticipos'),
        # Logistica
            path('stockcentral', views.stockcentral, name='reportes_stockcentral'),
            path('stockcUY', views.stockcUY, name='reportes_stock_cuy'),
            path('stockSupply', views.stockcentral_pivot, name='reportes_stock_supply'),
            path('stockSupplyUY', views.stockcentral_pivotUY, name='reportes_stock_supply_uy'),
            path('pendiente_despacho', views.Pedidos_pendiente_despacho, name='reportes_pedidos_pendiente_despacho'),
            path('MovimientosWms', views.MovimientosWms, name='reportes_movimientos_wms'),
            path('ConsultaDestino', views.ConsultaDestino, name='reportes_consulta_destino'),
        # Abastecimiento
            path('Auditoria_orden', views.Auditoria_orden, name='reportes_auditoria_orden'),
            path('CategoriasDeProductos', views.CategoriasDeProductos, name='reportes_categorias_productos'),
            path('HRecodificaciones', views.HRecodificaciones, name='reportes_historial_recodificaciones'),
            path('Eficiencia_pedidos', views.Eficiencia_pedidos, name='reportes_eficiencia_pedidos'),
            path('promocionesActivas', views.promocionesActivas, name='reportes_promociones_activas'),
        # Comercial
            path('stockSucursalesLakers', views.stockSucursalesLakers, name='reportes_stock_sucursales_lakers'),
            path('Stock_Suc_Articulos', views.Stock_Sucursales, name='reportes_stock_sucursales_articulos'),
            path('stockSucursalesTasky', views.stockSucursalesTasky, name='reportes_stock_sucursales_tasky'),
            path('VentasXcanal', views.VentasXcanal, name='reportes_ventas_por_canal'),
            path('AdmEmpleados', views.AdmEmpleados, name='reportes_adm_empleados'),
            path('AnalisisProductos', views.AnalisisProductos, name='reportes_analisis_productos'),
        # Mayoristas
            path('Tracking_pedidos_mayoristas', views.Tracking_pedidos_mayoristas, name='reportes_tracking_pedidos_mayoristas'),
        # Ecommerce
            path('stock_ecommerce', views.stockcentral_ecommerce, name='reportes_stock_ecommerce'),
            path('Tracking_Ecommerce', views.Tracking_Ecommerce, name='reportes_tracking_ecommerce'),
            path('stockUY_ecommerce', views.stockUY_ecommerce, name='reportes_stock_uy_ecommerce'),
            path('Pedidos', views.Pedidos, name='reportes_pedidos'),
            path('PedidosUY', views.PedidosUY, name='reportes_pedidos_uy'),
            path('Auditoria_Ecommerce', views.Auditoria_Ecommerce, name='reportes_auditoria_ecommerce'),
            path('Auditoria_Prisma', views.Auditoria_Prisma, name='reportes_auditoria_prisma'),
            path('Segmentacion_clientes', views.Segmentacion_clientes, name='reportes_segmentacion_clientes'),
            path('TableroDeControl', views.TableroDeControl, name='reportes_tablero_control'),
        # Gerencia
            path('DetalleRemitos599/<str:UserName>', views.DetalleRemitos599, name='reportes_detalle_remitos_599'),
            path('ChequesRecibidos/<str:UserName>', views.ChequesRecibidos, name='reportes_cheques_recibidos'),
        # Administracion
            path('VentasXmedio_pago', views.VentasXmedio_pago, name='reportes_ventas_por_medio_pago'),
            path('Consultagastos', views.Consultagastos, name='reportes_consulta_gastos'),
            path('VentaVscobranza', views.VentaVscobranza, name='reportes_venta_vs_cobranza'),
            path('Controlcajasmensual', views.Controlcajasmensual, name='reportes_control_cajas_mensual'),
            path('ResumenMensualAlquileres', views.ResumenMensualAlquileres, name='reportes_resumen_mensual_alquileres'),
            path('CargaGastosTesoreria', views.CargaGastosTesoreria, name='reportes_carga_gastos_tesoreria'),
            path('DetalleContratosDeAlquiler', views.DetalleContratosDeAlquiler, name='reportes_detalle_contratos_alquiler'),
            path('FacturaManualLista', viewsApp.facturas_por_fecha, name='reportes_factura_manual_lista'), # View not found in source
            path('ContratosFranquicias', views.ContratosFranquicias, name='reportes_contratos_franquicias'),
            path('GastosSupervision', views.GastosSupervision, name='reportes_gastos_supervision'),
        # Supervisores
            path('Proyectos', views.Proyectos, name='reportes_proyectos'),
]
