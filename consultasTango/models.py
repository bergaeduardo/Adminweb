# -*- encoding:utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.core.validators import RegexValidator


class StockCentral(models.Model):
    articulo = models.CharField(db_column='COD_ARTICU', max_length=15,primary_key=True,unique=False)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=30, blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(db_column='COD_DEPOSI', max_length=2)  # Field name made lowercase.
    total = models.FloatField(db_column='STOCK_TOTAL', blank=True, null=True)  # Field name made lowercase.
    comp = models.FloatField(db_column='CANT_COMP', blank=True, null=True)  # Field name made lowercase.
    reserva = models.IntegerField(db_column='CANT_RESERVA')  # Field name made lowercase.
    excluido = models.IntegerField(db_column='STOCK_EXCLUIDO')  # Field name made lowercase.
    disponible = models.FloatField(db_column='STOCK_DISPONIBLE')  # Field name made lowercase.
    destino = models.CharField(db_column='DESTINO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rubro = models.CharField(db_column='RUBRO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    categoria = models.CharField(db_column='CATEGORIA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    temporada = models.CharField(db_column='TEMPORADA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='COLOR', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'STOCK_CENTRAL'


    def __str__(self):
        return self.articulo

class SjStockDisponibleEcommerce(models.Model):
    articulo = models.CharField(db_column='COD_ARTICU', max_length=15,primary_key=True,unique=False)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=30, blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(db_column='COD_DEPOSI', max_length=2)  # Field name made lowercase.
    total = models.FloatField(db_column='STOCK', blank=True, null=True)  # Field name made lowercase.
    stock_seguridad = models.FloatField(db_column='STOCK_SEGURIDAD', blank=True, null=True)  # Field name made lowercase.
    cant_comp = models.FloatField(db_column='CANT_COMP', blank=True, null=True)  # Field name made lowercase.
    reserva_ecommerce = models.FloatField(db_column='RESERVA_ECOMMERCE', blank=True, null=True)  # Field name made lowercase.
    stock_reserva_vtex = models.FloatField(db_column='STOCK_RESERVA_VTEX', blank=True, null=True)  # Field name made lowercase.
    stock_excluido = models.FloatField(db_column='STOCK_EXCLUIDO', blank=True, null=True)  # Field name made lowercase.
    stock_disponible = models.FloatField(db_column='STOCK_DISPONIBLE', blank=True, null=True)  # Field name made lowercase.
    rubro = models.CharField(db_column='RUBRO', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'SJ_STOCK_DISPONIBLE_ECOMMERCE'

class Turno(models.Model):
    IdTurno = models.AutoField(primary_key=True)
    CodigoProveedor = models.CharField(max_length=6,null=False, blank=False)
    FechaAsignacion = models.DateTimeField()
    OrdenCompra = models.CharField(max_length=14,null=False, blank=False)
    Remitos = models.CharField(max_length=100,null=False, blank=False)
    CantidadUnidades = models.IntegerField(null=False, blank=False)
    CantidadBultos = models.IntegerField(null=True, blank=True)
    Recepcionado = models.BooleanField(default=False)
    Auditado = models.BooleanField(default=False)
    Posicionado = models.BooleanField(default=False)
    Observaciones = models.CharField(max_length=300, null=True, blank=True)
    CodigoError = models.IntegerField(null=True, blank=True)
    RecepcionadoFechaHora = models.DateTimeField(null=True, blank=True)
    AuditadoFechaHora = models.DateTimeField(null=True, blank=True)
    PosicionadoFechaHora = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.IdTurno} - {self.OrdenCompra}'

class CodigosError(models.Model):
    CodigoError = models.IntegerField(primary_key=True)
    DescripcionError = models.CharField(max_length=100)

class EstadoTurno(models.Model):
    """
    Modelo para gestionar estados dinámicos de turnos
    Solo usuarios Admin y Logistica_Sup pueden gestionarlos
    """
    id_estado = models.AutoField(primary_key=True, db_column='id_estado')
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Estado")
    descripcion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción")
    orden_ejecucion = models.IntegerField(unique=True, verbose_name="Orden de Ejecución")
    es_requerido = models.BooleanField(default=True, verbose_name="¿Es Requerido?")
    permite_editar = models.BooleanField(default=True, verbose_name="¿Permite Editar Turno?")
    color = models.CharField(max_length=7, default='#17a2b8', verbose_name="Color (Hex)")
    activo = models.BooleanField(default=True, verbose_name="Estado Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Modificación")
    
    class Meta:
        db_table = 'EstadoTurno'
        ordering = ['orden_ejecucion']
        verbose_name = 'Estado de Turno'
        verbose_name_plural = 'Estados de Turnos'
    
    def __str__(self):
        return f'{self.orden_ejecucion}. {self.nombre}'

class TurnoReserva(models.Model):
    """
    Modelo para gestionar reservas de turnos para proveedores
    Usa bloques de 30 minutos y valida límites para usuarios no-admin
    """
    id_turno_reserva = models.AutoField(primary_key=True, db_column='id_turno_reserva')
    codigo_proveedor = models.CharField(max_length=6, null=False, blank=False, verbose_name="Código Proveedor")
    nombre_proveedor = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre Proveedor")
    fecha = models.DateField(verbose_name="Fecha del Turno")
    hora_inicio = models.TimeField(verbose_name="Hora Inicio")
    hora_fin = models.TimeField(verbose_name="Hora Fin")
    orden_compra = models.CharField(max_length=14, null=False, blank=False, verbose_name="Orden de Compra")
    remitos = models.CharField(max_length=100, null=False, blank=False, verbose_name="Remitos")
    cantidad_unidades = models.IntegerField(null=False, blank=False, verbose_name="Cantidad de Unidades")
    cantidad_bultos = models.IntegerField(null=True, blank=True, verbose_name="Cantidad de Bultos")
    observaciones = models.TextField(max_length=300, null=True, blank=True, verbose_name="Observaciones")
    usuario_creador = models.CharField(max_length=150, verbose_name="Usuario que Creó el Turno")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Modificación")
    estado = models.ForeignKey(
        EstadoTurno,
        on_delete=models.PROTECT,
        related_name='turnos',
        db_column='id_estado',
        verbose_name="Estado del Turno"
    )
    usuario_ultima_modificacion_estado = models.CharField(
        max_length=150, 
        null=True, 
        blank=True, 
        verbose_name="Usuario Última Modificación Estado"
    )
    estado_actual_desde = models.DateTimeField(null=True, blank=True, verbose_name="Estado Actual Desde")

    class Meta:
        db_table = 'TurnoReserva'
        ordering = ['fecha', 'hora_inicio']
        verbose_name = 'Turno Reserva'
        verbose_name_plural = 'Turnos Reservas'
        # Evitar superposición de turnos
        unique_together = [['fecha', 'hora_inicio']]

    def __str__(self):
        return f'{self.codigo_proveedor} - {self.fecha} {self.hora_inicio}-{self.hora_fin}'

    def get_duracion_minutos(self):
        """Calcula la duración del turno en minutos"""
        from datetime import datetime, timedelta
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        return int((fin - inicio).total_seconds() / 60)

class HistorialEstadoTurno(models.Model):
    """
    Modelo para registrar historial de cambios de estado de turnos
    Auditoría completa de quién y cuándo cambió cada estado
    """
    id_historial = models.AutoField(primary_key=True, db_column='id_historial')
    turno = models.ForeignKey(
        TurnoReserva,
        on_delete=models.CASCADE,
        related_name='historial_estados',
        db_column='id_turno_reserva',
        verbose_name="Turno Reserva"
    )
    estado_anterior = models.ForeignKey(
        EstadoTurno,
        on_delete=models.PROTECT,
        related_name='historiales_como_anterior',
        db_column='id_estado_anterior',
        null=True,
        blank=True,
        verbose_name="Estado Anterior"
    )
    estado_nuevo = models.ForeignKey(
        EstadoTurno,
        on_delete=models.PROTECT,
        related_name='historiales_como_nuevo',
        db_column='id_estado_nuevo',
        verbose_name="Estado Nuevo"
    )
    usuario = models.CharField(max_length=150, verbose_name="Usuario que Realizó el Cambio")
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora del Cambio")
    observaciones = models.TextField(max_length=500, null=True, blank=True, verbose_name="Observaciones")
    
    class Meta:
        db_table = 'HistorialEstadoTurno'
        ordering = ['-fecha_cambio']
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historiales de Estados'
    
    def __str__(self):
        anterior = self.estado_anterior.nombre if self.estado_anterior else "Inicial"
        return f'{self.turno} - {anterior} → {self.estado_nuevo.nombre}'

class EB_facturaManual(models.Model):
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    numeroSucursal = models.IntegerField()
    tipoFactura = models.IntegerField(choices=[(0, 'Factura-A'), (1, 'Factura-B')])
    numeroFactura = models.CharField(max_length=14, validators=[RegexValidator(regex='^\d{5}-\d{8}$', message='El formato debe ser XXXXX-XXXXXXX')])
    imgFactura = models.ImageField(upload_to='images/', blank=True, null=True)
    fechaVencimiento = models.DateField(blank=True, null=True)