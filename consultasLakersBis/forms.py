from dataclasses import field
from django import forms
from .models import SucursalesLakers

class sucursalesform(forms.ModelForm):
    mail = forms.EmailField(required=False)
    
    class Meta:

        model = SucursalesLakers
        fields = ['id','nro_sucursal','cod_client','desc_sucursal','direccion','telefono','mail','localidad','provincia','canal',
        'habilitado','dashboard_bi','tango','nro_suc_madre','tipo_local','empresa_ferreteria','horario','integra_vtex','cod_deposi','retiro_expres','mail_grupo_emp']


class SucursalesLakersCompletaForm(forms.ModelForm):
    """Formulario completo para edición de todos los campos de SucursalesLakers"""
    
    PROVINCIAS_CHOICES = [
        ('', '- - -'),
        ('BUENOS AIRES', 'BUENOS AIRES'),
        ('CAPITAL FEDERAL', 'CAPITAL FEDERAL'),
        ('CATAMARCA', 'CATAMARCA'),
        ('CHACO', 'CHACO'),
        ('CHUBUT', 'CHUBUT'),
        ('CORDOBA', 'CORDOBA'),
        ('CORRIENTES', 'CORRIENTES'),
        ('ENTRE RIOS', 'ENTRE RIOS'),
        ('FORMOSA', 'FORMOSA'),
        ('JUJUY', 'JUJUY'),
        ('LA PAMPA', 'LA PAMPA'),
        ('LA RIOJA', 'LA RIOJA'),
        ('MENDOZA', 'MENDOZA'),
        ('MISIONES', 'MISIONES'),
        ('NEUQUEN', 'NEUQUEN'),
        ('RIO NEGRO', 'RIO NEGRO'),
        ('SALTA', 'SALTA'),
        ('SAN JUAN', 'SAN JUAN'),
        ('SAN LUIS', 'SAN LUIS'),
        ('SANTA CRUZ', 'SANTA CRUZ'),
        ('SANTA FE', 'SANTA FE'),
        ('SANTIAGO DEL ESTERO', 'SANTIAGO DEL ESTERO'),
        ('TIERRA DEL FUEGO', 'TIERRA DEL FUEGO'),
        ('TUCUMAN', 'TUCUMAN'),
        ('URUGUAY', 'URUGUAY'),
    ]
    
    mail = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mail_grupo_emp = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    fecha_cierre = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    provincia = forms.ChoiceField(
        choices=PROVINCIAS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = SucursalesLakers
        fields = '__all__'  # Incluye TODOS los campos del modelo
        widgets = {
            'nro_sucursal': forms.NumberInput(attrs={'class': 'form-control'}),
            'cod_client': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'desc_sucursal': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase'}),
            'canal': forms.TextInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dashboard_bi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tango': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'suc_madre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nro_suc_madre': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_local': forms.TextInput(attrs={'class': 'form-control'}),
            'integracion_mercadopago_madre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'integracion_mercadopago_hija': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empresa_ferreteria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'conexion_dns': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_dns': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_dns': forms.TextInput(attrs={'class': 'form-control'}),
            'conexion_teamviewer_madre': forms.TextInput(attrs={'class': 'form-control'}),
            'clave_teamviewer': forms.TextInput(attrs={'class': 'form-control'}),
            'factura_elect': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lapos_integrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'link_pedido': forms.TextInput(attrs={'class': 'form-control'}),
            'link_sales': forms.TextInput(attrs={'class': 'form-control'}),
            'lapos_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'version_soft_lapos': forms.TextInput(attrs={'class': 'form-control'}),
            'cable_lapos_integrado': forms.TextInput(attrs={'class': 'form-control'}),
            'n_llave_tango': forms.TextInput(attrs={'class': 'form-control'}),
            'base_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'conexion_teamviewer_hija': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_pc_madre': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_deposi': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'integra_vtex': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retiro_expres': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }