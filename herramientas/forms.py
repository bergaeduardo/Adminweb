from django import forms

class EBSincArtVolumenForm(forms.Form):
    # Campos no editables (solo lectura)
    cod_articulo = forms.CharField(
        max_length=20, 
        label='Código Artículo',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    descripcion = forms.CharField(
        max_length=50, 
        label='Descripción',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    rubro = forms.CharField(
        max_length=50,
        required=False,
        label='Rubro',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    
    # Campos editables - Dimensiones de embalaje
    alto_embalaje = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Alto Embalaje (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    ancho_embalaje = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Ancho Embalaje (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    largo_embalaje = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Largo Embalaje (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    
    # Campos editables - Dimensiones reales
    alto_real = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Alto Real (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    ancho_real = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Ancho Real (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    largo_real = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2,
        label='Largo Real (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
    )
    
    # Campos editables - Peso
    peso_embalaje = forms.IntegerField(
        required=False,
        label='Peso Embalaje (gr)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    peso_real = forms.IntegerField(
        required=False,
        label='Peso Real (gr)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    
    def __init__(self, *args, **kwargs):
        # Extraer datos iniciales si se proporcionan
        initial_data = kwargs.pop('initial_data', None)
        super().__init__(*args, **kwargs)
        
        if initial_data:
            # Función para convertir mm a cm
            def mm_a_cm(valor_mm):
                if valor_mm is None or valor_mm == 0:
                    return None
                try:
                    return round(float(valor_mm) / 10, 2)
                except (ValueError, TypeError):
                    return None
            
            self.fields['cod_articulo'].initial = initial_data.get('COD_ARTICULO')
            self.fields['descripcion'].initial = initial_data.get('DESCRIPCION')
            self.fields['rubro'].initial = initial_data.get('Rubro')
            self.fields['alto_embalaje'].initial = mm_a_cm(initial_data.get('altoEmbalaje'))
            self.fields['ancho_embalaje'].initial = mm_a_cm(initial_data.get('anchoEmbalaje'))
            self.fields['largo_embalaje'].initial = mm_a_cm(initial_data.get('largoEmbalaje'))
            self.fields['alto_real'].initial = mm_a_cm(initial_data.get('altoReal'))
            self.fields['ancho_real'].initial = mm_a_cm(initial_data.get('anchoReal'))
            self.fields['largo_real'].initial = mm_a_cm(initial_data.get('largoReal'))
            self.fields['peso_embalaje'].initial = initial_data.get('pesoEmbalaje')
            self.fields['peso_real'].initial = initial_data.get('pesoReal')