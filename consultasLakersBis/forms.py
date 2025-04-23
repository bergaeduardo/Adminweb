from dataclasses import field
from django import forms
from .models import SucursalesLakers

class sucursalesform(forms.ModelForm):
    mail = forms.EmailField(required=False)
    
    class Meta:

        model = SucursalesLakers
        fields = ['id','nro_sucursal','cod_client','desc_sucursal','direccion','telefono','mail','localidad','provincia','canal',
        'habilitado','dashboard_bi','tango','nro_suc_madre','tipo_local','empresa_ferreteria','horario','integra_vtex','cod_deposi','retiro_expres']