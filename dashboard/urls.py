# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    # Logistica
    path('Kpis_Logistica', views.Kpis_Logistica, name='dashboard_kpis_logistica'),
    # Abastecimiento - No URLs currently
    # Comercial
    path('Promociones', views.Promociones, name='dashboard_promociones'),
    path('Inventarios_Sucursales', views.Inventarios_Sucursales, name='dashboard_inventarios_sucursales'),
    path('Conteos', views.Conteos, name='dashboard_conteos'),
    path('Geodatos', views.Geodatos, name='dashboard_geodatos'),
    path('Notas_de_credito', views.Notas_de_credito, name='dashboard_notas_de_credito'),
    path('Ventas_Franquicias', views.Ventas_Franquicias, name='dashboard_ventas_franquicias'),
    path('Ventas_Sucursales', views.Ventas_Sucursales, name='dashboard_ventas_sucursales'),
    path('Ventas_SucursalesUY', views.Ventas_SucursalesUY, name='dashboard_ventas_sucursales_uy'),
    path('Velocidad_de_Ventas', views.Velocidad_de_Ventas, name='dashboard_velocidad_de_ventas'),
    # Mayoristas
    path('Ventas_Mayoristas', views.Ventas_Mayoristas, name='dashboard_ventas_mayoristas'),
    # Ecommerce
    path('Ventas_Ecommerce', views.Ventas_Ecommerce, name='dashboard_ventas_ecommerce'),
    path('Kpis_Ecommerce', views.Kpis_Ecommerce, name='dashboard_kpis_ecommerce'),
    path('PromocionesEcommerce', views.PromocionesEcommerce, name='dashboard_promociones_ecommerce'),
    # Gerencia
    path('PremiosComercial', views.PremiosComercial, name='dashboard_premios_comercial'),
]
