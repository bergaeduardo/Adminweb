from django.conf import settings
from django.db import models

# Create your models here.


class RegistroAltaMuestraArticulo(models.Model):
    ACCION_IMPORTAR = 'importar'
    ACCION_EJECUTAR = 'ejecutar'
    ACCION_CHOICES = [
        (ACCION_IMPORTAR, 'Importar datos'),
        (ACCION_EJECUTAR, 'Ejecutar recodificación'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    fecha = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    filas = models.JSONField()
    numero_tarea = models.CharField(max_length=100, blank=True, null=True)
    filas_con_error = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Registro de alta de muestra de artículo'
        verbose_name_plural = 'Registros de altas de muestras de artículos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario} - {self.get_accion_display()} - {self.fecha:%Y-%m-%d %H:%M}'

class EBSincArtVolumen:
    """
    Modelo para representar la tabla EB_sincArt_volumen de la base de datos LAKER_SA.
    No heredo de models.Model ya que usaremos SQL directo para CRUD.
    """
    def __init__(self, cod_articulo=None, descripcion=None, rubro=None, fecha_alta=None, 
                 estado=None, fecha_sinc=None, alto_embalaje=None, 
                 ancho_embalaje=None, largo_embalaje=None, alto_real=None, 
                 ancho_real=None, largo_real=None, peso_embalaje=None, peso_real=None):
        self.cod_articulo = cod_articulo
        self.descripcion = descripcion
        self.rubro = rubro
        self.fecha_alta = fecha_alta
        self.estado = estado
        self.fecha_sinc = fecha_sinc
        self.alto_embalaje = alto_embalaje
        self.ancho_embalaje = ancho_embalaje
        self.largo_embalaje = largo_embalaje
        self.alto_real = alto_real
        self.ancho_real = ancho_real
        self.largo_real = largo_real
        self.peso_embalaje = peso_embalaje
        self.peso_real = peso_real
