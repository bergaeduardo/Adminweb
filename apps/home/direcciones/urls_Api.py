# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from apps.home import views
from apps.authentication import api_views as auth_api_views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'uploadFacturasSuc', views.uploadFactura, basename='uploadFacturasSuc')

urlpatterns = [
    # Locales
        path('', include(router.urls)),
        path('altaFactura/<int:IdSuc>', views.altaFactura, name='uploadFacturasSuc'),
        path('gettoken', views.login, name='gettoken'),
        path('getFacturas/<int:numSuc>', views.getFacturas, name='getFacturas'),
        path('postFactura', views.postFactura, name='postFactura'),
        path('listarFacturasManuales', views.facturas_por_fecha, name='postFactura'),
        # SSO con el proyecto PHP (app.xl.com.ar)
        path('auth/validar-credenciales/', auth_api_views.validar_credenciales, name='validar_credenciales'),
        path('auth/validar-sso/', auth_api_views.validar_sso, name='validar_sso'),
]