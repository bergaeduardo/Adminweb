import pprint
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
# from Transportes.models import Transporte # Removed Transportes dependency
# from Transportes.forms import TransporteForm # Removed Transportes dependency
from django.views.generic.list import ListView
from apps.settingsUrls import *

# Logistica
@login_required(login_url="/login/")
def Kpis_Logistica(request):
    Nombre='Kpis Logistica'
    dir_iframe = DIR_PBI['Kpis_Logistica']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Abastecimiento - No views currently

# Comercial
@login_required(login_url="/login/")
def Promociones(request):
    Nombre='Promociones'
    dir_iframe = DIR_PBI['Promociones']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Inventarios_Sucursales(request):
    Nombre='Inventarios Sucursales'
    dir_iframe = DIR_PBI['Inventarios_Sucursales']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Conteos(request):
    Nombre='Conteos'
    dir_iframe = DIR_PBI['Conteos']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Geodatos(request):
    Nombre='Geodatos'
    dir_iframe = DIR_PBI['Geodatos']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Notas_de_credito(request):
    Nombre='Notas de credito'
    dir_iframe = DIR_PBI['Notas_de_credito']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Ventas_Franquicias(request):
    Nombre='Ventas Franquicias'
    dir_iframe = DIR_PBI['Ventas_Franquicias']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Ventas_Sucursales(request):
    Nombre='Ventas Sucursales'
    dir_iframe = DIR_PBI['Ventas_Sucursales']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Ventas_SucursalesUY(request):
    Nombre='Ventas Sucursales Uruguay'
    dir_iframe = DIR_PBI['Ventas_SucursalesUY']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Velocidad_de_Ventas(request):
    Nombre='Velocidad de Ventas'
    dir_iframe = DIR_PBI['Velocidad_de_Ventas']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Mayoristas
@login_required(login_url="/login/")
def Ventas_Mayoristas(request):
    Nombre='Ventas Mayoristas'
    dir_iframe = DIR_PBI['Ventas_Mayoristas']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Ecommerce
@login_required(login_url="/login/")
def Ventas_Ecommerce(request):
    Nombre='Ventas Ecommerce'
    dir_iframe = DIR_PBI['Ventas_Ecommerce']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Kpis_Ecommerce(request):
    Nombre='Kpis Ecommerce'
    dir_iframe = DIR_PBI['Kpis_Ecommerce']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def PromocionesEcommerce(request):
    Nombre='Promociones Ecommerce'
    dir_iframe = DIR_PBI['PromocionesEcommerce']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

# Gerencia
@login_required(login_url="/login/")
def PremiosComercial(request):
    Nombre='' # Nombre is empty in original, keeping it
    dir_iframe = DIR_PBI['PremiosComercial']
    return render(request,'home/PlantillaDash_PBI.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})
