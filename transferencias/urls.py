# -*- encoding: utf-8 -*-

from django.urls import path

from . import views

app_name = "transferencias"

urlpatterns = [
    path('Depositos', views.transferencias_depositos,
         name='transferencias_depositos'),
    path('Depositos/subir-archivo', views.transferencias_depositos_subir_archivo,
         name='transferencias_depositos_subir_archivo'),
    path('Depositos/buscar-articulo', views.transferencias_depositos_buscar_articulo,
         name='transferencias_depositos_buscar_articulo'),
    path('Depositos/validar', views.transferencias_depositos_validar,
         name='transferencias_depositos_validar'),
    path('Depositos/ejecutar', views.transferencias_depositos_ejecutar,
         name='transferencias_depositos_ejecutar'),
    path('Depositos/historial', views.transferencias_depositos_historial,
         name='transferencias_depositos_historial'),
    path('Depositos/historial/exportar', views.transferencias_depositos_historial_exportar,
         name='transferencias_depositos_historial_exportar'),
]
