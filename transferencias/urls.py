# -*- encoding: utf-8 -*-

from django.urls import path

from . import views

app_name = "transferencias"

urlpatterns = [
    path('Depositos', views.transferencias_depositos,
         name='transferencias_depositos'),
    path('Depositos/subir-archivo', views.transferencias_depositos_subir_archivo,
         name='transferencias_depositos_subir_archivo'),
    path('Depositos/validar', views.transferencias_depositos_validar,
         name='transferencias_depositos_validar'),
    path('Depositos/ejecutar', views.transferencias_depositos_ejecutar,
         name='transferencias_depositos_ejecutar'),
]
