# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "extras"
urlpatterns = [
    path('runscript', views.runscript, name='extras_runscript'),
    path('runscriptResult', views.runscriptResult, name='extras_runscript_result'),
    path('editarSucursal/<int:id>', views.editarSucursal, name='extras_editar_sucursal'),
    path('registraSucursal', views.registraSucursal, name='extras_registrar_sucursal'),
    # Removed import file URLs as they were moved to 'herramientas'
    # path('import_file_etiquetas', views.import_file_etiquetas, name='import_file_etiquetas'),
    # path('import_file_cierrePedidos', views.import_file_cierrePedidos, name='import_file_cierrePedidos'),
    # path('import_file_cierrePedidosUY', views.import_file_cierrePedidosUY, name='import_file_cierrePedidosUY'),
    # path('import_file_ubi', views.import_file_ubi, name='import_file_ubi'),
    path('direccionario', views.agenda, name='extras_direccionario'), # Corrected name
    path('direccionario/AltaSucursal', views.registraSucursal, name='altadireccionario'),
    path('direccionario/editarSucursal/<int:id>', views.editarSucursal, name='editarSucursal'),
    # path('agenda', views.agenda, name='extras_agenda'), # Corrected name
    path('direccionarioTabla', views.DireccionarioTabla, name='extras_direccionario_tabla'), # Corrected name
    path('reporTrello', views.reporTrello, name='extras_reporte_trello'), # Corrected name
    path('internos', views.internos, name='extras_internos'), # Corrected name
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
