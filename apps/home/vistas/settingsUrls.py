SERVIDOR = {
    'testing': 'http://192.168.0.233:8080/',
    'production': 'http://192.168.0.143:8080/',
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
    'Pedidos_pendiente_despacho':SERVIDOR['testing'] + 'sistemas/cronoDespacho/pedidos.php',
    'ConsultaDestino':SERVIDOR['testing'] + 'sistemas/maestroDestinos/indexMob.php',
    # Abastecimiento
    'Auditoria_orden': 'http://192.168.0.143:8080/sistemas/distriCuero/listOrdenesComercial.php',
    'CategoriasDeProductos':'http://192.168.0.143:8080/administracion/comercial/consultaCategoriaProductos.php',
    'HRecodificaciones':'http://192.168.0.143:8080/recodificacion/historialDeRecodificaciones.php',
    'Eficiencia_pedidos': 'http://192.168.0.143:8080/comercial/abastecimiento/pedidos/eficienciaPedidos.php',
    # Comercial
    'Stock_Sucursales': 'http://app.xl.com.ar:8080/stockArticulos/index.php',
    'Stock_central': 'http://192.168.0.143:8080/logistica/stock.php',
    'promocionesActivas': 'http://192.168.0.143:8080/comercial/mayoristas/promocionesBancarias/promocionesActivas.php',
    'VentasXcanal':'http://192.168.0.143:8080/comercial/abastecimiento/ventasAbastecimiento/',
    'AdmEmpleados':'http://192.168.0.143:8080/administracion/recursosHumanos/controlHorarios/verControlHorario.php',
    'AnalisisProductos':'http://app.xl.com.ar:8080/comercial/abastecimiento/analisisProducto/listado.php',
    # Mayoristas
    'Tracking_pedidos_mayoristas': 'http://192.168.0.143:8080/Despacho/tracking.php',
    # Ecommerce
    'Pedidos': SERVIDOR['testing'] + 'ECOMMERCE/',
    'Tracking_Ecommerce':SERVIDOR['testing'] + 'ecommerce/consultaPedido.php',
    'PedidosUY': SERVIDOR['testing'] + 'Uruguay/ecommerce/consultaPedidos.php',
    'Auditoria_Ecommerce': SERVIDOR['testing'] + 'ecommerce-auditoria/',
    'Auditoria_Prisma': SERVIDOR['testing'] + 'ecommerce/auditoriaPrisma/',
    'Segmentacion_clientes':SERVIDOR['testing'] + 'ecommerce/segmentacion/segmentacionDeClientes.php',
    'TableroDeControl':SERVIDOR['production'] + 'ecommerce/tableroControl/index.php',
    # Administracion
    'VentasXmedio_pago':SERVIDOR['testing'] + 'administracion/controlSucursales/resumenVentas.php',
    'consultaGastos':SERVIDOR['testing'] + 'administracion/contabilidad/consultaGastos.php',
    'ventaVsCobranza':SERVIDOR['testing'] + 'administracion/controlSucursales/ventaVsCobranza.php',
    'Controlcajasmensual':SERVIDOR['testing'] + 'administracion/controlSucursales/controlMensualCajaSucursales.php',
    'ResumenMensualAlquileres':SERVIDOR['testing'] + 'administracion/impuestos/alquileres/consultaAlquileres.php',
    'CargaGastosTesoreria':SERVIDOR['testing'] + 'administracion/controlSucursales/cargaGastosTesoreria.php',
    'DetalleContratosDeAlquiler':SERVIDOR['testing'] + 'administracion/impuestos/alquileres/detalleContratosAlquiler.php',
    'ContratosFranquicias':SERVIDOR['testing'] + 'administracion/impuestos/alquileresFranquicias/detalleContratosAlquiler.php',
    # Gerencia
    'DetalleRemitos599':'http://192.168.0.143:8080/sistemas/599/consultaderemitos.php?userName=',
    'ChequesRecibidos':'http://192.168.0.143:8080/sistemas/599/reportedecheques.php?userName=',
    # RRHH
    'AsistenciasSuc':'http://192.168.0.143:8080/sistemas/fichaje/reporteDeAsistencias.php',
    'ReporteAnticipos':'http://app.xl.com.ar:8080/administracion/recursosHumanos/anticipoSueldos/reporteAnticipos.php',

}

DIR_HERAMIENTAS = {
    # Logistica
    'Gestion_cronograma': SERVIDOR['testing'] + 'sistemas/cronoDespacho/index.php',
    'Gestion_guias_mayoristas': SERVIDOR['testing'] + 'Despacho/guias.php',
    # Abastecimiento
    'Stock_excluido': 'http://192.168.0.143:8080/sistemas/stockExcluido/index.php',
    'Carga_de_orden': 'http://192.168.0.143:8080/sistemas/distriCuero/index.php',
    'Activar_orden': 'http://192.168.0.143:8080/sistemas/distriCuero/activaOrdenes.php',
    'Desactivar_orden': 'http://192.168.0.143:8080/sistemas/distriCuero/desactivaOrdenes.php',
    'Recodificacion': 'http://192.168.0.143:8080/recodificacion/nuevoProceso.php',
    'AltaPromoBancaria':'http://192.168.0.143:8080/comercial/mayoristas/promocionesBancarias/altaPromoBancaria.php',
    'CrearGrupoPromo':'http://192.168.0.143:8080/comercial/mayoristas/promocionesBancarias/crearGrupoPromo.php',
    'EditarGrupoPromo':'http://192.168.0.143:8080/comercial/mayoristas/promocionesBancarias/listarGruposPromo.php',
    # Comercial
    'Ventas_sucursales': 'http://192.168.0.143:8080/proyecto_21/ventas-canales/ventas_comercial/index.php',
    'Gestion_categoria_productos':'http://192.168.0.143:8080/administracion/comercial/gestionCategoriaProductos.php',
    'AdministrarCuotas':'http://192.168.0.143:8080/cuotas/',
    'AdministrarInternos':'http://192.168.0.143:8080/comercial/recepcion/listado.php',
    # Mayoristas
    'Adm_Pedido':'http://192.168.0.143:8080/sistemas/despachoMayorista/index.php',
    # Ecommerce
    'Control_pedidos': SERVIDOR['testing'] + 'logistica/ecommerce/',
    'StockSegVtex': SERVIDOR['testing'] + 'ecommerce/stockSeguridad/stockSeguridad.php',
    'novICBC':'http://192.168.0.226:923/',
    # Gerencia
    'rendircobranzas': 'http://192.168.0.143:8080/sistemas/599/valoresrendir.php?userName=',
    'gestionarCobro':'http://192.168.0.143:8080/sistemas/599/composicionDeRemitos.php?userName=',
    'registrarEfectivo':'http://192.168.0.143:8080/administracion/controlSucursales/controlRecepcionEfectivo.php?userName=',
    'gestionPremiosComercial':'http://192.168.0.143:8080/comercial/supervision/gestionarPremios.php',
    # Administracion
    'ControlGastosSupervision':SERVIDOR['testing'] + 'comercial/supervision/controlarGastos.php',
    'controlGastos':SERVIDOR['testing'] + 'administracion/contabilidad/controlGastos.php',
    'cargaGastos':SERVIDOR['testing'] + 'administracion/contabilidad/cargaGastos.php',
    'cargaInicial':SERVIDOR['testing'] + 'administracion/comercioExterior/cargaInicial.php',
    'mostrarOrden':SERVIDOR['testing'] + 'administracion/comercioExterior/mostrarOrden.php',
    'Controlcajasdiario':SERVIDOR['testing'] + 'administracion/controlSucursales/controlDiarioCajaSucursales.php',
    'CargaGastosAlquileres':SERVIDOR['testing'] + 'administracion/impuestos/alquileres/cargaAlquileres.php',
    'GestionDeAlquileres':SERVIDOR['testing'] + 'administracion/impuestos/alquileres/porcGastosAlquileres.php',
    'ControlEgresosDeCaja':SERVIDOR['production'] + 'administracion/controlSucursales/controlEgresosCajaSucursales.php?userName=',
    'ControlMasivoCobranza':SERVIDOR['testing'] + 'administracion/controlSucursales/controlMasivoCaja.php',
    'CargarContratosDeAlquiler':SERVIDOR['testing'] + 'administracion/impuestos/alquileres/cargaContratoAlquileres.php',
    'RelacionesCtaCont':SERVIDOR['testing'] + 'administracion/contabilidad/gestionRelacionesCuenta.php',
    'CargaContratosFr':SERVIDOR['testing'] + 'administracion/impuestos/alquileresFranquicias/cargaContratosAlquileres.php',
    'CargaFacturasSuc':SERVIDOR['testing'] + 'administracion/controlSucursales/cargaFacturaSucursales.php',
    'EgresosCajaTesoreria':SERVIDOR['testing'] + 'administracion/tesoreria/cargaGastos.php',
    # RRHH
    'adminEmpleados':'http://192.168.0.143:8080/administracion/recursosHumanos/controlHorarios/controlHorario.php',
    'altaVendedores':'http://192.168.0.143:8080/administracion/recursoshumanos/altaVendedores/altaVendedores.php',
    'listarGrupos':'http://192.168.0.143:8080/administracion/recursosHumanos/altaVendedores/listarGrupos.php',
    'gestionarVendedores':'http://192.168.0.143:8080/administracion/recursosHumanos/altaVendedores/gestionarVendedores.php',
    'CargaAnticipoGrupo':'http://app.xl.com.ar:8080/administracion/recursosHumanos/anticipoSueldos/cargaAnticipoGrupo.php',
    'CargaAnticipo':'http://app.xl.com.ar:8080/administracion/recursosHumanos/anticipoSueldos/cargaAnticipo.php',
    
    # Tesoreria
    'ControlDeEfectivo':'http://192.168.0.143:8080/administracion/controlSucursales/controlRecepcionEfectivo.php',
}

DIR_EXTRAS = {
    'direccionario': 'http://192.168.0.143:8080/proyecto_21/direccionario/index.php',
    'reporteTrello':'http://192.168.0.143:8080/Proyectos/ReporteTrello_Claude/trello-activity-report.html',
    'internos':'http://192.168.0.143:8080/comercial/recepcion/index.php',
    
}