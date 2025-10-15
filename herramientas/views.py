import pprint
import logging
import os
from django.conf import settings
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
# from Transportes.models import Transporte
# from Transportes.forms import TransporteForm
from django.views import View
from django.views.generic.list import ListView
from apps.settingsUrls import *
from consultasTango.forms import TurnoForm,TurnoEditForm,CodigoErrorForm,CategoriaForm, SubcategoriaForm, RelacionForm
from consultasTango.models import Turno,CodigosError
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import openpyxl
import pandas as pd
import json
from apps.home.SQL.Sql_Tango import * # Keep SQL imports
from apps.home.SQL.Sql_WMS import * # Keep SQL imports
import xlwt # Keep excel writing imports
import xlrd # Keep excel reading imports
from numpy import int64, isnan # Keep numpy imports


# @login_required(login_url="/login/")
# def (request):
#     Nombre=''
#     dir_iframe = DIR_HERAMIENTAS['']
#     return render(request,'home/PlantillaHerramientas.html',{'dir_iframe':dir_iframe,'Nombre':Nombre})


# Logistica

@login_required(login_url="/login/")
def RemisionMasiva(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['RemisionMasiva']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def ImprimirEtiquetasBultos(request):
    Nombre = 'Imprimir Etiquetas Bultos'
    dir_iframe = DIR_HERAMIENTAS['ImprimirEtiquetasBultos']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def CargaAnticipoGrupo(request):
    Nombre = 'Carga de anticipos'
    dir_iframe = DIR_HERAMIENTAS['CargaAnticipoGrupo']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def registro_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('herramientas:listado_turnos') # Updated redirect
    else:
        form = TurnoForm()

    return render(request, 'appConsultasTango/registro_turno.html', {'form': form, 'Nombre': 'Registro de Turno'})

@login_required(login_url="/login/")
def get_nombre_proveedor(request):
    codigo_proveedor = request.GET.get('codigo', '')
    # Aquí deberías implementar la lógica para obtener el nombre del proveedor
    # Por ahora, usaremos un diccionario de ejemplo
    proveedores = {
        'AGODIF': 'DI FALCO MARIO DI FALCO JOSE Y DI FALCO COSME SOC DE HECHO',
        'BFBISE': 'BANCO MACRO S.A.',
        # ... Añade el resto de los proveedores aquí
    }
    nombre_proveedor = proveedores.get(codigo_proveedor, '')
    return JsonResponse({'nombre': nombre_proveedor})

@login_required(login_url="/login/")
def listado_turnos(request):
    turnos = Turno.objects.all().order_by('-FechaAsignacion')
    for turno in turnos:
        turno.progreso = calcular_progreso(turno)
        turno.save()
    nombre_template = 'Listado de Turnos'
    return render(request, 'appConsultasTango/listado_turnos.html', {'turnos': turnos,'Nombre':nombre_template})

def eliminar_turno(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)
    if request.method == 'POST':
        turno.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def calcular_progreso(turno):
    total_steps = 3
    completed_steps = sum([turno.Recepcionado, turno.Auditado, turno.Posicionado])
    return int((completed_steps / total_steps) * 100)

def ver_turno(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)

    codigo_proveedor = turno.CodigoProveedor
    proveedores = {
        'AGODIF': 'DI FALCO MARIO DI FALCO JOSE Y DI FALCO COSME SOC DE HECHO',
        'BFBISE': 'BANCO MACRO S.A.',
        'OGPACK':'Tasky',
    }
    nombre_proveedor = proveedores.get(codigo_proveedor, 'Nombre Proveedor')

    # Asignar NombreProveedor AL OBJETO turno
    turno.NombreProveedor = nombre_proveedor

    timeline = [
        {
            'estado': 'Recepcionado',
            'completado': turno.Recepcionado,
            'fecha': turno.RecepcionadoFechaHora
        },
        {
            'estado': 'Auditado',
            'completado': turno.Auditado,
            'fecha': turno.AuditadoFechaHora
        },
        {
            'estado': 'Posicionado',
            'completado': turno.Posicionado,
            'fecha': turno.PosicionadoFechaHora
        }
    ]

    context = {
        'turno': turno,
        'timeline': timeline,
        'Nombre': 'Ver Turno'
    }

    return render(request, 'appConsultasTango/ver_turno.html', context)


def editar_turno(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)
    if request.method == 'POST':
        form = TurnoEditForm(request.POST, instance=turno)
        if form.is_valid():
            turno = form.save(commit=False)

            # Actualizar las fechas de los estados
            if turno.Recepcionado and not turno.RecepcionadoFechaHora:
                turno.RecepcionadoFechaHora = timezone.now()
            if turno.Auditado and not turno.AuditadoFechaHora:
                turno.AuditadoFechaHora = timezone.now()
            if turno.Posicionado and not turno.PosicionadoFechaHora:
                turno.PosicionadoFechaHora = timezone.now()

            turno.save()
            return redirect('herramientas:ver_turno', turno_id=turno.IdTurno) # Updated redirect
    else:
        form = TurnoEditForm(instance=turno)

    return render(request, 'appConsultasTango/editar_turno.html', {'form': form, 'turno': turno, 'Nombre': 'Editar Turno'})

def lista_codigos_error(request):
    codigos = CodigosError.objects.all().order_by('CodigoError')
    nombre_template = 'Listado de Códigos de Error'
    return render(request, 'appConsultasTango/lista_codigos_error.html', {'codigos': codigos, 'Nombre': nombre_template})

def crear_codigo_error(request):
    if request.method == 'POST':
        form = CodigoErrorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Código de error creado exitosamente.')
            return redirect('herramientas:lista_codigos_error') # Updated redirect
    else:
        form = CodigoErrorForm()
    return render(request, 'appConsultasTango/crear_editar_codigo_error.html', {'form': form, 'accion': 'Crear', 'Nombre': 'Crear Código de Error'})

def editar_codigo_error(request, codigo_id):
    codigo = get_object_or_404(CodigosError, pk=codigo_id)
    if request.method == 'POST':
        form = CodigoErrorForm(request.POST, instance=codigo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Código de error actualizado exitosamente.')
            return redirect('herramientas:lista_codigos_error') # Updated redirect
    else:
        form = CodigoErrorForm(instance=codigo)
    return render(request, 'appConsultasTango/crear_editar_codigo_error.html', {'form': form, 'accion': 'Editar', 'Nombre': 'Editar Código de Error'})

def eliminar_codigo_error(request, codigo_id):
    codigo = get_object_or_404(CodigosError, pk=codigo_id)
    if request.method == 'POST':
        codigo.delete()
        messages.success(request, 'Código de error eliminado exitosamente.')
        return redirect('herramientas:lista_codigos_error') # Updated redirect
    nombre_template = 'Eliminar Código de Error'
    return render(request, 'appConsultasTango/confirmar_eliminar_codigo_error.html', {'codigo': codigo, 'Nombre': nombre_template})

logger = logging.getLogger(__name__)

# @login_required(login_url="/login/")
# @method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(View):
    @method_decorator(login_required(login_url="/login/"))
    @method_decorator(csrf_exempt)
    def get(self, request):
        return render(request, 'appConsultasTango/uploadImg.html')

    @method_decorator(login_required(login_url="/login/"))
    @method_decorator(csrf_exempt)
    def post(self, request):
        if not request.FILES:
            logger.warning("No files received in POST request.")
            return JsonResponse({'error': 'No se recibió ningún archivo'}, status=400)

        file_key = next(iter(request.FILES), None)
        if not file_key:
            logger.warning("File key not found in request.FILES.")
            return JsonResponse({'error': 'Formato de archivo incorrecto o no se encontró el archivo'}, status=400)

        f = request.FILES.get(file_key)

        if not f:
            logger.warning(f"No file found for key: {file_key}")
            return JsonResponse({'error': 'No se encontró el archivo en la solicitud'}, status=400)

        try:
            file_path = os.path.join(settings.MEDIA_ROOT, 'imgTempEcommerce', f.name)
            counter = 1
            name, extension = os.path.splitext(f.name)
            while os.path.exists(file_path):
                file_path = os.path.join(settings.MEDIA_ROOT, 'imgTempEcommerce', f"{name}_{counter}{extension}")
                counter += 1

            with open(file_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            logger.info(f"Successfully saved file: {f.name} to {file_path}")

            # --- CAMBIO AQUÍ: Asegurar que siempre se incluya la información del archivo ---
            # return JsonResponse({
            #     'message': 'Imagen cargada con éxito',
            #     'filename': f.name, # Envía el nombre del archivo específico
            #     'filepath': file_path.replace(settings.MEDIA_ROOT, '') # Opcional: ruta relativa si es útil
            # })
            # --- CAMBIO AQUÍ: Simplificar la respuesta JSON para Dropzone ---
            # Dropzone es bastante flexible con respuestas 200, un JSON vacío
            # o simple a menudo funciona mejor para marcar el éxito.
            return JsonResponse({'message': 'success'}, status=200) # O simplemente {}
            # return JsonResponse({}, status=200) # Esto también debería funcionar

        except Exception as e:
            logger.error(f"Error processing file {f.name}: {e}", exc_info=True)
            return JsonResponse({'error': f'Error al procesar la imagen {f.name}', 'details': str(e)}, status=500)

@login_required(login_url="/login/")
def upload_success(request):
    return render(request, 'appConsultasTango/successImg.html')

# ***************************
# ***************************

@login_required(login_url="/login/")
def Eliminar_Turno(request):
    if request.method == 'POST':
        IdTurno = request.POST.get('IdTurno')
        datos = Turno.objects.get(IdTurno=IdTurno)
        datos.delete()
        # Redirigir a la página de éxito
        return redirect('herramientas:Listar_turno') # Updated redirect
    else:
        IdTurno = request.GET.get('IdTurno')
        datos = Turno.objects.get(IdTurno=IdTurno)
        return render(request, 'appConsultasTango/Eliminar_turno.html', {'datos': datos})

@login_required(login_url="/login/")
def Editar_Turno(request,IdTurno):
    datos = Turno.objects.get(IdTurno=IdTurno)
    if request.method == 'POST':
        form = TurnoForm(request.POST or None, request.FILES or None, instance=datos)
        if form.is_valid():
            form.save()
            # Redirigir a la página de éxito
            return redirect('herramientas:Listar_turno') # Updated redirect
    else:
        form = TurnoForm(instance=datos)
    return render(request, 'appConsultasTango/Editar_turno.html', {'form': form})

@login_required(login_url="/login/")
def Listar_turno(request):
    datos = Turno.objects.all()
    return render(request,'appConsultasTango/turno_list.html', {'turnos': datos})

@login_required(login_url="/login/")
def Crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a la página de éxito
            return redirect('herramientas:Listar_turno') # Updated redirect
    else:
        form = TurnoForm()
    return render(request, 'appConsultasTango/Crear_turno.html', {'form': form})


@login_required(login_url="/login/")
def Gestion_cronograma(request):
    Nombre = 'Gestión cronograma'
    dir_iframe = DIR_HERAMIENTAS['Gestion_cronograma']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


@login_required(login_url="/login/")
def Gestion_guias_mayoristas(request):
    Nombre = 'Guías mayoristas'
    dir_iframe = DIR_HERAMIENTAS['Gestion_guias_mayoristas']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def ImpRotulos(request):
    Nombre = 'Imprecion de Rotulos'
    dir_iframe = DIR_HERAMIENTAS['ImpRotulos']
    # return redirect(dir_iframe)
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def ImpRemEcom(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['ImportarRemEcommerce']
    # return redirect(dir_iframe)
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


# Abastecimiento

@login_required(login_url="/login/")
def StockBase(request):
    Nombre = 'Stock Base'
    dir_iframe = DIR_HERAMIENTAS['StockBase']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def MedidasLocales(request):
    Nombre = 'Medidas Locales'
    dir_iframe = DIR_HERAMIENTAS['MedidasLocales']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Recodificacion(request):
    Nombre = 'Recodificacion Outlet'
    dir_iframe = DIR_HERAMIENTAS['Recodificacion']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def Stock_excluido(request):
    Nombre = 'Stock excluido'
    dir_iframe = DIR_HERAMIENTAS['Stock_excluido']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


@login_required(login_url="/login/")
def Carga_de_orden(request):
    Nombre = 'Carga de orden'
    dir_iframe = DIR_HERAMIENTAS['Carga_de_orden']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


@login_required(login_url="/login/")
def Activar_orden(request):
    Nombre = 'Activar orden'
    dir_iframe = DIR_HERAMIENTAS['Activar_orden']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


@login_required(login_url="/login/")
def Desactivar_orden(request):
    Nombre = 'Desactivar orden'
    dir_iframe = DIR_HERAMIENTAS['Desactivar_orden']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def AltaPromoBancaria(request):
    Nombre = 'AltaPromoBancaria'
    dir_iframe = DIR_HERAMIENTAS['AltaPromoBancaria']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def CrearGrupoPromo(request):
    Nombre = 'CrearGrupoPromo'
    dir_iframe = DIR_HERAMIENTAS['CrearGrupoPromo']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def EditarGrupoPromo(request):
    Nombre = 'EditarGrupoPromo'
    dir_iframe = DIR_HERAMIENTAS['EditarGrupoPromo']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def MaestroDestinos(request):
    Nombre = 'MaestroDestinos'
    dir_iframe = DIR_HERAMIENTAS['MaestroDestinos']
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def GestionEquivalentes(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['GestionEquivalentes']
    return redirect(dir_iframe)

# Comercial
@login_required(login_url="/login/")
def Gestion_categoria_productos(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['Gestion_categoria_productos'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def AdministrarCuotas(request):
    Nombre = 'Administrar Cuotas'
    dir_iframe = DIR_HERAMIENTAS['AdministrarCuotas'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def AdministrarInternos(request):
    Nombre = 'Administrar Internos'
    dir_iframe = DIR_HERAMIENTAS['AdministrarInternos'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })


@login_required(login_url="/login/")
def PromoBancos(request):
    Nombre = 'Promo Bancos'
    dir_iframe = DIR_HERAMIENTAS['PromoBancos'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def AltaNuevosLocales(request):
    Nombre = 'Alta de Nuevos Locales'
    dir_iframe = DIR_HERAMIENTAS['AltaNuevosLocales'] #+ UserName
    # return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def UsuariosFranquicias(request):
    Nombre = 'Usuarios de Franquicias'
    dir_iframe = DIR_HERAMIENTAS['UsuariosFranquicias'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def ObjetivosVentaFranquicias(request):
    Nombre = 'Objetivos Ventas Franquicias'
    dir_iframe = DIR_HERAMIENTAS['ObjetivosVentaFranquicias'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

# Mayoristas
@login_required(login_url="/login/")
def Adm_Pedido(request):
    Nombre = 'Adm Pedido'
    dir_iframe = DIR_HERAMIENTAS['Adm_Pedido']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

# Ecommerce

# --- Categorías ---
@login_required(login_url="/login/")
def categoria_list(request):
    categorias = obtener_categorias()
    paginator = Paginator(categorias, 10)  # Muestra 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'appConsultasTango/ecommerce/categorias/categoria_list.html', {'page_obj': page_obj})

@login_required(login_url="/login/")
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            crear_categoria(form.cleaned_data['nombre'], form.cleaned_data['codigo'], form.cleaned_data['PalabrasClave'])
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('herramientas:categoria_list') # Updated redirect
    else:
        form = CategoriaForm()
    return render(request, 'appConsultasTango/ecommerce/categorias/categoria_create.html', {'form': form})

@login_required(login_url="/login/")
def categoria_update(request, id_categoria):
    categoria = obtener_categoria(id_categoria)
    if not categoria:
        messages.error(request, 'Categoría no encontrada.')
        return redirect('herramientas:categoria_list') # Updated redirect
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            editar_categoria(id_categoria, form.cleaned_data['nombre'], form.cleaned_data['codigo'], form.cleaned_data['PalabrasClave'])
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('herramientas:categoria_list') # Updated redirect
    else:
        form = CategoriaForm(initial={'nombre': categoria[1], 'codigo': categoria[2], 'PalabrasClave': categoria[3]})
    return render(request, 'appConsultasTango/ecommerce/categorias/categoria_update.html', {'form': form, 'id_categoria': id_categoria})

@login_required(login_url="/login/")
def categoria_delete(request, id_categoria):
    categoria = obtener_categoria(id_categoria)
    if not categoria:
        messages.error(request, 'Categoría no encontrada.')
        return redirect('herramientas:categoria_list') # Updated redirect
    if request.method == 'POST':
         eliminar_categoria(id_categoria)
         messages.success(request, 'Categoría eliminada exitosamente.')
         return redirect('herramientas:categoria_list') # Updated redirect
    return render(request, 'appConsultasTango/ecommerce/categorias/categoria_delete.html', {'categoria': categoria})

# --- Subcategorías ---
@login_required(login_url="/login/")
def subcategoria_list(request):
    subcategorias = obtener_subcategorias()
    # paginator = Paginator(subcategorias, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'appConsultasTango/ecommerce/subcategorias/subcategoria_list.html', {'page_obj': subcategorias})


@login_required(login_url="/login/")
def subcategoria_create(request):
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            crear_subcategoria(form.cleaned_data['codigo'], form.cleaned_data['nombre'],
                               form.cleaned_data['Keywords'], form.cleaned_data['id_categoria_VtxAr'],form.cleaned_data['id_categoria_Tango'])
            messages.success(request, 'Subcategoría creada exitosamente.')
            return redirect('herramientas:subcategoria_list') # Updated redirect
    else:
        form = SubcategoriaForm()
    return render(request, 'appConsultasTango/ecommerce/subcategorias/subcategoria_create.html', {'form': form})

@login_required(login_url="/login/")
def subcategoria_update(request, id_subcategoria):
    subcategoria = obtener_subcategoria(id_subcategoria)
    if not subcategoria:
        messages.error(request, 'Subcategoría no encontrada.')
        return redirect('herramientas:subcategoria_list') # Updated redirect
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
             editar_subcategoria(id_subcategoria, form.cleaned_data['codigo'], form.cleaned_data['nombre'],
                               form.cleaned_data['Keywords'], form.cleaned_data['id_categoria_VtxAr'],form.cleaned_data['id_categoria_Tango'])

             messages.success(request, 'Subcategoría actualizada exitosamente.')
             return redirect('herramientas:subcategoria_list') # Updated redirect
    else:
          form = SubcategoriaForm(initial={'codigo': subcategoria[1],'nombre': subcategoria[2],'Keywords': subcategoria[3],'id_categoria_VtxAr': subcategoria[4],'id_categoria_Tango': subcategoria[5]})
    return render(request, 'appConsultasTango/ecommerce/subcategorias/subcategoria_update.html', {'form': form, 'id_subcategoria': id_subcategoria})

@login_required(login_url="/login/")
def subcategoria_delete(request, id_subcategoria):
    subcategoria = obtener_subcategoria(id_subcategoria)
    if not subcategoria:
        messages.error(request, 'Subcategoría no encontrada.')
        return redirect('herramientas:subcategoria_list') # Updated redirect
    if request.method == 'POST':
         eliminar_subcategoria(id_subcategoria)
         messages.success(request, 'Subcategoría eliminada exitosamente.')
         return redirect('herramientas:subcategoria_list') # Updated redirect
    return render(request, 'appConsultasTango/ecommerce/subcategorias/subcategoria_delete.html', {'subcategoria': subcategoria})

# --- Relaciones ---
@login_required(login_url="/login/")
def relacion_list(request):
    relaciones = obtener_relaciones()
    # paginator = Paginator(relaciones, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'appConsultasTango/ecommerce/relaciones/relacion_list.html', {'page_obj': relaciones})

@login_required(login_url="/login/")
def relacion_create(request):
    if request.method == 'POST':
        form = RelacionForm(request.POST)
        if form.is_valid():
            crear_relacion(form.cleaned_data['id_categoria_Tango'], form.cleaned_data['id_subCat_VtxAr'])
            messages.success(request, 'Relación creada exitosamente.')
            return redirect('herramientas:relacion_list') # Updated redirect
    else:
        form = RelacionForm()
    return render(request, 'appConsultasTango/ecommerce/relaciones/relacion_create.html', {'form': form})


@login_required(login_url="/login/")
def relacion_update(request, id_categoria_tango,id_subcategoria):
    relacion = obtener_relacion(id_categoria_tango,id_subcategoria)
    if not relacion:
        messages.error(request, 'Relación no encontrada.')
        return redirect('herramientas:relacion_create') # Updated redirect
    if request.method == 'POST':
        form = RelacionForm(request.POST)
        if form.is_valid():
             editar_relacion(id_categoria_tango,id_subcategoria,form.cleaned_data['id_categoria_Tango'], form.cleaned_data['id_subCat_VtxAr'])
             messages.success(request, 'Relación actualizada exitosamente.')
             return redirect('herramientas:relacion_list') # Updated redirect
    else:
        form = RelacionForm(initial={'id_categoria_Tango': relacion[0], 'id_subCat_VtxAr': relacion[1]})
    return render(request, 'appConsultasTango/ecommerce/relaciones/relacion_update.html', {'form': form, 'id_categoria_tango': id_categoria_tango,'id_subcategoria':id_subcategoria})


@login_required(login_url="/login/")
def relacion_delete(request, id_categoria_tango, id_subcategoria):
    relacion = obtener_relacion(id_categoria_tango,id_subcategoria)
    if not relacion:
        messages.error(request, 'Relación no encontrada.')
        return redirect('herramientas:relacion_list') # Updated redirect
    if request.method == 'POST':
        eliminar_relacion(id_categoria_tango, id_subcategoria)
        messages.success(request, 'Relación eliminada exitosamente.')
        return redirect('herramientas:relacion_list') # Updated redirect
    return render(request, 'appConsultasTango/ecommerce/relaciones/relacion_delete.html', {'relacion': relacion,'id_categoria_tango': id_categoria_tango, 'id_subcategoria': id_subcategoria})

@login_required(login_url="/login/")
def import_art_vtex(request):
    nombre_db='LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    print('Cambiando base de datos a ' + nombre_db)
    print('import_art_vtex')
    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            pfile = request.FILES['excel_file']
            filesys =FileSystemStorage()
            # Obtener el nombre del archivo sin espacios en blanco
            filename = pfile.name.replace(' ', '')

            # Guardar el archivo con el nombre sin espacios en blanco
            uploadfilename = filesys.save(filename, pfile)
            extension = os.path.splitext(uploadfilename)
            if  not extension[1] == '.xlsx':
                error_extension = 'El formato del archivo debe ser de tipo .xlsx'
                os.remove(filesys.path(uploadfilename))
                return render(request,'appConsultasTango/importFileArtVtex.html',{'mensaje_error':error_extension})

            uploaded_url = filesys.url(uploadfilename)  #Ruta donde se guardo el archivo
            uploaded_url = os.path.normpath(uploaded_url)
            # print("uploaded_url: " + uploaded_url)
            ruta_actual = os.path.join(os.getcwd()) #Ruta del proyecto
            # print('Ruta actual: ' + ruta_actual)
            path_filname = ruta_actual + uploaded_url
            wb = openpyxl.load_workbook(path_filname) #Abrimos el archivo
            worksheet = wb.active
            excel_data = list()
            enc_data = list()
            mensaje_error = ''
            mensaje_Success = ''
            art_valido = ''
            nombre_archivo = "AltaArtVtex.xls"
            eliminar_archivo_excel(nombre_archivo)
            # iterando sobre las filas y obteniendo
            # valor de cada celda en la fila
            for row in worksheet.iter_rows():
                fila = row[0].row   #Numero de fila
                row_data = list()
                talon_pedido = 0
                i = 1
                if worksheet.cell(row=fila, column=1).value is None: #Frena el loop al llegar al final de la lista
                    break

                for cell in row:
                    if fila == 1:
                        enc_data.append(str(cell.value))
                    else:
                        if worksheet.cell(row=1, column=i).value == 'ARTICULO':
                            if fila > 1:
                                articulo = worksheet.cell(row=fila, column=i).value
                                art_valido= validar_articulo(articulo)
                                print('art_valido: ' + str(art_valido))
                                if art_valido == 'ERROR':
                                    mensaje_error = 'Hay articulos que no existen en SJ_ETIQUETAS_FINAL'
                                    row_data.append('*' + str(cell.value) + '*')
                                    i += 1
                                    continue
                        elif worksheet.cell(row=1, column=i).value == 'DESCRIPCION':
                            worksheet.cell(row=fila, column=i).value = art_valido

                        if cell.value == None:
                            row_data.append(str(''))
                        else:
                            row_data.append(str(cell.value))
                    i += 1

                excel_data.append(row_data)
                if len(row_data) > 0:
                    resultado = json.loads(obtenerInformacionArticulo(row_data[0], row_data[2]))
                    crear_archivo_excel(resultado, nombre_archivo)

            wb.save(path_filname)
            if not(mensaje_error):
                mensaje_Success = 'Articulos cargados correctamente'
                os.remove(filesys.path(uploadfilename))
            else:
                os.remove(filesys.path(uploadfilename))

            return render(request, 'appConsultasTango/importFileArtVtex.html' ,{'enc_data':enc_data,'excel_data':excel_data,'mensaje_Success':mensaje_Success,'mensaje_error':mensaje_error})


    except Exception as identifier:
        print(identifier)
    return render(request,'appConsultasTango/importFileArtVtex.html',{})

import xlwt
import xlrd

def crear_archivo_excel(tempJson, nombre_archivo):
    # Construir la ruta absoluta del archivo
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, nombre_archivo)

    try:
        # Abrir el archivo de Excel existente
        libro_rd = xlrd.open_workbook(ruta_archivo)
        hoja_rd = libro_rd.sheet_by_index(0)
        ultima_fila = hoja_rd.nrows

        # Crear un nuevo objeto Workbook
        libro_wt = xlwt.Workbook()
        hoja_wt = libro_wt.add_sheet('Hoja 1')

        # Copiar los datos de la hoja existente a la nueva hoja
        for i in range(ultima_fila):
            for j in range(hoja_rd.ncols):
                hoja_wt.write(i, j, hoja_rd.cell_value(i, j))

        # Agregar los nuevos datos a la hoja
        for i, fila in enumerate(tempJson):
            for j, valor in enumerate(fila.values()):
                hoja_wt.write(ultima_fila + i, j, valor)

        # Guardar el libro en un archivo
        libro_wt.save(ruta_archivo)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo
        libro_wt = xlwt.Workbook()
        hoja_wt = libro_wt.add_sheet('Hoja 1')

        # Agregar los encabezados si es el primer registro
        if len(tempJson) > 0:
            encabezados = list(tempJson[0].keys())
            for i, encabezado in enumerate(encabezados):
                hoja_wt.write(0, i, encabezado)

        # Agregar los datos a la hoja
        for i, fila in enumerate(tempJson):
            for j, valor in enumerate(fila.values()):
                hoja_wt.write(i + 1, j, valor)

        # Guardar el libro en un archivo
        libro_wt.save(ruta_archivo)

def eliminar_archivo_excel(nombre_archivo):
    # Construir la ruta absoluta del archivo
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    print('ruta_archivo: ' + ruta_archivo)
    # Verificar si el archivo existe y eliminarlo si es así
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        print('Se elimino el archivo ' + nombre_archivo)

@login_required(login_url="/login/")
def Control_pedidos(request):
    Nombre = 'Control pedidos'
    dir_iframe = DIR_HERAMIENTAS['Control_pedidos']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })


@login_required(login_url="/login/")
def StockSegVtex(request):
    Nombre = 'Adm. Stock Seguridad Vtex'
    dir_iframe = DIR_HERAMIENTAS['StockSegVtex']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe, })

@login_required(login_url="/login/")
def novICBC(request):
    Nombre = 'Actualizar novedades ICBC'
    dir_iframe = DIR_HERAMIENTAS['novICBC']
    # return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})
    return redirect(dir_iframe)

# Gerencia
@login_required(login_url="/login/")
def rendircobranzas(request,UserName):
    Nombre = 'Rendir Cobranzas'
    dir_iframe = DIR_HERAMIENTAS['rendircobranzas'] + UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def GestionarCobro(request,UserName):
    Nombre = 'Gestionar Cobro'
    dir_iframe = DIR_HERAMIENTAS['gestionarCobro'] + UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def RegistrarEfectivo(request,UserName):
    Nombre = 'Registrar Efectivo'
    dir_iframe = DIR_HERAMIENTAS['registrarEfectivo'] + UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def gestionPremiosComercial(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['gestionPremiosComercial']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

# Administracion

@login_required(login_url="/login/")
def EgresosCajaTesoreria(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['EgresosCajaTesoreria'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def CargaFacturasSuc(request):
    Nombre = 'Carga Facturas Suc'
    dir_iframe = DIR_HERAMIENTAS['CargaFacturasSuc'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def CargaContratosFr(request):
    Nombre = 'Carga Contratos Franquicias'
    dir_iframe = DIR_HERAMIENTAS['CargaContratosFr'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def ControlGastosSupervision(request):
    Nombre = 'Gastos Supervision'
    dir_iframe = DIR_HERAMIENTAS['ControlGastosSupervision'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def ControlMasivoCobranza(request):
    Nombre = 'Control Gastos'
    dir_iframe = DIR_HERAMIENTAS['ControlMasivoCobranza'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Controlgastos(request):
    Nombre = 'Control Gastos'
    dir_iframe = DIR_HERAMIENTAS['controlGastos'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Cargargastos(request):
    Nombre = 'Gestionar Cobro'
    dir_iframe = DIR_HERAMIENTAS['cargaGastos'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def Controlcajasdiario(request):
    Nombre = 'Control cajas Diario'
    dir_iframe = DIR_HERAMIENTAS['Controlcajasdiario'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def CargaGastosAlquileres(request):
    Nombre = 'Carga Gastos Alquileres'
    dir_iframe = DIR_HERAMIENTAS['CargaGastosAlquileres'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def GestionDeAlquileres(request):
    Nombre = 'Gestión % De Alquileres'
    dir_iframe = DIR_HERAMIENTAS['GestionDeAlquileres'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def ControlEgresosDeCaja(request,UserName):
    Nombre = 'Control Egresos De Caja'
    dir_iframe = DIR_HERAMIENTAS['ControlEgresosDeCaja'] + UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def CargarContratosDeAlquiler(request):
    Nombre = 'Cargar Contratos De Alquiler'
    dir_iframe = DIR_HERAMIENTAS['CargarContratosDeAlquiler'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def RelacionesCtaCont(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['RelacionesCtaCont'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def GestionDeProveedores(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['GestionDeProveedores'] #+ UserName
    return redirect(dir_iframe)

# Administracion_CE             ***Comercio Exterior***
@login_required(login_url="/login/")
def Cargarcontenedor(request):
    Nombre = 'Cargar Contenedor'
    dir_iframe = DIR_HERAMIENTAS['cargaInicial'] #+ UserName
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def EditarContenedor(request):
    Nombre = 'Editar Contenedor'
    dir_iframe = DIR_HERAMIENTAS['mostrarOrden'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

# RRHH

@login_required(login_url="/login/")
def CargaAnticipo(request):
    Nombre = 'Carga de anticipos'
    dir_iframe = DIR_HERAMIENTAS['CargaAnticipo']
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre})

@login_required(login_url="/login/")
def altaVendedores(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['altaVendedores'] #+ UserName
    # return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    return redirect(dir_iframe)

@login_required(login_url="/login/")
def listarGrupos(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['listarGrupos'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })

@login_required(login_url="/login/")
def gestionarVendedores(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['gestionarVendedores'] #+ UserName
    # return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    return redirect(dir_iframe)

# @login_required(login_url="/login/")
# def adminEmpleados(request):
#     Nombre = ''
#     dir_iframe = DIR_HERAMIENTAS['adminEmpleados'] #+ UserName
#     return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
#     # return redirect(dir_iframe)

# Tesoreria

@login_required(login_url="/login/")
def ControlDeEfectivo(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['ControlDeEfectivo'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    # return redirect(dir_iframe)

# Supervisores

@login_required(login_url="/login/")
def CargaProyecto(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['CargaProyecto'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    # return redirect(dir_iframe)

# Admin

@login_required(login_url="/login/")
def AdminNotificaciones(request):
    Nombre = ''
    dir_iframe = DIR_HERAMIENTAS['AdminNotificaciones'] #+ UserName
    return render(request, 'home/PlantillaHerramientas.html', {'dir_iframe': dir_iframe,'Nombre':Nombre })
    # return redirect(dir_iframe)


# --- Moved from viewsExtras.py ---
@login_required(login_url="/login/")
def import_file_etiquetas(request):
    nombre_db='LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    print('Cambiando base de datos a ' + nombre_db)
    print('import_file_etiquetas')
    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            pfile = request.FILES['excel_file']
            filesys =FileSystemStorage()
            # Obtener el nombre del archivo sin espacios en blanco
            filename = pfile.name.replace(' ', '')

            # Guardar el archivo con el nombre sin espacios en blanco
            uploadfilename = filesys.save(filename, pfile)
            extension = os.path.splitext(uploadfilename)
            if  not extension[1] == '.xlsx':
                error_extension = 'El formato del archivo debe ser de tipo .xlsx'
                os.remove(filesys.path(uploadfilename))
                return render(request,'appConsultasTango/importFileEtiquetas.html',{'mensaje_error':error_extension})

            uploaded_url = filesys.url(uploadfilename)  #Ruta donde se guardo el archivo
            uploaded_url = os.path.normpath(uploaded_url)
            # print("uploaded_url: " + uploaded_url)
            ruta_actual = os.path.join(os.getcwd()) #Ruta del proyecto
            # print('Ruta actual: ' + ruta_actual)
            path_filname = ruta_actual + uploaded_url
            wb = openpyxl.load_workbook(path_filname) #Abrimos el archivo
            worksheet = wb.active
            excel_data = list()
            enc_data = list()
            mensaje_error = ''
            mensaje_Success = ''
            art_valido = ''
            # iterando sobre las filas y obteniendo
            # valor de cada celda en la fila
            for row in worksheet.iter_rows():
                fila = row[0].row   #Numero de fila
                row_data = list()
                talon_pedido = 0
                i = 1
                if worksheet.cell(row=fila, column=1).value is None: #Frena el loop al llegar al final de la lista
                    break

                for cell in row:
                    if fila == 1:
                        enc_data.append(str(cell.value))
                    else:
                        if worksheet.cell(row=1, column=i).value == 'ARTICULO':
                            if fila > 1:
                                articulo = worksheet.cell(row=fila, column=i).value
                                art_valido= validar_articulo(articulo)
                                if art_valido == 'ERROR':
                                    mensaje_error = 'Hay articulos que no existen en SJ_ETIQUETAS_FINAL'
                                    row_data.append('*' + str(cell.value) + '*')
                                    i += 1
                                    continue
                        elif worksheet.cell(row=1, column=i).value == 'DESCRIPCION':
                            worksheet.cell(row=fila, column=i).value = art_valido

                        if cell.value == None:
                            row_data.append(str(''))
                        else:
                            row_data.append(str(cell.value))
                    i += 1

                excel_data.append(row_data)

            # print('path_filname: ' + path_filname)
            wb.save(path_filname)
            if not(mensaje_error):
                upload_file_artEtiquetas(path_filname) #Carga articulos en base de datos
                mensaje_Success = 'Articulos cargados correctamente'
                os.remove(filesys.path(uploadfilename))

            else:
                os.remove(filesys.path(uploadfilename))


            return render(request, 'appConsultasTango/importFileEtiquetas.html' ,{'enc_data':enc_data,'excel_data':excel_data,'mensaje_Success':mensaje_Success,'mensaje_error':mensaje_error})


    except Exception as identifier:
        print(identifier)
    return render(request,'appConsultasTango/importFileEtiquetas.html',{})

def upload_file_artEtiquetas(path_filname):
    excel_file =path_filname
    empexceldata = pd.read_excel(excel_file, engine='openpyxl')
    dbframe = empexceldata
    borrar_contTabla('SJ_T_ETIQUETAS_FINAL')

    for df in dbframe.itertuples():
        articulo = str(df.ARTICULO)
        descripcion = str(df.DESCRIPCION)
        cargar_articulo(articulo,descripcion)

@login_required(login_url="/login/")
def import_file_cierrePedidos(request):
    nombre_db='LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    print('Cambiando base de datos a ' + nombre_db)
    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            pfile = request.FILES['excel_file']
            filesys =FileSystemStorage()
            # Obtener el nombre del archivo sin espacios en blanco
            filename = pfile.name.replace(' ', '')

            # Guardar el archivo con el nombre sin espacios en blanco
            uploadfilename = filesys.save(filename, pfile)
            extension = os.path.splitext(uploadfilename)
            if  not extension[1] == '.xlsx':
                error_extension = 'El formato del archivo debe ser de tipo .xlsx'
                os.remove(filesys.path(uploadfilename))
                return render(request,'appConsultasTango/importFilePedidosCierre.html',{'mensaje_error':error_extension})

            uploaded_url = filesys.url(uploadfilename)  #Ruta donde se guardo el archivo
            uploaded_url = os.path.normpath(uploaded_url)
            # print("uploaded_url: " + uploaded_url)
            ruta_actual = os.path.join(os.getcwd()) #Ruta del proyecto
            # print('Ruta actual: ' + ruta_actual)
            path_filname = ruta_actual + uploaded_url
            wb = openpyxl.load_workbook(path_filname) #Abrimos el archivo
            worksheet = wb.active
            excel_data = list()
            enc_data = list()
            mensaje_error = ''
            mensaje_Success = ''
            # iterando sobre las filas y obteniendo
            # valor de cada celda en la fila
            for row in worksheet.iter_rows():
                fila = row[0].row   #Numero de fila
                row_data = list()
                talon_pedido = 0
                i = 1
                if worksheet.cell(row=fila, column=1).value is None: #Frena el loop al llegar al final de la lista
                    break
                
                for cell in row:
                    if fila == 1:
                        enc_data.append(str(cell.value))
                    else:
                        if worksheet.cell(row=1, column=i).value == 'NRO_PEDIDO':
                            if fila > 1:
                                pedido = worksheet.cell(row=fila, column=i).value
                                if worksheet.cell(row=1, column=6).value == 'TALON_PED':
                                    talon_pedido = worksheet.cell(row=fila, column=6).value

                                ped_valido= validar_pedido(pedido,str(talon_pedido))
                                # print('ped_valido: ' + str(ped_valido))
                                if ped_valido == 0:
                                    mensaje_error = 'Los Pedidos NO EXISTEN  o NO ESTAN PENDIENTES'
                                    row_data.append('*' + str(cell.value) + '*')
                                    i += 1
                                    continue
                        if cell.value == None:
                            row_data.append(str(''))
                        else:
                            row_data.append(str(cell.value))                        
                    i += 1

                excel_data.append(row_data)

            # print('path_filname: ' + path_filname)
            wb.save(path_filname)
            if not(mensaje_error):
                upload_file_CierrePedidos(path_filname) #Ejecuta ejuste en base de datos
                mensaje_Success = 'Articulos cargados correctamente'
                os.remove(filesys.path(uploadfilename))
                
            else:
                os.remove(filesys.path(uploadfilename))

            
            return render(request, 'appConsultasTango/importFilePedidosCierre.html' ,{'enc_data':enc_data,'excel_data':excel_data,'mensaje_Success':mensaje_Success,'mensaje_error':mensaje_error})


    except Exception as identifier:            
        print(identifier)
    return render(request,'appConsultasTango/importFilePedidosCierre.html',{})

@login_required(login_url="/login/")
def import_file_cierrePedidosUY(request):
    nombre_db='TASKY_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    print('Cambiando base de datos a ' + nombre_db)
    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            pfile = request.FILES['excel_file']
            filesys =FileSystemStorage()
            # Obtener el nombre del archivo sin espacios en blanco
            filename = pfile.name.replace(' ', '')

            # Guardar el archivo con el nombre sin espacios en blanco
            uploadfilename = filesys.save(filename, pfile)
            extension = os.path.splitext(uploadfilename)
            if  not extension[1] == '.xlsx':
                error_extension = 'El formato del archivo debe ser de tipo .xlsx'
                os.remove(filesys.path(uploadfilename))
                return render(request,'appConsultasTango/importFilePedidosCierreUY.html',{'mensaje_error':error_extension})

            uploaded_url = filesys.url(uploadfilename)  #Ruta donde se guardo el archivo
            uploaded_url = os.path.normpath(uploaded_url)
            # print("uploaded_url: " + uploaded_url)
            ruta_actual = os.path.join(os.getcwd()) #Ruta del proyecto
            # print('Ruta actual: ' + ruta_actual)
            path_filname = ruta_actual + uploaded_url
            wb = openpyxl.load_workbook(path_filname) #Abrimos el archivo
            worksheet = wb.active
            excel_data = list()
            enc_data = list()
            mensaje_error = ''
            mensaje_Success = ''
            # iterando sobre las filas y obteniendo
            # valor de cada celda en la fila
            for row in worksheet.iter_rows():
                fila = row[0].row   #Numero de fila
                row_data = list()
                talon_pedido = 0
                i = 1
                if worksheet.cell(row=fila, column=1).value is None: #Frena el loop al llegar al final de la lista
                    break
                
                for cell in row:
                    if fila == 1:
                        enc_data.append(str(cell.value))
                    else:
                        if worksheet.cell(row=1, column=i).value == 'NRO_PEDIDO':
                            if fila > 1:
                                pedido = worksheet.cell(row=fila, column=i).value
                                if worksheet.cell(row=1, column=6).value == 'TALON_PED':
                                    talon_pedido = worksheet.cell(row=fila, column=6).value

                                ped_valido= validar_pedido(pedido,str(talon_pedido))
                                # print('ped_valido: ' + str(ped_valido))
                                if ped_valido == 0:
                                    mensaje_error = 'Los Pedidos NO EXISTEN  o NO ESTAN PENDIENTES'
                                    row_data.append('*' + str(cell.value) + '*')
                                    i += 1
                                    continue
                        if cell.value == None:
                            row_data.append(str(''))
                        else:
                            row_data.append(str(cell.value))                        
                    i += 1

                excel_data.append(row_data)

            # print('path_filname: ' + path_filname)
            wb.save(path_filname)
            if not(mensaje_error):
                upload_file_CierrePedidos(path_filname) #Ejecuta ejuste en base de datos
                mensaje_Success = 'Pedidos anulados correctamente'
                os.remove(filesys.path(uploadfilename))
                
            else:
                os.remove(filesys.path(uploadfilename))

            
            return render(request, 'appConsultasTango/importFilePedidosCierreUY.html' ,{'enc_data':enc_data,'excel_data':excel_data,'mensaje_Success':mensaje_Success,'mensaje_error':mensaje_error})


    except Exception as identifier:            
        print(identifier)
    return render(request,'appConsultasTango/importFilePedidosCierreUY.html',{})

def upload_file_CierrePedidos(path_filname):
    excel_file =path_filname
    empexceldata = pd.read_excel(excel_file, engine='openpyxl')
    dbframe = empexceldata
    for df in dbframe.itertuples():
        
        numero_pedido = ' 0000' + str(df.NRO_PEDIDO)[-9:]  #Toma los ultimos 9 digitos del numero de pedido
        talon_pedido = str(df.TALON_PED)

        # if type(numero_pedido) == int:
        #     pedido = ' 0000' + numero_pedido
        # else:
        #     pedido = numero_pedido
        #     print('Dato sin concatenar')
        
        cerrar_pedido(talon_pedido,numero_pedido)


@login_required(login_url="/login/")
def import_file_ubi(request):
    try:
        if request.method == 'POST' and request.FILES['excel_file']:
            pfile = request.FILES['excel_file']
            filesys =FileSystemStorage()
            uploadfilename = filesys.save(pfile.name,pfile) #Nombre del archivo
            extension = os.path.splitext(uploadfilename)
            if  not extension[1] == '.xlsx':
                error_extension = 'El formato del archivo debe ser de tipo .xlsx'
                os.remove(filesys.path(uploadfilename))
                return render(request,'appConsultasWMS/importFileUbi.html',{'mensaje_error':error_extension})

            uploaded_url = filesys.url(uploadfilename)  #Ruta donde se guardo el archivo
            uploaded_url = os.path.normpath(uploaded_url)
            # print("uploaded_url: " + uploaded_url)
            ruta_actual = os.path.join(os.getcwd()) #Ruta del proyecto
            # print('Ruta actual: ' + ruta_actual)
            path_filname = ruta_actual + uploaded_url
            wb = openpyxl.load_workbook(path_filname) #Abrimos el archivo
            worksheet = wb.active
            worksheet.cell(row=1, column=15).value = 'id_Ubicacion'
            excel_data = list()
            enc_data = list()
            mensaje_error = ''
            mensaje_Success = ''
            # iterando sobre las filas y obteniendo
            # valor de cada celda en la fila
            for row in worksheet.iter_rows():
                fila = row[0].row   #Numero de fila
                row_data = list()
                i = 1
                if worksheet.cell(row=fila, column=1).value is None: #Frena el loop al llegar al final de la lista
                    break
                
                for cell in row:
                    
                    # if cell.value == None:
                    #     break
                    if fila == 1:
                        enc_data.append(str(cell.value))
                    else:
                        if worksheet.cell(row=1, column=i).value == 'Cod_Ubicacion':
                        # print('Valor en contrado en la fila: ' + str(fila) + ' y columna: ' + str(i))
                            if fila > 1:
                                ubi = worksheet.cell(row=fila, column=i).value
                                # print(ubi)
                                Id_ubicacion= validar_ubicacion(ubi)
                                # print(Id_ubicacion)
                                if Id_ubicacion == 0:
                                    mensaje_error = 'Una o mas ubicaciones no existen en la base de datos'
                                    row_data.append('*' + str(cell.value) + '*')
                                    i += 1
                                    # print('row_data Id_ubicacion == 0: ')
                                    # print(row_data)
                                    continue
                                else:
                                    worksheet.cell(row=fila, column=15).value = Id_ubicacion

                        if cell.value == None:
                            row_data.append(str(''))
                        else:
                            row_data.append(str(cell.value))                        
                    i += 1

                excel_data.append(row_data)

            # print('path_filname: ' + path_filname)
            wb.save(path_filname)
            if not(mensaje_error):
                mensaje_Success = 'Se importo correctamente el archivo'
                upload_file_ubi(path_filname) #Ejecuta ejuste en base de datos

            # os.remove(filesys.path(uploadfilename))
            return render(request, 'appConsultasWMS/importFileUbi.html' ,{'enc_data':enc_data,'excel_data':excel_data,'mensaje_Success':mensaje_Success,'mensaje_error':mensaje_error})

        if request.method == 'POST' and request.SUBMIT['Procesar']:
            print('Hola Mundo >>>>')

    except Exception as identifier:            
        print(identifier)
    return render(request,'appConsultasWMS/importFileUbi.html',{})

def upload_file_ubi(path_filname):
    excel_file =path_filname
    empexceldata = pd.read_excel(excel_file, engine='openpyxl')
    dbframe = empexceldata

    for df in dbframe.itertuples():
        id_Ubi = str(df.id_Ubicacion)
        nom_ubi = df.Nombre_Ubicacion
        tipo = df.Tipo_Ubicacion
        estado_ubi = df.Estado_U

        if isnan(df.Rack):
            orden_rack = 0
        else:
            orden_rack = int(df.Rack)

        if isnan(df.Modulo):
            orden_modulo = 0
        else:
            orden_modulo = int(df.Modulo)
        
        if isnan(df.Altura):
            orden_altura = 0
        else:
            orden_altura = int(df.Altura)
        
            
        
        actualizar_ubicacion(id_Ubi,nom_ubi,tipo,estado_ubi,orden_rack,orden_modulo,orden_altura)

# ========================================
# CRUD para EB_sincArt_volumen
# ========================================

from .forms import EBSincArtVolumenForm
from .sql_volumen import (
    obtener_articulos_volumen, 
    obtener_articulo_volumen_por_codigo,
    actualizar_articulo_volumen,
    crear_articulo_volumen,
    eliminar_articulo_volumen,
    buscar_articulos_volumen,
    obtener_rubros_disponibles
)
from .excel_utils import generar_plantilla_excel, procesar_archivo_excel
from django.http import HttpResponse
import io

@login_required(login_url="/login/")
def eb_sinc_art_volumen_list(request):
    """Lista todos los artículos de volumen con funcionalidad de búsqueda y filtros"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    search_term = request.GET.get('search', '')
    filtro_estado = request.GET.get('estado', '')
    filtro_rubro = request.GET.get('rubro', '')
    
    # Convertir filtro_estado a formato esperado por la función SQL
    estado_sql = None
    if filtro_estado == 'activo':
        estado_sql = 'activo'
    elif filtro_estado == 'inactivo':
        estado_sql = 'inactivo'
    
    if search_term:
        articulos = buscar_articulos_volumen(search_term, estado_sql, filtro_rubro or None)
    else:
        articulos = obtener_articulos_volumen(estado_sql, filtro_rubro or None)
    
    # Obtener rubros disponibles para el filtro
    rubros_disponibles = obtener_rubros_disponibles()
    
    # Paginación
    paginator = Paginator(articulos, 25)  # 25 artículos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'filtro_estado': filtro_estado,
        'filtro_rubro': filtro_rubro,
        'rubros_disponibles': rubros_disponibles,
        'total_articulos': len(articulos)
    }
    
    return render(request, 'herramientas/eb_sinc_art_volumen/list.html', context)

@login_required(login_url="/login/")
def eb_sinc_art_volumen_detail(request, cod_articulo):
    """Muestra los detalles de un artículo específico"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    articulo = obtener_articulo_volumen_por_codigo(cod_articulo)
    
    if not articulo:
        messages.error(request, 'Artículo no encontrado.')
        return redirect('herramientas:eb_sinc_art_volumen_list')
    
    return render(request, 'herramientas/eb_sinc_art_volumen/detail.html', {'articulo': articulo})

@login_required(login_url="/login/")
def eb_sinc_art_volumen_edit(request, cod_articulo):
    """Edita un artículo existente"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    articulo = obtener_articulo_volumen_por_codigo(cod_articulo)
    
    if not articulo:
        messages.error(request, 'Artículo no encontrado.')
        return redirect('herramientas:eb_sinc_art_volumen_list')
    
    if request.method == 'POST':
        form = EBSincArtVolumenForm(request.POST, initial_data=articulo)
        if form.is_valid():
            try:
                # Ahora guardamos directamente en cm (no hay conversión)
                datos_actualizados = {
                    'alto_embalaje': form.cleaned_data['alto_embalaje'],
                    'ancho_embalaje': form.cleaned_data['ancho_embalaje'],
                    'largo_embalaje': form.cleaned_data['largo_embalaje'],
                    'alto_real': form.cleaned_data['alto_real'],
                    'ancho_real': form.cleaned_data['ancho_real'],
                    'largo_real': form.cleaned_data['largo_real'],
                    'peso_embalaje': form.cleaned_data['peso_embalaje'],
                    'peso_real': form.cleaned_data['peso_real']
                }
                
                actualizar_articulo_volumen(cod_articulo, datos_actualizados)
                messages.success(request, f'Artículo {cod_articulo} actualizado exitosamente.')
                return redirect('herramientas:eb_sinc_art_volumen_detail', cod_articulo=cod_articulo)
                
            except Exception as e:
                messages.error(request, f'Error al actualizar el artículo: {str(e)}')
    else:
        form = EBSincArtVolumenForm(initial_data=articulo)
    
    context = {
        'form': form,
        'articulo': articulo,
        'cod_articulo': cod_articulo
    }
    
    return render(request, 'herramientas/eb_sinc_art_volumen/edit.html', context)

@login_required(login_url="/login/")
def eb_sinc_art_volumen_delete(request, cod_articulo):
    """Elimina un artículo"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    articulo = obtener_articulo_volumen_por_codigo(cod_articulo)
    
    if not articulo:
        messages.error(request, 'Artículo no encontrado.')
        return redirect('herramientas:eb_sinc_art_volumen_list')
    
    if request.method == 'POST':
        try:
            eliminar_articulo_volumen(cod_articulo)
            messages.success(request, f'Artículo {cod_articulo} eliminado exitosamente.')
            return redirect('herramientas:eb_sinc_art_volumen_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el artículo: {str(e)}')
    
    return render(request, 'herramientas/eb_sinc_art_volumen/delete.html', {'articulo': articulo})

@login_required(login_url="/login/")
def eb_sinc_art_volumen_descargar_plantilla(request):
    """Genera y descarga una plantilla Excel para carga masiva"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    try:
        # Usar la función simplificada que sabemos que funciona
        from .excel_utils_simple import generar_plantilla_excel_simple
        wb = generar_plantilla_excel_simple()
        
        # Usar BytesIO para manejar el contenido en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        content = output.getvalue()
        
        # Crear respuesta HTTP con archivo Excel
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="Plantilla_Volumenes_Articulos.xlsx"'
        response['Content-Length'] = str(len(content))
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error al generar la plantilla: {str(e)}')
        return redirect('herramientas:eb_sinc_art_volumen_list')

@login_required(login_url="/login/")
def eb_sinc_art_volumen_carga_masiva(request):
    """Maneja la carga masiva desde archivo Excel"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    if request.method == 'POST':
        if 'archivo_excel' not in request.FILES:
            messages.error(request, 'No se seleccionó ningún archivo.')
            return redirect('herramientas:eb_sinc_art_volumen_list')
        
        archivo = request.FILES['archivo_excel']
        
        # Validar extensión
        if not archivo.name.endswith('.xlsx'):
            messages.error(request, 'El archivo debe tener extensión .xlsx')
            return redirect('herramientas:eb_sinc_art_volumen_list')
        
        try:
            errores, actualizaciones = procesar_archivo_excel(archivo)
            
            if errores:
                error_msg = f'Se procesaron {actualizaciones} registros correctamente. Errores encontrados:<br>'
                error_msg += '<br>'.join(errores[:10])  # Mostrar máximo 10 errores
                if len(errores) > 10:
                    error_msg += f'<br>... y {len(errores) - 10} errores más.'
                messages.warning(request, error_msg)
            else:
                messages.success(request, f'Carga masiva completada exitosamente. Se actualizaron {actualizaciones} artículos.')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
    
    return redirect('herramientas:eb_sinc_art_volumen_list')

@login_required(login_url="/login/")
def eb_sinc_art_volumen_carga_masiva_form(request):
    """Muestra el formulario para carga masiva"""
    return render(request, 'herramientas/eb_sinc_art_volumen/carga_masiva.html')

def test_excel_download(request):
    """Vista de prueba simple para descargar Excel"""
    try:
        print("[TEST] Creando archivo Excel simple...")
        
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test"
        
        ws['A1'] = "Prueba"
        ws['B1'] = "Excel"
        ws['A2'] = "Funciona"
        ws['B2'] = "OK"
        
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="test.xlsx"'
        
        print("[TEST] Archivo Excel de prueba creado correctamente")
        return response
        
    except Exception as e:
        print(f"[TEST ERROR] {str(e)}")
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")

def test_plantilla_step_by_step(request):
    """Prueba la generación de plantilla paso a paso"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    try:
        print("[STEP 1] Configurando base de datos...")
        
        print("[STEP 2] Importando funciones...")
        from .sql_volumen import obtener_articulos_volumen
        
        print("[STEP 3] Obteniendo artículos...")
        articulos = obtener_articulos_volumen()
        print(f"[STEP 3] Se obtuvieron {len(articulos)} artículos")
        
        print("[STEP 4] Creando Excel básico con datos...")
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Volumenes"
        
        # Encabezados básicos
        ws['A1'] = "COD_ARTICULO"
        ws['B1'] = "DESCRIPCION"
        ws['C1'] = "RUBRO"
        
        # Agregar algunos datos (máximo 10 para prueba)
        for i, articulo in enumerate(articulos[:10], 2):
            ws[f'A{i}'] = articulo.get('COD_ARTICULO', '')
            ws[f'B{i}'] = articulo.get('DESCRIPCION', '')
            ws[f'C{i}'] = articulo.get('Rubro', '')
        
        print("[STEP 5] Generando respuesta...")
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="test_plantilla_simple.xlsx"'
        
        print("[STEP 5] ¡Éxito! Plantilla básica generada")
        return response
        
    except Exception as e:
        print(f"[STEP ERROR] Error en paso: {str(e)}")
        import traceback
        traceback.print_exc()
        return HttpResponse(f"Error en generación paso a paso: {str(e)}", content_type="text/plain")

def test_plantilla_simplificada(request):
    """Prueba con plantilla Excel simplificada"""
    # Configurar la base de datos
    nombre_db = 'LAKER_SA'
    settings.DATABASES['mi_db_2']['NAME'] = nombre_db
    
    try:
        print("[SIMPLE] Importando función simplificada...")
        from .excel_utils_simple import generar_plantilla_excel_simple
        
        print("[SIMPLE] Generando plantilla...")
        wb = generar_plantilla_excel_simple()
        
        print("[SIMPLE] Creando respuesta...")
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="Plantilla_Simplificada.xlsx"'
        
        print("[SIMPLE] ¡Éxito! Plantilla simplificada generada")
        return response
        
    except Exception as e:
        print(f"[SIMPLE ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return HttpResponse(f"Error en plantilla simplificada: {str(e)}", content_type="text/plain")

@login_required(login_url="/login/")
def gestion_sucursales_ecommerce(request):
    """Vista para gestionar las sucursales de ecommerce"""
    try:
        if request.method == 'POST':
            nro_sucursal = request.POST.get('nro_sucursal')
            if nro_sucursal:
                # Activar la sucursal seleccionada
                activar_sucursal_ecommerce(nro_sucursal)
                messages.success(request, f'Sucursal {nro_sucursal} activada exitosamente')
                return redirect('herramientas:gestion_sucursales_ecommerce')
        
        # Obtener todas las sucursales
        sucursales = obtener_sucursales_ecommerce()
        sucursal_activa = obtener_sucursal_activa()
        
        context = {
            'sucursales': sucursales,
            'sucursal_activa': sucursal_activa,
            'titulo': 'Gestión de Sucursales E-commerce'
        }
        
        return render(request, 'herramientas/gestion_sucursales_ecommerce.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar las sucursales: {str(e)}')
        return render(request, 'herramientas/gestion_sucursales_ecommerce.html', {
            'sucursales': [],
            'sucursal_activa': None,
            'titulo': 'Gestión de Sucursales E-commerce'
        })
