import django_filters
from consultasLakersBis.models import SofStockLakers,Direccionario
from django.db import connections

# Consultas sql para traer los items de los filtros 
def filtroCanal():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select CANAL from DIRECCIONARIO
                        group by CANAL
                        ''')
        consulta = cursor.fetchall()
        
        lista=[]
        for c in consulta:
            lista.append(c[0])
    return lista

def filtroCanal_2():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select CANAL from DIRECCIONARIO
                        group by CANAL
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroTipoLocal():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select TIPO_LOCAL from DIRECCIONARIO
                        group by TIPO_LOCAL
                        ''')
        consulta = cursor.fetchall()

        lista=[]
        for c in consulta:
            lista.append(c[0])
    return lista

def filtroTipoLocal_2():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select TIPO_LOCAL from DIRECCIONARIO
                        group by TIPO_LOCAL
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroGrupoEmpresario():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select GRUPO_EMPRESARIO from DIRECCIONARIO
                        where GRUPO_EMPRESARIO != ''
                        group by GRUPO_EMPRESARIO
                        order by GRUPO_EMPRESARIO
                        ''')
        consulta = cursor.fetchall()

        lista=[]
        for c in consulta:
            lista.append(c[0])
    return lista

def filtroProvincias():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
            SELECT PROVINCIA FROM DIRECCIONARIO
            WHERE NRO_SUC_MADRE IS NULL
            AND PROVINCIA IS NOT NULL AND PROVINCIA != ''
            GROUP BY PROVINCIA
            ORDER BY PROVINCIA
        ''')
        consulta = cursor.fetchall()
        lista = []
        for c in consulta:
            lista.append(c[0])
    return lista

def filtroRubro():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                            SELECT RUBRO FROM SOF_RUBROS_TANGO
                            where RUBRO != '_KITS'
                            GROUP BY RUBRO
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroTemporada():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select  ISNULL(TEMPORADA,'SIN TEMPORADA')TEMPORADA from SOF_STOCK_LAKERS
                        group by TEMPORADA
                        order by TEMPORADA
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroDescSuc():
    with connections['mi_db_4'].cursor() as cursor:
        cursor.execute('''
                        select  ISNULL(DESC_SUCURSAL,'SIN')DESC_SUCURSAL from SOF_STOCK_LAKERS
                        group by DESC_SUCURSAL
                        order by DESC_SUCURSAL
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

def itemsFiltros_upper(consulta):
    lista=[]
    for c in consulta:
        lista.append(tuple([c[0],c[0]]))
        opciones=tuple(lista)   
    return opciones

class UtilidadesTasky:
    @staticmethod
    def filtroDescSuc(parametro):
        with connections[parametro].cursor() as cursor:
            cursor.execute('''
                        select  ISNULL(DESC_SUCURSAL,'SIN')DESC_SUCURSAL from SOF_STOCK_LAKERS
                        group by DESC_SUCURSAL
                        order by DESC_SUCURSAL
                        ''')
            row = list(cursor.fetchall())
        return row
    
    @staticmethod
    def filtroTemp(parametro):
        with connections[parametro].cursor() as cursor:
            cursor.execute('''
                            select  ISNULL(TEMPORADA,'SIN')TEMPORADA from SOF_MAESTRO_ARTICULOS_RUBRO_CATEGORIA
                            group by TEMPORADA
                            order by TEMPORADA desc
                            ''')
            row = list(cursor.fetchall())
        return row
    
    @staticmethod
    def filtroRub(parametro):
        with connections[parametro].cursor() as cursor:
            cursor.execute('''
                            SELECT RUBRO FROM SOF_RUBROS_TANGO
                            where RUBRO != '_KITS'
                            GROUP BY RUBRO
                            ''')
            row = list(cursor.fetchall())
        return row
    
    @staticmethod
    def itemsFil(consulta):
        lista=[]
        for c in consulta:
            lista.append(tuple([c[0],c[0].lower()]))
            opciones=tuple(lista)   
        return opciones

    
# Clase para aplicar filtros a la consulta de stock central
class OrderFilterTasky(django_filters.FilterSet):
    desc_sucursal = django_filters.ChoiceFilter()
    temporada = django_filters.ChoiceFilter()
    rubro = django_filters.MultipleChoiceFilter()
    def __init__(self, DESC_SUCURSAL, TEMPORADA, RUBRO, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['desc_sucursal'].extra.update(choices=DESC_SUCURSAL)
        self.filters['temporada'].extra.update(choices=TEMPORADA)
        self.filters['rubro'].extra.update(choices=RUBRO)

    class Meta:
        model = SofStockLakers
        fields = ['desc_sucursal','temporada','rubro']


class DireccionarioFilter(django_filters.FilterSet):
    consulta = filtroCanal_2()
    CANAL = itemsFiltros_upper(consulta)

    consulta = filtroTipoLocal_2()
    TIPO_LOCAL = itemsFiltros_upper(consulta)

    class Meta:
        model = Direccionario
        fields = ['canal']
        ordering = ('nro_sucursal',)
        
    canal = django_filters.ChoiceFilter(label='CANAL ', choices=CANAL)
    tipo_local = django_filters.ChoiceFilter(label='TIPO LOCAL ', choices=TIPO_LOCAL)