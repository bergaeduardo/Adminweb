# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pprint
from tkinter.tix import CELL, COLUMN
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
# Removed numpy imports as they were only used by moved import functions
# from numpy import int64, isnan
from consultasTango.models import StockCentral,SjStockDisponibleEcommerce
from consultasWMS.models import Ubicacion
from consultasLakersBis.models import Direccionario, SofStockLakers, SucursalesLakers # Added SucursalesLakers
from django.views.generic.list import ListView
from apps.settingsUrls import *
# Removed SQL imports as they were only used by moved import functions
# from apps.home.SQL.Sql_WMS import validar_ubicacion,actualizar_ubicacion
# from apps.home.SQL.Sql_Tango import validar_pedido,cerrar_pedido,validar_articulo,borrar_contTabla,cargar_articulo
# from apps.static.Scripts.getData_Trello import reporte_trello
import json
from consultasTango.filters import *
from consultasLakersBis.filters import filtroCanal,filtroTipoLocal,filtroGrupoEmpresario,DireccionarioFilter
from django.contrib import messages
# Removed openpyxl and pandas imports as they were only used by moved import functions
# import openpyxl
# import pandas as pd


from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from consultasLakersBis.forms import sucursalesform
import os
import subprocess
from django.templatetags.static import static

@login_required(login_url="/login/")
def runscript(request):
    # script_path = 'ruta_al_script/script.py'
    # # Ejecutar el script utilizando subprocess
    # output = subprocess.check_output(['python', script_path])
    return render(request, 'appConsultasTango/runScript.html')


def runscriptResult(request):
    mensaje_success=''
    output=''
    ruta_actual = r'C:\Users\eduardo.berga\Desktop\Proyectos\Lakers_Lab\Adminweb\apps\static\Scripts'
    archivo = r'\miTareaPy.py'
    # script_path = static(r'Scripts\Imprimir_Etiquetas_Andreani2.py')
    # script_path= ruta_actual + '\Scripts\hora.py'
    # script_path = r'C:\Users\eduardo.berga\Desktop\Proyectos\Lakers_Lab\Adminweb\apps\static\Scripts\hora.py'
    script_path = ruta_actual + archivo
    print('Ruta actual: ' + script_path)
    # # Ejecutar el script utilizando subprocess
    resultado = subprocess.run(['python', script_path], capture_output=True, text=True)
    salida = resultado.returncode
    if salida == 0:
        mensaje_success = "La ejecucion fue un exito"
        output = 'El resultado del script es la hora actual: ' + resultado.stdout
    print(resultado)
    # output = subprocess.check_output(['python', script_path])
    # output = "Hola Mundo"
    return render(request, 'appConsultasTango/runScriptResult.html', {'mensaje_success': mensaje_success,'output': output})


@login_required(login_url="/login/")
def editarSucursal(request,id):
    suc = SucursalesLakers.objects.get(nro_sucursal=id)
    sucForm = sucursalesform(request.POST or None, request.FILES or None, instance=suc)
    Disabled='disabled'
    # print(id)
    # print(sucForm.errors)
    if sucForm.is_valid() and request.POST:
        suc = sucForm.save(commit=False)
        suc.save()
        messages.success(request, 'OK')
        infForm = sucForm.cleaned_data
        # print(infForm)
        return redirect('extras:editarSucursal',id=id) # Updated redirect

    return  render(request,'appConsultasTango/editarSucursal.html',{'formulario':sucForm,'Disabled':Disabled})

@login_required(login_url="/login/")
def registraSucursal(request):
    if request.method=='POST':
        formulario=sucursalesform(request.POST)
        if formulario.is_valid():
            sucursal = formulario.save(commit=False)
            sucursal.save()
            messages.success(request, 'OK')
            infForm = formulario.cleaned_data
            # print(infForm)
            return redirect('extras:extras_direccionario') # Updated redirect

    else:
        formulario=sucursalesform()

    return  render(request,'appConsultasTango/registraSucursal.html',{'formulario':formulario})

# Removed import_file_etiquetas and its helpers

# Removed import_file_cierrePedidos and its helpers

# Removed import_file_cierrePedidosUY and its helpers

# Removed import_file_ubi and its helpers


@login_required(login_url="/login/") # DESABILITADO
def direccionario(request):
    Nombre='Pedidos' # This Nombre seems incorrect for a "Direccionario" view
    dir_iframe = DIR_EXTRAS['direccionario']
    return render(request,'home/direccionario.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def agenda(request):
    Nombre='Direccionario'
    datos = Direccionario.objects.all()
    canal = filtroCanal()
    tipo_local = filtroTipoLocal()
    grupo = filtroGrupoEmpresario()

    for dato in datos:
        if dato.mail_grupo_emp:
            # Reemplazar comas y espacios por punto y coma para tener un único delimitador
            mail_string = dato.mail_grupo_emp.replace(',', ';').replace(' ', ';')
            # Dividir la cadena y limpiar cada dirección de correo
            dato.mails_empresa = [mail.strip() for mail in mail_string.split(';') if mail.strip()]
        else:
            dato.mails_empresa = []

    return render(request,'appConsultasTango/direccionario2.html',{'datos': datos,'canal':canal,'tipo_local':tipo_local,'grupo':grupo,'Nombre':Nombre})

@login_required(login_url="/login/")
def DireccionarioTabla(request):    # <<<----- Direccionario Tabla -->
    Nombre='Direccionario'
    stock = Direccionario.objects.all()
    myFilter = DireccionarioFilter(request.GET, queryset=stock)
    if request.GET:
        datos = myFilter
    else:
        datos = Direccionario.objects.all()

    return render(request,'appConsultasTango/direccionarioTabla.html',{'myFilter':myFilter,'datos':datos,'Nombre':Nombre})

# @login_required(login_url="/login/")
# def reporTrello(request):
#     miReporte_json = reporte_trello()
# #     print(type(miReporte_json))

# # # convertir la variable miReporte_json del formato <class 'dict'> a json
#     miReporte_json = json.dumps(miReporte_json)
#     print(type(miReporte_json))
#     # print(miReporte_json)

#     return render(request, 'home/trello-activity-report.html', {'data': miReporte_json})

@login_required(login_url="/login/")
def reporTrello(request):
    Nombre=''
    dir_iframe = DIR_EXTRAS['reporteTrello']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def internos(request):
    Nombre=''
    dir_iframe = DIR_EXTRAS['internos']
    return render(request,'home/PlantillaReportes.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})
