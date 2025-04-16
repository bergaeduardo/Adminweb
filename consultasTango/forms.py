from django import forms
from .models import Turno, CodigosError

class ImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Selecciona múltiples imágenes'
    )

class CodigoErrorForm(forms.ModelForm):
    class Meta:
        model = CodigosError
        fields = ['CodigoError', 'DescripcionError']
        widgets = {
            'CodigoError': forms.NumberInput(attrs={'class': 'form-control'}),
            'DescripcionError': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_CodigoError(self):
        codigo = self.cleaned_data.get('CodigoError')
        if codigo < 1:
            raise forms.ValidationError("El código de error debe ser un número positivo.")
        return codigo
    
class TurnoEditForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['Recepcionado', 'Auditado', 'Posicionado', 'Observaciones', 'CodigoError']
        widgets = {
            'Observaciones': forms.Textarea(attrs={'rows': 3}),
            'Recepcionado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Auditado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Posicionado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_Recepcionado(self):
        recepcionado = self.cleaned_data.get('Recepcionado')
        # Verificar si el turno ya existe y si Recepcionado ya estaba marcado
        if self.instance and self.instance.pk and self.instance.Recepcionado:
            if not recepcionado:  # Si están intentando desmarcar Recepcionado
                raise forms.ValidationError("No se puede desmarcar 'Recepcionado' una vez activado.")
        return recepcionado


    def clean(self):
        cleaned_data = super().clean()
        recepcionado = cleaned_data.get('Recepcionado')
        auditado = cleaned_data.get('Auditado')
        posicionado = cleaned_data.get('Posicionado')

        if auditado and not recepcionado:
            raise forms.ValidationError("No se puede marcar como Auditado sin haber sido Recepcionado.")
        if posicionado and not (recepcionado and auditado):
            raise forms.ValidationError("No se puede marcar como Posicionado sin haber sido Recepcionado y Auditado.")

        return cleaned_data
    
class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['CodigoProveedor', 'FechaAsignacion', 'OrdenCompra', 'Remitos', 'CantidadUnidades', 'CantidadBultos']
        widgets = {
            'FechaAsignacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CodigoProveedor'].widget.attrs.update({'class': 'form-control', 'id': 'codigoProveedor'})
        self.fields['FechaAsignacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['OrdenCompra'].widget.attrs.update({'class': 'form-control'})
        self.fields['Remitos'].widget.attrs.update({'class': 'form-control'})
        self.fields['CantidadUnidades'].widget.attrs.update({'class': 'form-control'})
        self.fields['CantidadBultos'].widget.attrs.update({'class': 'form-control'})

    NombreProveedor = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%Y-%m-%d'])
