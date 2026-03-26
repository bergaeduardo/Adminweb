# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pprint
from tkinter.tix import CELL, COLUMN
from django import template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
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
from consultasLakersBis.filters import filtroCanal,filtroTipoLocal,filtroGrupoEmpresario,DireccionarioFilter,filtroProvincias
from django.contrib import messages
# Removed openpyxl and pandas imports as they were only used by moved import functions
# import openpyxl
# import pandas as pd


from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from consultasLakersBis.forms import sucursalesform, SucursalesLakersCompletaForm
import os
import subprocess
from django.templatetags.static import static


def usuario_es_admin_o_sistemas(user):
    """Verifica si el usuario pertenece a los grupos 'admin' o 'Sistemas'"""
    return user.groups.filter(name__in=['admin', 'Sistemas']).exists() or user.is_superuser

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
        # Redirige al listado del direccionario tras guardar
        return redirect('extras:extras_direccionario')

    return  render(request,'appConsultasTango/editarSucursal.html',{'formulario':sucForm,'Disabled':Disabled})

@login_required(login_url="/login/")
@user_passes_test(usuario_es_admin_o_sistemas, login_url="/login/")
def editarSucursalCompleta(request, id):
    """
    Vista para editar TODOS los campos de una sucursal.
    Solo accesible para usuarios de grupos 'admin' y 'Sistemas'.
    """
    sucursal = get_object_or_404(SucursalesLakers, nro_sucursal=id)
    
    if request.method == 'POST':
        formulario = SucursalesLakersCompletaForm(request.POST, request.FILES, instance=sucursal)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'Sucursal {sucursal.nro_sucursal} - {sucursal.desc_sucursal} actualizada exitosamente.')
            return redirect('extras:extras_direccionario')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        formulario = SucursalesLakersCompletaForm(instance=sucursal)
    
    context = {
        'formulario': formulario,
        'sucursal': sucursal,
        'nro_sucursal': id,
    }
    
    return render(request, 'consultasLakersBis/editarSucursalCompleta.html', context)

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
    Nombre = 'Direccionario'
    canales    = filtroCanal()
    provincias = filtroProvincias()
    tipo_local = filtroTipoLocal()
    grupo      = filtroGrupoEmpresario()
    return render(request, 'appConsultasTango/direccionario2.html', {
        'Nombre':     Nombre,
        'canales':    canales,
        'provincias': provincias,
        'tipo_local': tipo_local,
        'grupo':      grupo,
    })

@login_required(login_url="/login/")
def buscar_sucursales(request):
    """Endpoint AJAX para búsqueda y filtrado del direccionario."""
    action = request.POST.get('action') or request.GET.get('action', 'buscar')

    if action == 'getCanales':
        canales = list(
            Direccionario.objects.filter(nro_sucursal_madre__isnull=True)
            .exclude(canal__isnull=True).exclude(canal='')
            .values_list('canal', flat=True)
            .distinct().order_by('canal')
        )
        return JsonResponse({'canales': canales})

    if action == 'getProvincias':
        provincias = list(
            Direccionario.objects.filter(nro_sucursal_madre__isnull=True)
            .exclude(provincia__isnull=True).exclude(provincia='')
            .values_list('provincia', flat=True)
            .distinct().order_by('provincia')
        )
        return JsonResponse({'provincias': provincias})

    # action == 'buscar'
    busqueda      = (request.POST.get('busqueda')      or request.GET.get('busqueda', '')).strip()
    canal         = (request.POST.get('canal')         or request.GET.get('canal', '')).strip()
    provincia     = (request.POST.get('provincia')     or request.GET.get('provincia', '')).strip()
    tipo_local    = (request.POST.get('tipo_local')    or request.GET.get('tipo_local', '')).strip()
    grupo_empresario = (request.POST.get('grupo_empresario') or request.GET.get('grupo_empresario', '')).strip()

    # mostrar_todos: solo permitido para admin / Sistemas / superuser
    mostrar_todos_raw = (request.POST.get('mostrar_todos') or request.GET.get('mostrar_todos', 'false'))
    puede_ver_todo = (
        request.user.groups.filter(name__in=['admin', 'Sistemas']).exists()
        or request.user.is_superuser
    )

    qs = Direccionario.objects.all()
    if not (puede_ver_todo and mostrar_todos_raw == 'true'):
        qs = qs.filter(nro_sucursal_madre__isnull=True)

    if busqueda:
        qs = qs.filter(
            Q(desc_sucursal__icontains=busqueda) |
            Q(localidad__icontains=busqueda) |
            Q(direccion__icontains=busqueda)
        )
    if canal:
        qs = qs.filter(canal=canal)
    if provincia:
        qs = qs.filter(provincia=provincia)
    if tipo_local:
        qs = qs.filter(tipo_local=tipo_local)
    if grupo_empresario:
        qs = qs.filter(grupo_empresario=grupo_empresario)

    data = []
    puede_ver_tecnico = (
        request.user.groups.filter(name__in=['admin', 'soporteExt']).exists()
        or request.user.is_superuser
    )
    for d in qs:
        data.append({
            'nro_sucursal':        d.nro_sucursal,
            'cod_client':          d.cod_client or '',
            'desc_sucursal':       d.desc_sucursal or '',
            'canal':               d.canal or '',
            'tipo_local':          d.tipo_local or '',
            'grupo_empresario':    d.grupo_empresario or '',
            'direccion':           d.direccion or '',
            'telefono':            d.telefono or '',
            'mail':                d.mail or '',
            'horario':             d.horario or '',
            'localidad':           d.localidad or '',
            'provincia':           d.provincia or '',
            'tango':               d.tango or '',
            'tienda':              d.tienda or '',
            'integra_vtex':        d.integra_vtex or '',
            'deposito':            d.deposito or '',
            'retiro_expres':       d.retiro_expres or '',
            'nro_sucursal_madre':   d.nro_sucursal_madre,
            'nro_sucursal_anterior': d.nro_sucursal_anterior,
            # Campos sensibles: solo incluidos para admin / soporteExt
            **({'base_nombre':   d.base_nombre or '',
                'conexion_dns':  d.conexion_dns or '',
                'n_llave_tango': d.n_llave_tango or ''}
               if puede_ver_tecnico else {}),
        })

    return JsonResponse({'sucursales': data, 'total': len(data)})

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
