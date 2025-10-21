SERVIDOR = {
    'testing': 'http://192.168.0.233:8080/',
    'production': 'https://app.xl.com.ar/',
}
DIR_PBI = {
    # Logistica
    'Kpis_Logistica':'https://app.powerbi.com/view?r=eyJrIjoiNTYxZDFlNGEtZTFiNy00ODM1LTk5NzYtZTg3NDljYTM3ZmVhIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    # Abastecimiento
    # Comercial
    'Promociones':'https://app.powerbi.com/view?r=eyJrIjoiZTRlYWQ0Y2YtZjIwYi00Y2Y5LWFiOGMtZTcxOGU1ZjQ5Zjg5IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Inventarios_Sucursales':'https://app.powerbi.com/view?r=eyJrIjoiMTc3MzY1ZjMtMGNlNS00YTJjLWJkM2ItYmRkM2ZlZTE3NTNkIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Conteos':'https://app.powerbi.com/view?r=eyJrIjoiMDYxYzNkNjYtZjg0NS00ODFmLWJmN2MtYTA5MTQzNTMxMDAwIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Geodatos':'https://app.powerbi.com/view?r=eyJrIjoiMjA3OGM2MGItYmEzYy00ZWZmLTk4NDYtMzMwNWIzZDk3ZTI3IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Notas_de_credito':'https://app.powerbi.com/view?r=eyJrIjoiYzRjNzY0MGItZDk0MC00NWIyLWI5NmItYzcxYjhhMzA4MTQ3IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Ventas_Franquicias':'https://app.powerbi.com/view?r=eyJrIjoiMDBiN2Q3ZjItNTcyOS00YTAwLWE4YjgtN2JkMTQ1MGM0NjI3IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Ventas_Sucursales':'https://app.powerbi.com/view?r=eyJrIjoiMjYyY2YwZTAtNGY4OC00YzM4LTkzYTktYTU5YTM2OWIzMjRjIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Ventas_SucursalesUY':'https://app.powerbi.com/view?r=eyJrIjoiOTNjMGFlOTUtM2Q4MS00YTg1LWJmNDItMjg4NzAxNmFjODg5IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Velocidad_de_Ventas':'https://app.powerbi.com/view?r=eyJrIjoiMWJiNDk5ZDAtYzFkYy00OWRmLTk1OTYtMDIxNWU2MTllNmEzIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    # Mayoristas
    'Ventas_Mayoristas':'https://app.powerbi.com/view?r=eyJrIjoiMzcwMDA2ZGItMTFkZS00MThiLWI2N2EtYWFiODY5YzYzYTA0IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    # Ecommerce
    'Ventas_Ecommerce':'https://app.powerbi.com/view?r=eyJrIjoiNmUyZDQyNjctZWJlOC00YWFkLWEwMDYtZjYwODRiZmIyMDNmIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'Kpis_Ecommerce':'https://app.powerbi.com/view?r=eyJrIjoiMWQyMDA5ZDMtNjRjMi00NWU4LTlhZDgtYzZhY2E0ZTE0YTE3IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    'PromocionesEcommerce':'https://app.powerbi.com/view?r=eyJrIjoiN2VlNWMyMzgtMWMyMC00NmJhLThiMDUtZDA1YjI2MzBjZjg5IiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',
    # Gerencia
    'PremiosComercial':'https://app.powerbi.com/view?r=eyJrIjoiOTI3NmI1MzMtNTU3MC00NDc0LThhMjktMzA2ZTA1OTA3NThlIiwidCI6IjQ0Y2E2MmNkLTY4MjItNDZkNC05NTUxLTEzNDQ5N2ZmM2VjMiIsImMiOjR9',

    }

DIR_REPORTES = {
    # Logistica
    'Pedidos_pendiente_despacho':SERVIDOR['production'] + 'sistemas/cronoDespacho/pedidos.php',
    'ConsultaDestino':SERVIDOR['production'] + 'sistemas/maestroDestinos/indexMob.php',
    # Abastecimiento
    'Auditoria_orden': SERVIDOR['production']  + 'sistemas/distriCuero/listOrdenesComercial.php',
    'CategoriasDeProductos':SERVIDOR['production']  + 'comercial/producto/consultaCategoriaProductos.php',
    'HRecodificaciones':SERVIDOR['production']  + 'recodificacion/historialDeRecodificaciones.php',
    'Eficiencia_pedidos': SERVIDOR['production']  + 'comercial/abastecimiento/pedidos/eficienciaPedidos.php',
    # Comercial
    'Stock_Sucursales': SERVIDOR['production']  + 'sistemas/stockYprecios/stockDepositos.php',
    'Stock_central': SERVIDOR['production']  + 'logistica/stock.php',
    'promocionesActivas': SERVIDOR['production']  + 'comercial/mayoristas/promocionesBancarias/promocionesActivas.php',
    'VentasXcanal':SERVIDOR['production']  + 'comercial/abastecimiento/ventasAbastecimiento/',
    # 'AdmEmpleados':SERVIDOR['production']  + 'administracion/recursosHumanos/controlHorarios/verControlHorario.php',
    'AnalisisProductos':SERVIDOR['production']  + 'comercial/abastecimiento/analisisProducto/listado.php',
    'compararStock':SERVIDOR['production']  + 'controlGestion/compararStock/',
    'compararVentas':SERVIDOR['production']  + 'controlGestion/compararVentas/',
    'PresupuestoComercial':'https://192.168.0.13:3000/home/',
    # Mayoristas
    'Tracking_pedidos_mayoristas': SERVIDOR['production']  + 'comercial/mayoristas/despacho/tracking.php',
    # Ecommerce
    'Pedidos': SERVIDOR['production'] + 'ECOMMERCE/',
    'Tracking_Ecommerce':SERVIDOR['production'] + 'ecommerce/seguimientoPedidos/',
    'PedidosUY': SERVIDOR['production'] + 'Uruguay/ecommerce/consultaPedidos.php',
    'Auditoria_Ecommerce': SERVIDOR['production'] + 'ecommerce-auditoria/',
    'Auditoria_Prisma': SERVIDOR['production'] + 'ecommerce/auditoriaPrisma/auditoriaPrisma.php',
    'Segmentacion_clientes':SERVIDOR['production'] + 'ecommerce/segmentacion/segmentacionDeClientes.php',
    'TableroDeControl':SERVIDOR['production'] + 'ecommerce/tableroControl/index.php',
    # Administracion
    'VentasXmedio_pago':SERVIDOR['production'] + 'administracion/controlSucursales/resumenVentas.php',
    'consultaGastos':SERVIDOR['production'] + 'administracion/contabilidad/consultaGastos.php',
    'ventaVsCobranza':SERVIDOR['production'] + 'administracion/controlSucursales/ventaVsCobranza.php',
    'Controlcajasmensual':SERVIDOR['production'] + 'administracion/controlSucursales/controlMensualCajaSucursales.php',
    'ResumenMensualAlquileres':SERVIDOR['production'] + 'administracion/impuestos/alquileres/consultaAlquileres.php',
    'CargaGastosTesoreria':SERVIDOR['production'] + 'administracion/controlSucursales/cargaGastosTesoreria.php',
    'DetalleContratosDeAlquiler':SERVIDOR['production'] + 'administracion/impuestos/alquileres/detalleContratosAlquiler.php',
    'ContratosFranquicias':SERVIDOR['production'] + 'administracion/impuestos/alquileresFranquicias/detalleContratosAlquiler.php',
    'GastosSupervision':SERVIDOR['production'] + 'comercial/supervision/presupuesto/dashboard.php',
    'controlVentasSucursales':SERVIDOR['production'] + 'administracion/controlSucursales/controlVentasSucursales.php',
    'saldoCaja':SERVIDOR['production'] + 'administracion/tesoreria/saldoCaja.php',
    'costoOcupacion':SERVIDOR['production'] + 'administracion/impuestos/alquileres/costoOcupacion.php',

    # Gerencia
    'DetalleRemitos599':SERVIDOR['production']  + 'sistemas/599/consultaderemitos.php?userName=',
    'ChequesRecibidos':SERVIDOR['production']  + 'sistemas/599/reportedecheques.php?userName=',
    # RRHH
    'AsistenciasSuc':SERVIDOR['production'] + 'sistemas/fichaje/reporteDeAsistencias.php',
    'ReporteAnticipos':SERVIDOR['production'] + 'administracion/recursosHumanos/anticipoSueldos/reporteAnticipos.php',
    'gestionClientes':SERVIDOR['production'] + 'recursosHumanos/clientes/index.php',
    # Supervisores
    'Proyectos':SERVIDOR['production'] + 'projects/adminProyectos/index.php',

}

DIR_HERAMIENTAS = {
    # Logistica
    'Gestion_cronograma': SERVIDOR['production'] + 'sistemas/cronoDespacho/index.php',
    'Gestion_guias_mayoristas': SERVIDOR['production'] + 'comercial/mayoristas/despacho/index.php',
    'ImpRotulos': SERVIDOR['production'] + 'remapp/index.html',
    'ImportarRemEcommerce': SERVIDOR['production'] + 'ecommerce/abastecimiento/',
    'ImprimirEtiquetasBultos': SERVIDOR['production']  + 'logistica/etiquetas/',
    'RemisionMasiva': SERVIDOR['production']  + 'logistica/remisionMasiva/',
    # Abastecimiento
    'Stock_excluido': SERVIDOR['production']  + 'comercial/abastecimiento/stockExcluido/index.php',
    'Carga_de_orden': SERVIDOR['production']  + 'sistemas/distriCuero/index.php',
    'Activar_orden': SERVIDOR['production']  + 'sistemas/distriCuero/activaOrdenes.php',
    'Desactivar_orden': SERVIDOR['production']  + 'sistemas/distriCuero/desactivaOrdenes.php',
    'Recodificacion': SERVIDOR['production']  + 'recodificacion/nuevoProceso.php',
    'AltaPromoBancaria':SERVIDOR['production']  + 'comercial/mayoristas/promocionesBancarias/altaPromoBancaria.php',
    'CrearGrupoPromo':SERVIDOR['production']  + 'comercial/mayoristas/promocionesBancarias/crearGrupoPromo.php',
    'EditarGrupoPromo':SERVIDOR['production']  + 'comercial/mayoristas/promocionesBancarias/listarGruposPromo.php',
    'MaestroDestinos':SERVIDOR['production']  + 'comercial/abastecimiento/destinos/maestroDestinos.php',
    'GestionEquivalentes':SERVIDOR['production']  + 'comercial/abastecimiento/analisisProducto/gestion_equivalencias.php',
    'StockBase':SERVIDOR['production']  + 'comercial/abastecimiento/stock_base/',
    'MedidasLocales':SERVIDOR['production']  + 'comercial/abastecimiento/gestor_locales/',
    # Comercial
    'Gestion_categoria_productos':SERVIDOR['production']  + 'comercial/producto/gestionCategoriaProductos.php',
    'AdministrarCuotas':SERVIDOR['production']  + 'promociones/Cuotas/gestionar.php',
    'AdministrarInternos':SERVIDOR['production']  + 'comercial/recepcion/listado.php',
    'PromoBancos':SERVIDOR['production']  + 'promoBancos/',
    'AltaNuevosLocales':SERVIDOR['production']  + 'app/usuarios',
    'UsuariosFranquicias':SERVIDOR['production']  + 'usuariosFranquicias/',
    'ObjetivosVentaFranquicias':SERVIDOR['production']  + 'comercial/franquicias/objetivosVenta/',
    # Mayoristas
    'Adm_Pedido':SERVIDOR['production']  + 'sistemas/despachoMayorista/index.php',
    # Ecommerce
    'Control_pedidos': SERVIDOR['production'] + 'logistica/ecommerce/',
    'StockSegVtex': SERVIDOR['production'] + 'ecommerce/stockSeguridad/stockSeguridad.php',
    'novICBC':'http://192.168.0.233:8080/',
    # Gerencia
    'rendircobranzas': SERVIDOR['production']  + 'sistemas/599/valoresrendir.php?userName=',
    'gestionarCobro':SERVIDOR['production']  + 'sistemas/599/composicionDeRemitos.php?userName=',
    'registrarEfectivo':SERVIDOR['production']  + 'administracion/controlSucursales/controlRecepcionEfectivo.php?userName=',
    'gestionPremiosComercial':SERVIDOR['production']  + 'comercial/supervision/gestionarPremios.php',
    # Administracion
    'ControlGastosSupervision':SERVIDOR['production'] + 'comercial/supervision/controlarGastos.php',
    'controlGastos':SERVIDOR['production'] + 'administracion/contabilidad/controlGastos.php',
    'cargaGastos':SERVIDOR['production'] + 'administracion/contabilidad/cargaGastos.php',
    'cargaInicial':SERVIDOR['production'] + 'administracion/comercioExterior',
    'mostrarOrden':SERVIDOR['production'] + 'administracion/comercioExterior/mostrarOrden.php',
    'Controlcajasdiario':SERVIDOR['production'] + 'administracion/controlSucursales/controlDiarioCajaSucursales.php',
    'CargaGastosAlquileres':SERVIDOR['production'] + 'administracion/impuestos/alquileres/cargaAlquileres.php',
    'GestionDeAlquileres':SERVIDOR['production'] + 'administracion/impuestos/alquileres/porcGastosAlquileres.php',
    'ControlEgresosDeCaja':SERVIDOR['production'] + 'administracion/controlSucursales/controlEgresosCajaSucursales.php?userName=',
    'ControlMasivoCobranza':SERVIDOR['production'] + 'administracion/controlSucursales/controlMasivoCaja.php',
    'CargarContratosDeAlquiler':SERVIDOR['production'] + 'administracion/impuestos/alquileres/cargaContratoAlquileres.php',
    'RelacionesCtaCont':SERVIDOR['production'] + 'administracion/contabilidad/gestionRelacionesCuenta.php',
    'CargaContratosFr':SERVIDOR['production'] + 'administracion/impuestos/alquileresFranquicias/cargaContratosAlquileres.php',
    'CargaFacturasSuc':SERVIDOR['production'] + 'administracion/controlSucursales/cargaFacturaSucursales.php',
    'EgresosCajaTesoreria':SERVIDOR['production'] + 'administracion/tesoreria/cargaGastos.php',
    'GestionDeProveedores':'https://proveedores.xl.com.ar/administracion/dashboard/',
    'VentasLocatarios':SERVIDOR['production'] + 'administracion/impuestos/alquileres/locatarios/',
    # RRHH
    # 'adminEmpleados':SERVIDOR['production'] + 'administracion/recursosHumanos/controlHorarios/controlHorario.php',
    'altaVendedores':SERVIDOR['production'] + 'administracion/recursoshumanos/altaVendedores/altaVendedores.php',
    'listarGrupos':SERVIDOR['production'] + 'administracion/recursosHumanos/altaVendedores/listarGrupos.php',
    'gestionarVendedores':SERVIDOR['production'] + 'administracion/recursosHumanos/altaVendedores/gestionarVendedores.php',
    'CargaAnticipoGrupo':SERVIDOR['production'] + 'administracion/recursosHumanos/anticipoSueldos/cargaAnticipoGrupo.php',
    'CargaAnticipo':SERVIDOR['production'] + 'administracion/recursosHumanos/anticipoSueldos/cargaAnticipo.php',
    
    # Tesoreria
    'ControlDeEfectivo':SERVIDOR['production'] + 'administracion/controlSucursales/controlRecepcionEfectivo.php',
    
    #Supervisores
    'CargaProyecto':SERVIDOR['production'] + 'projects/adminProyectos/cargarProyecto.php',

    # Admin
    'AdminNotificaciones':SERVIDOR['production'] + 'sistemas/adminNotificaciones/',
}

DIR_EXTRAS = {
    'direccionario': SERVIDOR['production'] + 'proyecto_21/direccionario/index.php',
    'reporteTrello':SERVIDOR['production'] + 'Proyectos/ReporteTrello_Claude/trello-activity-report.html',
    'internos':SERVIDOR['production'] + 'comercial/recepcion/index.php',
    
}