from django.contrib import admin

from .models import RegistroAltaMuestraArticulo

# Register your models here.


@admin.register(RegistroAltaMuestraArticulo)
class RegistroAltaMuestraArticuloAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'numero_tarea')
    list_filter = ('accion', 'usuario')
    ordering = ('-fecha',)
    readonly_fields = ('usuario', 'fecha', 'accion', 'filas', 'numero_tarea', 'filas_con_error')
