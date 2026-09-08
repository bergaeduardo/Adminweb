from django.conf import settings
from django.db import models


class RegistroTransferenciaDeposito(models.Model):
    """Auditoría de las transferencias masivas entre depósitos.

    Vive en la base `default` (Postgres); el movimiento de stock real ocurre en
    LAKER_SA y en el WMS. Se guarda el lote completo como JSON, igual que
    RegistroAltaMuestraArticulo, para poder reconstruir qué se pidió.
    """

    ACCION_VALIDAR = 'validar'
    ACCION_EJECUTAR = 'ejecutar'
    ACCION_CHOICES = [
        (ACCION_VALIDAR, 'Validar lote'),
        (ACCION_EJECUTAR, 'Ejecutar transferencia'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    fecha = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    lote_id = models.UUIDField(db_index=True)
    filas = models.JSONField()
    filas_con_error = models.JSONField(blank=True, null=True)
    numero_tarea = models.TextField(blank=True, null=True)
    nro_comprobante = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Registro de transferencia entre depósitos'
        verbose_name_plural = 'Registros de transferencias entre depósitos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario} - {self.get_accion_display()} - {self.fecha:%Y-%m-%d %H:%M}'
