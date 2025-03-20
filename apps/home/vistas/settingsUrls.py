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
    'Pedidos_pendiente_despacho':SERVIDOR['production'] + 'sistemas/cronoDespacho/pedidos.php',
    'ConsultaDestino':SERVIDOR['production'] + 'sistemas/maestroDestinos/indexMob.php',
    # Abastecimiento
    'Auditoria_orden': SERVIDOR['testing']  + 'sistemas/distriCuero/listOrdenesComercial.php',
    'CategoriasDeProductos':SERVIDOR['testing']  + 'administracion/comercial/consultaCategoriaProductos.php',
    'HRecodificaciones':SERVIDOR['testing']  + 'recodificacion/historialDeRecodificaciones.php',
    'Eficiencia_pedidos': SERVIDOR['testing']  + 'comercial/abastecimiento/pedidos/eficienciaPedidos.php',
    # Comercial
    'Stock_Sucursales': SERVIDOR['testing']  + 'stockArticulos/index.php',
    'Stock_central': SERVIDOR['testing']  + 'logistica/stock.php',
    'promocionesActivas': SERVIDOR['testing']  + 'comercial/mayoristas/promocionesBancarias/promocionesActivas.php',
    'VentasXcanal':SERVIDOR['testing']  + 'comercial/abastecimiento/ventasAbastecimiento/',
    'AdmEmpleados':SERVIDOR['testing']  + 'administracion/recursosHumanos/controlHorarios/verControlHorario.php',
    'AnalisisProductos':SERVIDOR['testing']  + 'comercial/abastecimiento/analisisProducto/listado.php',
    # Mayoristas
    'Tracking_pedidos_mayoristas': SERVIDOR['testing']  + 'Despacho/tracking.php',
    # Ecommerce
    'Pedidos': SERVIDOR['production'] + 'ECOMMERCE/',
    'Tracking_Ecommerce':SERVIDOR['production'] + 'ecommerce/consultaPedido.php',
    'PedidosUY': SERVIDOR['production'] + 'Uruguay/ecommerce/consultaPedidos.php',
    'Auditoria_Ecommerce': SERVIDOR['production'] + 'ecommerce-auditoria/',
    'Auditoria_Prisma': SERVIDOR['production'] + 'ecommerce/auditoriaPrisma/',
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
    # Gerencia
    'DetalleRemitos599':SERVIDOR['testing']  + 'sistemas/599/consultaderemitos.php?userName=',
    'ChequesRecibidos':SERVIDOR['testing']  + 'sistemas/599/reportedecheques.php?userName=',
    # RRHH
    'AsistenciasSuc':'http://192.168.0.143:8080/sistemas/fichaje/reporteDeAsistencias.php',
    'ReporteAnticipos':'http://app.xl.com.ar:8080/administracion/recursosHumanos/anticipoSueldos/reporteAnticipos.php',

}

DIR_HERAMIENTAS = {
    # Logistica
    'Gestion_cronograma': SERVIDOR['production'] + 'sistemas/cronoDespacho/index.php',
    'Gestion_guias_mayoristas': SERVIDOR['production'] + 'Despacho/guias.php',
    # Abastecimiento
    'Stock_excluido': SERVIDOR['testing']  + 'sistemas/stockExcluido/index.php',
    'Carga_de_orden': SERVIDOR['testing']  + 'sistemas/distriCuero/index.php',
    'Activar_orden': SERVIDOR['testing']  + 'sistemas/distriCuero/activaOrdenes.php',
    'Desactivar_orden': SERVIDOR['testing']  + 'sistemas/distriCuero/desactivaOrdenes.php',
    'Recodificacion': SERVIDOR['testing']  + 'recodificacion/nuevoProceso.php',
    'AltaPromoBancaria':SERVIDOR['testing']  + 'comercial/mayoristas/promocionesBancarias/altaPromoBancaria.php',
    'CrearGrupoPromo':SERVIDOR['testing']  + 'comercial/mayoristas/promocionesBancarias/crearGrupoPromo.php',
    'EditarGrupoPromo':SERVIDOR['testing']  + 'comercial/mayoristas/promocionesBancarias/listarGruposPromo.php',
    # Comercial
    'Gestion_categoria_productos':SERVIDOR['testing']  + 'administracion/comercial/gestionCategoriaProductos.php',
    'AdministrarCuotas':SERVIDOR['testing']  + 'cuotas/',
    'AdministrarInternos':SERVIDOR['testing']  + 'comercial/recepcion/listado.php',
    # Mayoristas
    'Adm_Pedido':SERVIDOR['testing']  + 'sistemas/despachoMayorista/index.php',
    # Ecommerce
    'Control_pedidos': SERVIDOR['production'] + 'logistica/ecommerce/',
    'StockSegVtex': SERVIDOR['production'] + 'ecommerce/stockSeguridad/stockSeguridad.php',
    'novICBC':'http://192.168.0.226:923/',
    # Gerencia
    'rendircobranzas': SERVIDOR['testing']  + 'sistemas/599/valoresrendir.php?userName=',
    'gestionarCobro':SERVIDOR['testing']  + 'sistemas/599/composicionDeRemitos.php?userName=',
    'registrarEfectivo':SERVIDOR['testing']  + 'administracion/controlSucursales/controlRecepcionEfectivo.php?userName=',
    'gestionPremiosComercial':SERVIDOR['testing']  + 'comercial/supervision/gestionarPremios.php',
    # Administracion
    'ControlGastosSupervision':SERVIDOR['production'] + 'comercial/supervision/controlarGastos.php',
    'controlGastos':SERVIDOR['production'] + 'administracion/contabilidad/controlGastos.php',
    'cargaGastos':SERVIDOR['production'] + 'administracion/contabilidad/cargaGastos.php',
    'cargaInicial':SERVIDOR['production'] + 'administracion/comercioExterior/cargaInicial.php',
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