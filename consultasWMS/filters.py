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

# Funcion que arma una tupla con los parametros de filtros
def itemsFiltros(consulta):
    lista=[]
    for c in consulta:
        lista.append(tuple([c[0],c[0].lower()]))
        opciones=tuple(lista)
    return opciones


# Los combos de los filtros de WMS salen de vistas SQL pesadas (hasta ~20s
# cada una). Antes se resolvian en el cuerpo de la clase, es decir al
# IMPORTAR el modulo: eso bloqueaba el arranque de CADA worker de Django
# (y por lo tanto todo el sitio, no solo estas dos pantallas) durante
# ~85s en total. Ahora se resuelven de forma perezosa (solo al renderizar
# el formulario) y se cachean, para no pegarle a SQL Server en cada visita.
from django.core.cache import cache

CACHE_TIMEOUT = 60 * 60  # 1 hora

def choices_cache(cache_key, query_func):
    def get_choices():
        choices = cache.get(cache_key)
        if choices is None:
            choices = itemsFiltros(query_func())
            cache.set(cache_key, choices, CACHE_TIMEOUT)
        return choices
    return get_choices


# tipo_ubicacion, destino, rubro y temporada salen las 4 de la misma vista
# pesada (RO_STOCK_WMS_DESTINO, ~20s por consulta). Antes eran 4 SELECT...
# GROUP BY separados; ahora se resuelven con un unico SELECT y se derivan
# los 4 combos en Python, para pagar el costo de la vista una sola vez.
STOCK_WMS_DESTINO_FILTRO_KEYS = (
    'wms_filtro_tipo_ubicacion_stock',
    'wms_filtro_destino_stock',
    'wms_filtro_rubro_stock',
    'wms_filtro_temporada_stock',
)

def _cargar_filtros_stock_wms_destino():
    with connections['mi_db_3'].cursor() as cursor:
        cursor.execute('''
                        SELECT DISTINCT TIPO_UBICACION, DESTINO, RUBRO, TEMPORADA
                        FROM RO_STOCK_WMS_DESTINO
                        ''')
        rows = cursor.fetchall()

    tipo_ubicacion, destino, rubro, temporada = set(), set(), set(), set()
    for t, d, r, tmp in rows:
        if t:
            tipo_ubicacion.add(t)
        if d:
            destino.add(d)
        if r:
            rubro.add(r)
        if tmp:
            temporada.add(tmp)

    resultado = dict(zip(STOCK_WMS_DESTINO_FILTRO_KEYS, [
        itemsFiltros([(v,) for v in sorted(tipo_ubicacion)]),
        itemsFiltros([(v,) for v in sorted(destino)]),
        itemsFiltros([(v,) for v in sorted(rubro)]),
        itemsFiltros([(v,) for v in sorted(temporada)]),
    ]))
    for key, value in resultado.items():
        cache.set(key, value, CACHE_TIMEOUT)
    return resultado


def choices_cache_stock_wms_destino(cache_key):
    def get_choices():
        choices = cache.get(cache_key)
        if choices is None:
            choices = _cargar_filtros_stock_wms_destino()[cache_key]
        return choices
    return get_choices


# Clase para aplicar filtros a la consulta de stock central
class OrderFilterWms(django_filters.FilterSet):

    class Meta:
        model = RoMovimientosWms
        # fields = {
        #     'nro_tarea': ['icontains'],
        # }
        exclude = ['nro_tarea','nro_movim','fecha','hora','cod_articulo','descripcion','cantidad','tipo_movimiento','ubic_origen','depo_origen','ubic_destino','depo_destino','usuario']

    nro_tarea=django_filters.CharFilter(field_name='nro_tarea', label='TAREA N° ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    fecha_desde = DateFilter(field_name='fecha', lookup_expr='gte',label='DESDE ', widget=DateInput(attrs={**TEXT_ATTRS, 'type': 'date'}))
    fecha_hasta = DateFilter(field_name='fecha', lookup_expr='lte',label='HASTA ', widget=DateInput(attrs={**TEXT_ATTRS, 'type': 'date'}))
    usuario = django_filters.ChoiceFilter(label='USUARIO ', choices=choices_cache('wms_filtro_usuario', filtroUsuario), widget=Select(attrs=SELECT_ATTRS))
    depo_destino = django_filters.ChoiceFilter(label='DEPOSITO ', choices=choices_cache('wms_filtro_deposito', filtroDeposito), widget=Select(attrs=SELECT_ATTRS))
    tipo_movimiento = django_filters.ChoiceFilter(label='TIPO DE MOVIMIENTO ', choices=choices_cache('wms_filtro_movimientos', filtroMovimientos), widget=Select(attrs=SELECT_ATTRS))
    cod_articulo = django_filters.CharFilter(field_name='cod_articulo', label='CODIGO DE ARTICULO ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))


# Clase para aplicar filtros a la consulta de stock WMS por destino/ubicacion
class OrderFilterStockWmsDestino(django_filters.FilterSet):

    class Meta:
        model = RoStockWmsDestino
        exclude = ['deposito','ubicacion','cod_articulo','descripcion','stock_ubic','tipo_ubicacion','destino','rubro','temporada']

    deposito = django_filters.ChoiceFilter(label='DEPOSITO ', choices=choices_cache('wms_filtro_deposito', filtroDeposito), widget=Select(attrs=SELECT_ATTRS))
    ubicacion = django_filters.CharFilter(field_name='ubicacion', label='UBICACION ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    cod_articulo = django_filters.CharFilter(field_name='cod_articulo', label='CODIGO DE ARTICULO ', lookup_expr='icontains', widget=TextInput(attrs=TEXT_ATTRS))
    tipo_ubicacion = django_filters.ChoiceFilter(label='TIPO DE UBICACION ', choices=choices_cache_stock_wms_destino('wms_filtro_tipo_ubicacion_stock'), widget=Select(attrs=SELECT_ATTRS))
    destino = django_filters.ChoiceFilter(label='DESTINO ', choices=choices_cache_stock_wms_destino('wms_filtro_destino_stock'), widget=Select(attrs=SELECT_ATTRS))
    rubro = django_filters.ChoiceFilter(label='RUBRO ', choices=choices_cache_stock_wms_destino('wms_filtro_rubro_stock'), widget=Select(attrs=SELECT_ATTRS))
    temporada = django_filters.ChoiceFilter(label='TEMPORADA ', choices=choices_cache_stock_wms_destino('wms_filtro_temporada_stock'), widget=Select(attrs=SELECT_ATTRS))

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
