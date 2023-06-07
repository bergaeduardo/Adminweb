import pprint
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from Transportes.models import Transporte
from Transportes.forms import TransporteForm
from django.views.generic.list import ListView
from apps.home.vistas.settingsUrls import *
from consultasWMS.filters import *
from consultasWMS.models import RoMovimientosWms

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
    myFilter = OrderFilter(request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = RoMovimientosWms.objects.filter(ubic_destino='01')

    return render(request,'appConsultasWMS/Mov_WMS.html',{'myFilter':myFilter,'registros':datos,'Nombre':Nombre})

# Abastecimiento

@login_required(login_url="/login/")
def Auditoria_orden(request):
    Nombre='Auditoria orden'
    dir_iframe = DIR_REPORTES['Auditoria_orden']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Comercial

@login_required(login_url="/login/")
def Stock_Sucursales(request):
    Nombre='Stock Sucursales'
    dir_iframe = DIR_REPORTES['Stock_Sucursales']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")#---> Discontinuado
def Stock_central(request):
    Nombre='Stock central'
    dir_iframe = DIR_REPORTES['Stock_central']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Mayoristas

@login_required(login_url="/login/")
def Tracking_pedidos_mayoristas(request):
    Nombre='Tracking pedidos_mayoristas'
    dir_iframe = DIR_REPORTES['Tracking_pedidos_mayoristas']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Ecommerce

@login_required(login_url="/login/")
def Pedidos(request):
    Nombre='Pedidos'
    dir_iframe = DIR_REPORTES['Pedidos']
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
def VentasXmedio_pago(request):
    Nombre='Resumen de Ventas'
    dir_iframe = DIR_REPORTES['VentasXmedio_pago']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Consultagastos(request):
    Nombre='Consulta de gastos'
    dir_iframe = DIR_REPORTES['consultaGastos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})
    # url='http://192.168.0.143:8080/administracion/contabilidad/consultaGastos.php'
    # return redirect(url)

@login_required(login_url="/login/")
def VentaVscobranza(request):
    Nombre='Venta Vs cobranza'
    dir_iframe = DIR_REPORTES['ventaVsCobranza']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})
    # url='http://192.168.0.143:8080/administracion/controlSucursales/ventaVsCobranza.php'
    # return redirect(url)

@login_required(login_url="/login/")
def Controlcajasmensual(request):
    Nombre='Control cajas Mensual'
    dir_iframe = DIR_REPORTES['Controlcajasmensual']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Gerencia

@login_required(login_url="/login/")
def DetalleRemitos599(request):
    Nombre='Detalle Remitos 599'
    dir_iframe = DIR_REPORTES['DetalleRemitos599']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def ChequesRecibidos(request):
    Nombre='Reporte de cheques'
    dir_iframe = DIR_REPORTES['ChequesRecibidos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})