from django.contrib import admin

from .models import RegistroTransferenciaDeposito


@admin.register(RegistroTransferenciaDeposito)
class RegistroTransferenciaDepositoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'numero_tarea', 'nro_comprobante')
    list_filter = ('accion', 'usuario')
    ordering = ('-fecha',)
    readonly_fields = (
        'usuario', 'fecha', 'accion', 'lote_id', 'filas',
        'filas_con_error', 'numero_tarea', 'nro_comprobante',
    )
