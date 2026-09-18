from cProfile import label
from pyexpat import model
import django_filters
from django_filters import DateFilter

from consultasWMS.models import *
from django.db import connections
from django.forms.widgets import DateInput, TextInput, Select

TEXT_ATTRS = {'class': 'form-control form-control-sm'}
SELECT_ATTRS = {'class': 'form-control form-control-sm custom-select custom-select-sm'}

# Consultas sql para traer los items de los filtros 
def filtroUsuario():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        SELECT [UserName]
                        FROM [UbicacionesStockMvc].[dbo].[AspNetUsers]
                        where [LockoutEnabled]!=1
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroDeposito():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('''
                        select  COD_SUCURS from STA22
                        where INHABILITA = 0
                        AND COD_SUCURS != 'FA'
                        and ABASTECE = 0
                        group by COD_SUCURS
                        order by COD_SUCURS
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroMovimientos():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        select TIPO_MOVIMIENTO from RO_MOVIMIENTOS_WMS
                        where TIPO_MOVIMIENTO != 'NULL'
                        GROUP BY TIPO_MOVIMIENTO
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroTipoUbicacionStock():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        select TIPO_UBICACION from RO_STOCK_WMS_DESTINO
                        where TIPO_UBICACION is not null
                        GROUP BY TIPO_UBICACION
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroDestinoStock():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        select DESTINO from RO_STOCK_WMS_DESTINO
                        where DESTINO is not null
                        GROUP BY DESTINO
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroRubroStock():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        select RUBRO from RO_STOCK_WMS_DESTINO
                        where RUBRO is not null
                        GROUP BY RUBRO
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroTemporadaStock():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        select TEMPORADA from RO_STOCK_WMS_DESTINO
                        where TEMPORADA is not null
                        GROUP BY TEMPORADA
                        ''')
        row = list(cursor.fetchall())
    return row

# Funcion que arma una tupla con los parametros de filtros
def itemsFiltros(consulta):
    lista=[]
    for c in consulta:
        lista.append(tuple([c[0],c[0].lower()]))
        opciones=tuple(lista)   
    return opciones


# Clase para aplicar filtros a la consulta de stock central
class OrderFilterWms(django_filters.FilterSet):
    # Cargar los items de los filtros en la variable Deposito
    consulta = filtroDeposito()
    DEPOSITO = itemsFiltros(consulta)
    # Cargar los items de los filtros en la variable Temporada
    consulta = filtroUsuario()
    USER = itemsFiltros(consulta)
    # Cargar los items de los filtros en la variable Rubro
    consulta = filtroMovimientos()
    MOVIMIENTOS = itemsFiltros(consulta)
    

    class Meta:
        model = RoMovimientosWms
        # fields = {
        #     'nro_tarea': ['icontains'],
        # }
        exclude = ['nro_tarea','nro_movim','fecha','hora','cod_articulo','descripcion','cantidad','tipo_movimiento','ubic_origen','depo_origen','ubic_destino','depo_destino','usuario']

    nro_tarea=django_filters.CharFilter(field_name='nro_tarea', label='TAREA N° ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    fecha_desde = DateFilter(field_name='fecha', lookup_expr='gte',label='DESDE ', widget=DateInput(attrs={**TEXT_ATTRS, 'type': 'date'}))
    fecha_hasta = DateFilter(field_name='fecha', lookup_expr='lte',label='HASTA ', widget=DateInput(attrs={**TEXT_ATTRS, 'type': 'date'}))
    usuario = django_filters.ChoiceFilter(label='USUARIO ', choices=USER, widget=Select(attrs=SELECT_ATTRS))
    depo_destino = django_filters.ChoiceFilter(label='DEPOSITO ', choices=DEPOSITO, widget=Select(attrs=SELECT_ATTRS))
    tipo_movimiento = django_filters.ChoiceFilter(label='TIPO DE MOVIMIENTO ', choices=MOVIMIENTOS, widget=Select(attrs=SELECT_ATTRS))
    cod_articulo = django_filters.CharFilter(field_name='cod_articulo', label='CODIGO DE ARTICULO ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))


# Clase para aplicar filtros a la consulta de stock WMS por destino/ubicacion
class OrderFilterStockWmsDestino(django_filters.FilterSet):
    consulta = filtroDeposito()
    DEPOSITO = itemsFiltros(consulta)
    consulta = filtroTipoUbicacionStock()
    TIPO_UBICACION = itemsFiltros(consulta)
    consulta = filtroDestinoStock()
    DESTINO = itemsFiltros(consulta)
    consulta = filtroRubroStock()
    RUBRO = itemsFiltros(consulta)
    consulta = filtroTemporadaStock()
    TEMPORADA = itemsFiltros(consulta)

    class Meta:
        model = RoStockWmsDestino
        exclude = ['deposito','ubicacion','cod_articulo','descripcion','stock_ubic','tipo_ubicacion','destino','rubro','temporada']

    deposito = django_filters.ChoiceFilter(label='DEPOSITO ', choices=DEPOSITO, widget=Select(attrs=SELECT_ATTRS))
    ubicacion = django_filters.CharFilter(field_name='ubicacion', label='UBICACION ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    cod_articulo = django_filters.CharFilter(field_name='cod_articulo', label='CODIGO DE ARTICULO ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    tipo_ubicacion = django_filters.ChoiceFilter(label='TIPO DE UBICACION ', choices=TIPO_UBICACION, widget=Select(attrs=SELECT_ATTRS))
    destino = django_filters.ChoiceFilter(label='DESTINO ', choices=DESTINO, widget=Select(attrs=SELECT_ATTRS))
    rubro = django_filters.ChoiceFilter(label='RUBRO ', choices=RUBRO, widget=Select(attrs=SELECT_ATTRS))
    temporada = django_filters.ChoiceFilter(label='TEMPORADA ', choices=TEMPORADA, widget=Select(attrs=SELECT_ATTRS))

# # Clase para aplicar filtros a la consulta de stock central ecommerce
# class filtro_stock_ecommerce(django_filters.FilterSet):
#     # Cargar los items de los filtros en la variable Deposito
#     consulta = filtroDeposito()
#     DEPOSITO = itemsFiltros(consulta)
#     # Cargar los items de los filtros en la variable Rubro
#     consulta = filtroRubro()
#     RUBRO = itemsFiltros(consulta)
    
#     class Meta:
#         model = RoMovimientosWms
#         # fields = [...]
#         exclude = ['articulo','descripcion','deposito','total','stock_seguridad','cant_comp','reserva_ecommerce','stock_reserva_vtex','stock_excluido','stock_disponible','rubro']

#     # deposito = django_filters.ChoiceFilter(label='DEPOSITO ', choices=DEPOSITO)
#     rubro = django_filters.ChoiceFilter(label='RUBRO ', choices=RUBRO)
