import pprint
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
# from Transportes.models import Transporte
# from Transportes.forms import TransporteForm
from django.views.generic.list import ListView
from apps.settingsUrls import *
from django.conf import settings
from consultasWMS.filters import *
from consultasTango.filters import *
from consultasWMS.models import RoMovimientosWms
from consultasLakersBis.models import SofStockLakers
from consultasTango.models import StockCentral,SjStockDisponibleEcommerce
from consultasTango.filters import *
from consultasLakersBis.filters import *


# RRHH

@login_required(login_url="/login/")
def reporteAnticipos(request):
    Nombre='Reporte de Anticipos'
    dir_iframe = DIR_REPORTES['ReporteAnticipos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def AsistenciasSuc(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['AsistenciasSuc']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Logistica

@login_required(login_url="/login/")
def Pedidos_pendiente_despacho(request):
    Nombre='Despachos pendientes'
    dir_iframe = DIR_REPORTES['Pedidos_pendiente_despacho']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def MovimientosWms(request):
    Nombre='Movimientos WMS'

    stock = RoMovimientosWms.objects.all()
    myFilter = OrderFilterWms(request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = RoMovimientosWms.objects.filter(ubic_destino='01')

    return render(request,'appConsultasWMS/Mov_WMS.html',{'myFilter':myFilter,'registros':datos,'Nombre':Nombre})

@login_required(login_url="/login/")
def ConsultaDestino(request):
    Nombre='Consulta de Destino'
    dir_iframe = DIR_REPORTES['ConsultaDestino']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Abastecimiento

@login_required(login_url="/login/")
def Auditoria_orden(request):
    Nombre='Auditoria orden'
    dir_iframe = DIR_REPORTES['Auditoria_orden']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def CategoriasDeProductos(request):
    Nombre='Categorias de Productos'
    dir_iframe = DIR_REPORTES['CategoriasDeProductos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def HRecodificaciones(request):
    Nombre='Historial Recodificaciones Outlet'
    dir_iframe = DIR_REPORTES['HRecodificaciones']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Eficiencia_pedidos(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['Eficiencia_pedidos']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def promocionesActivas(request):
    Nombre='Promociones Activas'
    dir_iframe = DIR_REPORTES['promocionesActivas']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Comercial

@login_required(login_url="/login/")
def AdmEmpleados(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['AdmEmpleados']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def VentasXcanal(request):
    Nombre='Ventas por canal'
    dir_iframe = DIR_REPORTES['VentasXcanal']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Stock_Sucursales(request):
    Nombre='Stock Sucursales'
    dir_iframe = DIR_REPORTES['Stock_Sucursales']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def AnalisisProductos(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['AnalisisProductos']
    return redirect(dir_iframe)

@login_required(login_url="/login/")#---> Discontinuado
def Stock_central(request):
    Nombre='Stock central'
    dir_iframe = DIR_REPORTES['Stock_central']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Mayoristas

@login_required(login_url="/login/")
def Tracking_pedidos_mayoristas(request):
    Nombre='Tracking pedidos_mayoristas'
    # dir_iframe = DIR_REPORTES['Tracking_pedidos_mayoristas']
    return render(request,'home/page-404.html')


# Ecommerce

@login_required(login_url="/login/")
def TableroDeControl(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['TableroDeControl']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Tracking_Ecommerce(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['Tracking_Ecommerce']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Segmentacion_clientes(request):
    Nombre='Segmentación de clientes'
    dir_iframe = DIR_REPORTES['Segmentacion_clientes']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Pedidos(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['Pedidos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def PedidosUY(request):
    Nombre=''
    dir_iframe = DIR_REPORTES['PedidosUY']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Auditoria_Ecommerce(request):
    Nombre='Auditoría Ecommerce'
    dir_iframe = DIR_REPORTES['Auditoria_Ecommerce']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Auditoria_Prisma(request):
    Nombre='Auditoría Prisma'
    dir_iframe = DIR_REPORTES['Auditoria_Prisma']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Administracion

@login_required(login_url="/login/")
def ContratosFranquicias(request):
    Nombre='Contratos Franquicias'
    dir_iframe = DIR_REPORTES['ContratosFranquicias']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


@login_required(login_url="/login/")
def VentasXmedio_pago(request):
    Nombre='Resumen de Ventas'
    dir_iframe = DIR_REPORTES['VentasXmedio_pago']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Consultagastos(request):
    Nombre='Consulta de gastos'
    dir_iframe = DIR_REPORTES['consultaGastos']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def VentaVscobranza(request):
    Nombre='Venta Vs cobranza'
    dir_iframe = DIR_REPORTES['ventaVsCobranza']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Controlcajasmensual(request):
    Nombre='Control cajas Mensual'
    dir_iframe = DIR_REPORTES['Controlcajasmensual']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def ResumenMensualAlquileres(request):
    Nombre='Resumen Mensual de Alquileres'
    dir_iframe = DIR_REPORTES['ResumenMensualAlquileres']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def CargaGastosTesoreria(request):
    Nombre='CargaGastosTesoreria'
    dir_iframe = DIR_REPORTES['CargaGastosTesoreria']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def DetalleContratosDeAlquiler(request):
    Nombre='Detalle Contratos De Alquiler'
    dir_iframe = DIR_REPORTES['DetalleContratosDeAlquiler']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def GastosSupervision(request):
    Nombre='Dashboard Gastos de Supervision'
    dir_iframe = DIR_REPORTES['GastosSupervision']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Gerencia

@login_required(login_url="/login/")
def DetalleRemitos599(request,UserName):
    Nombre='Detalle Remitos 599'
    dir_iframe = DIR_REPORTES['DetalleRemitos599'] + UserName
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def ChequesRecibidos(request,UserName):
    Nombre='Reporte de cheques'
    dir_iframe = DIR_REPORTES['ChequesRecibidos'] + UserName
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


def cambiar_conexion(conection, nombre_db):
    if conection == 'mi_db_2':
        settings.DATABASES['mi_db_2']['NAME'] = nombre_db
        print('Cambiando base de datos a LAKER_SA')
    elif conection == 'mi_db_4':
        settings.DATABASES['mi_db_4']['NAME'] = nombre_db


@login_required(login_url="/login/")
def stockcentral(request):
    # myFilter=None
    parametro=''
    Nombre='Stock Central'
    nombre_db='LAKER_SA'
    conection = 'mi_db_2'
    cambiar_conexion(conection,nombre_db)
    parametro = 'mi_db_2'
    print('Se establecio la conexion por medio de ' + conection + ' a la base de datos ' + nombre_db)
    stock = StockCentral.objects.all()
    consulta = Utilidades.filtroDepo(parametro)
    filtroDepo = Utilidades.itemsFil(consulta)
    consulta = Utilidades.filtroTemp(parametro)
    filtroTemp = Utilidades.itemsFil(consulta)
    consulta = Utilidades.filtroRub(parametro)
    filtroRub = Utilidades.itemsFil(consulta)
    myFilter = OrderFilter(filtroDepo,filtroTemp,filtroRub,request.GET, queryset=stock)


    if request.GET:
        datos = myFilter
    else:
        datos = StockCentral.objects.filter(deposito='05')

    return render(request,'appConsultasTango/StockCentral.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})

@login_required(login_url="/login/")
def stockcentral_pivot(request):
    # myFilter=None
    parametro=''
    Nombre='Stock Supply'
    nombre_db='LAKER_SA'
    conection = 'mi_db_2'
    stock = []
    cambiar_conexion(conection,nombre_db)
    parametro = 'mi_db_2'
    print('Se establecio la conexion por medio de ' + conection + ' a la base de datos ' + nombre_db)

    aux = Utilidades.consultarStock_pivot(parametro)
    temporada = Utilidades.listdropdowns(Utilidades.filtroTemp(parametro))
    rubro = Utilidades.listdropdowns(Utilidades.filtroRub(parametro))
    categoria = Utilidades.listdropdowns(Utilidades.filtroCat(parametro))
    columnas = aux[1]

    if 'botonBuscar' in request.GET:
            stock = aux[0]
            filtro_rubro = request.GET.get('filtro_rubro')
            filtro_categoria = request.GET.get('filtro_categoria')
            filtro_temporada = request.GET.get('filtro_temporada')

            if filtro_rubro:
                stock = [item for item in stock if item[3] == filtro_rubro]  # Índice 3 para 'Rubro'
            if filtro_categoria:
                stock = [item for item in stock if item[4] == filtro_categoria]  # Índice 4 para 'Categoría'
            if filtro_temporada:
                stock = [item for item in stock if item[5] == filtro_temporada]  # Índice 5 para 'Temporada'

            print('se presiono el boton: botonBuscar')
            # print(stock)

    return render(request,'appConsultasTango/StockCentral_pivot.html',{'articulos':stock,'columnas':columnas,'Temporadas':temporada,'Rubros':rubro, 'Categorias':categoria,'Nombre':Nombre})

@login_required(login_url="/login/")
def stockcentral_pivotUY(request):
    # myFilter=None
    parametro=''
    Nombre='Stock Supply'
    nombre_db='TASKY_SA'
    conection = 'mi_db_2'
    stock = []
    cambiar_conexion(conection,nombre_db)
    parametro = 'mi_db_2'
    print('Se establecio la conexion por medio de ' + conection + ' a la base de datos ' + nombre_db)

    aux = Utilidades.consultarStock_pivot(parametro)
    temporada = Utilidades.listdropdowns(Utilidades.filtroTemp(parametro))
    rubro = Utilidades.listdropdowns(Utilidades.filtroRub(parametro))
    categoria = Utilidades.listdropdowns(Utilidades.filtroCat(parametro))
    columnas = aux[1]

    if 'botonBuscar' in request.GET:
            stock = aux[0]
            filtro_rubro = request.GET.get('filtro_rubro')
            filtro_categoria = request.GET.get('filtro_categoria')
            filtro_temporada = request.GET.get('filtro_temporada')

            if filtro_rubro:
                stock = [item for item in stock if item[3] == filtro_rubro]  # Índice 3 para 'Rubro'
            if filtro_categoria:
                stock = [item for item in stock if item[4] == filtro_categoria]  # Índice 4 para 'Categoría'
            if filtro_temporada:
                stock = [item for item in stock if item[5] == filtro_temporada]  # Índice 5 para 'Temporada'

            print('se presiono el boton: botonBuscar')
            # print(stock)

    return render(request,'appConsultasTango/StockCentral_pivotUY.html',{'articulos':stock,'columnas':columnas,'Temporadas':temporada,'Rubros':rubro, 'Categorias':categoria,'Nombre':Nombre})


@login_required(login_url="/login/")
def stockcUY(request):
    myFilter=None
    parametro=''
    Nombre=''
    nombre_db='TASKY_SA'
    parametro = 'mi_db_2'
    cambiar_conexion(parametro,nombre_db)
    print('Se establecio la conexion por medio de ' + parametro + ' a la base de datos ' + nombre_db)
    stock = StockCentral.objects.all()
    consulta = Utilidades.filtroDepo(parametro)
    filtroDepo = Utilidades.itemsFil(consulta)
    consulta = Utilidades.filtroTemp(parametro)
    filtroTemp = Utilidades.itemsFil(consulta)
    consulta = Utilidades.filtroRub(parametro)
    filtroRub = Utilidades.itemsFil(consulta)
    myFilter = OrderFilter(filtroDepo,filtroTemp,filtroRub,request.GET, queryset=stock)


    if request.GET:
        datos = myFilter
    else:
        datos = StockCentral.objects.filter(deposito='05')

    return render(request,'appConsultasTango/StockUY.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})

@login_required(login_url="/login/")
def stockcentral_ecommerce(request):
    Nombre='Stock Central ecommerce'
    parametro=''
    Nombre='Stock Central'
    nombre_db='LAKER_SA'
    conection = 'mi_db_2'
    cambiar_conexion(conection,nombre_db)
    parametro = 'mi_db_2'
    print('Se establecio la conexion por medio de ' + conection + ' a la base de datos ' + nombre_db)
    stock = SjStockDisponibleEcommerce.objects.filter(total__gt=0)
    consulta = Utilidades.filtroRub(parametro)
    filtroRub = Utilidades.itemsFil(consulta)
    myFilter = filtro_stock_ecommerce(filtroRub,request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = SjStockDisponibleEcommerce.objects.filter(deposito='01')

    return render(request,'appConsultasTango/StockCentral_ecommerce.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})

@login_required(login_url="/login/")
def stockUY_ecommerce(request):
    Nombre='Stock Uruguay ecommerce'
    parametro=''
    Nombre=''
    nombre_db='TASKY_SA'
    parametro = 'mi_db_2'
    cambiar_conexion(parametro,nombre_db)
    print('Se establecio la conexion por medio de ' + parametro + ' a la base de datos ' + nombre_db)
    stock = SjStockDisponibleEcommerce.objects.filter(total__gt=0)
    consulta = Utilidades.filtroRub(parametro)
    filtroRub = Utilidades.itemsFil(consulta)
    myFilter = filtro_stock_ecommerce(filtroRub,request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = SjStockDisponibleEcommerce.objects.filter(deposito='01')

    return render(request,'appConsultasTango/StockUY_ecommerce.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})

@login_required(login_url="/login/")
def stockSucursalesLakers(request):
    Nombre='Stock Sucursales'
    nombre_db='LOCALES_LAKERS'
    parametro = 'mi_db_4'
    cambiar_conexion(parametro,nombre_db)
    print('Se establecio la conexion por medio de ' + parametro + ' a la base de datos ' + nombre_db)
    stock = SofStockLakers.objects.all()
    consulta = UtilidadesTasky.filtroDescSuc(parametro)
    filtroDepo = UtilidadesTasky.itemsFil(consulta)
    consulta = UtilidadesTasky.filtroTemp(parametro)
    filtroTemp = UtilidadesTasky.itemsFil(consulta)
    consulta = UtilidadesTasky.filtroRub(parametro)
    filtroRub = UtilidadesTasky.itemsFil(consulta)
    myFilter = OrderFilterTasky(filtroDepo,filtroTemp,filtroRub,request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = SofStockLakers.objects.all()

    return render(request,'appConsultasTango/StockSucursales.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})

def stockSucursalesTasky(request):
    Nombre='Stock Sucursales Uruguay'
    nombre_db='SUCURSALES_URUGUAY'
    parametro = 'mi_db_4'
    cambiar_conexion(parametro,nombre_db)
    print('Se establecio la conexion por medio de ' + parametro + ' a la base de datos ' + nombre_db)
    stock = SofStockLakers.objects.all()
    consulta = UtilidadesTasky.filtroDescSuc(parametro)
    filtroDepo = UtilidadesTasky.itemsFil(consulta)
    consulta = UtilidadesTasky.filtroTemp(parametro)
    filtroTemp = UtilidadesTasky.itemsFil(consulta)
    consulta = UtilidadesTasky.filtroRub(parametro)
    filtroRub = UtilidadesTasky.itemsFil(consulta)
    myFilter = OrderFilterTasky(filtroDepo,filtroTemp,filtroRub,request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = SofStockLakers.objects.all()

    return render(request,'appConsultasTango/stockSucursalesUY.html',{'myFilter':myFilter,'articulos':datos,'Nombre':Nombre})
