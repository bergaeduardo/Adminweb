from cProfile import label
from pyexpat import model
import django_filters

from consultasTango.models import *
from django.db import connections

# Consultas sql para traer los items de los filtros 
def filtroTemporada():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('''
                        select  ISNULL(TEMPORADA,'SIN')TEMPORADA from SOF_MAESTRO_ARTICULOS_RUBRO_CATEGORIA
                        group by TEMPORADA
                        order by TEMPORADA desc
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroDeposito():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('''
                        select  COD_SUCURS from STA22
						where INHABILITA = 0
						AND COD_SUCURS IN ('82','01','02','03','04','05','06','07','08','09','10','11','12','20')
                        group by COD_SUCURS
                        order by COD_SUCURS
                        ''')
        row = list(cursor.fetchall())
    return row

def filtroRubro():
    with connections['mi_db_2'].cursor() as cursor:
        cursor.execute('''
                        select  ISNULL(RUBRO,'SIN')RUBRO from SOF_MAESTRO_ARTICULOS_RUBRO_CATEGORIA
                        group by RUBRO
                        order by RUBRO desc
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

class Utilidades:

    @staticmethod
    def consultarStock_pivot(parametro):
        sql = '''
            EXEC EB_StockCentralPivot
        '''
        with connections[parametro].cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
        
        return results, columns

    @staticmethod
    def filtroDepo(parametro):
        with connections[parametro].cursor() as cursor:
            cursor.execute('''
                            select  COD_SUCURS from STA22
                            where INHABILITA = 0
                            AND COD_SUCURS IN ('83','82','01','02','03','04','05','06','07','08','09','10','11','12','20')
                            group by COD_SUCURS
                            order by COD_SUCURS
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
                            select  ISNULL(RUBRO,'SIN')RUBRO from STOCK_CENTRAL
                            group by RUBRO
                            order by RUBRO desc
                            ''')
            row = list(cursor.fetchall())
        return row
    
    @staticmethod
    def filtroCat(parametro):
        with connections[parametro].cursor() as cursor:
            cursor.execute('''
                            select  ISNULL(CATEGORIA,'SIN')CATEGORIA from SOF_MAESTRO_ARTICULOS_RUBRO_CATEGORIA
                            group by CATEGORIA
                            order by CATEGORIA desc
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
    
    @staticmethod
    def listdropdowns(consulta):
        lista=[]
        for c in consulta:
            lista.append(str(c[0]))  
        return lista
    

# Clase para aplicar filtros a la consulta de stock central
class OrderFilter(django_filters.FilterSet):
    deposito = django_filters.ChoiceFilter()
    temporada = django_filters.ChoiceFilter()
    rubro = django_filters.ChoiceFilter()
    def __init__(self, DEPOSITO, TEMPORADA, RUBRO, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['deposito'].extra.update(choices=DEPOSITO)
        self.filters['temporada'].extra.update(choices=TEMPORADA)
        self.filters['rubro'].extra.update(choices=RUBRO)

    class Meta:
        model = StockCentral
        fields = ['deposito','temporada','rubro']

# Clase para aplicar filtros a la consulta de stock central ecommerce
class filtro_stock_ecommerce(django_filters.FilterSet):
    rubro = django_filters.ChoiceFilter()
    def __init__(self,RUBRO, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['rubro'].extra.update(choices=RUBRO)
    
    class Meta:
        model = SjStockDisponibleEcommerce
        fields = ['rubro']


class FacturaManualFilter(django_filters.FilterSet):
    fechaRegistro = django_filters.DateFilter(field_name='fechaRegistro', lookup_expr='date')
    numeroSucursal = django_filters.NumberFilter(field_name='numeroSucursal')

    class Meta:
        model = EB_facturaManual
        fields = ['fechaRegistro', 'numeroSucursal']
