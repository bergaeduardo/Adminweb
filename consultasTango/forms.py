from django import forms
from .models import Turno, CodigosError, TurnoReserva, EstadoTurno
from django.db import connections
from datetime import datetime, timedelta, date

class ImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        label='Selecciona múltiples imágenes'
    )

class CodigoErrorForm(forms.ModelForm):
    class Meta:
        model = CodigosError
        fields = ['DescripcionError']
        widgets = {
            'DescripcionError': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
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


class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=255, required=False)
    codigo = forms.CharField(max_length=50, required=False)
    PalabrasClave = forms.CharField(max_length=255, required=False, widget=forms.Textarea)

class SubcategoriaForm(forms.Form):
    codigo = forms.CharField(max_length=50, required=False)
    nombre = forms.CharField(max_length=255, required=False)
    Keywords = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    id_categoria_VtxAr = forms.ChoiceField(required=False)
    id_categoria_Tango = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las categorías para las listas desplegables
        with connections['mi_db_2'].cursor() as cursor:
            cursor.execute("SELECT id_Categoria_VtxAr, nombre FROM EB_Categoria_VtxAr")
            categorias = cursor.fetchall()
            self.fields['id_categoria_VtxAr'].choices = [('', '---------')] + [(cat[0], cat[1]) for cat in categorias]
            cursor.execute("SELECT ID, DESC_CATEGORIA FROM SJ_CATEGORIAS")
            categorias_tango = cursor.fetchall()
            self.fields['id_categoria_Tango'].choices = [('', '---------')] + [(cat[0], cat[1]) for cat in categorias_tango]


class RelacionForm(forms.Form):
    id_categoria_Tango = forms.ChoiceField(required=False)
    id_subCat_VtxAr = forms.ChoiceField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las subcategorias para las listas desplegables
        with connections['mi_db_2'].cursor() as cursor:
            cursor.execute("SELECT ID, DESC_CATEGORIA FROM SJ_CATEGORIAS")
            categorias_tango = cursor.fetchall()
            self.fields['id_categoria_Tango'].choices = [('', '---------')] + [(cat[0], cat[1]) for cat in categorias_tango]
            cursor.execute("SELECT id_subCat_VtxAr, nombre FROM EB_subCat_VtxAr")
            subcategorias = cursor.fetchall()
            self.fields['id_subCat_VtxAr'].choices = [('', '---------')] + [(subcat[0], subcat[1]) for subcat in subcategorias]


class TurnoReservaForm(forms.ModelForm):
    """
    Formulario para crear/editar reservas de turnos con validaciones específicas:
    - Usuarios no Admin/Logística: máximo 2 turnos consecutivos
    - Bloques de 30 minutos
    - Validación de disponibilidad de horario
    """
    # Campo adicional para control de cambio de estado
    cambiar_estado = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = TurnoReserva
        fields = [
            'codigo_proveedor', 
            'nombre_proveedor',
            'fecha', 
            'hora_inicio', 
            'hora_fin', 
            'orden_compra', 
            'remitos', 
            'cantidad_unidades', 
            'cantidad_bultos',
            'observaciones',
            'estado'
        ]
        widgets = {
            'codigo_proveedor': forms.TextInput(attrs={'class': 'form-control', 'id': 'codigoProveedor'}),
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'nombreProveedor'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '1800'}),  # Pasos de 30 min
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '1800'}),
            'orden_compra': forms.TextInput(attrs={'class': 'form-control'}),
            'remitos': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_unidades': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_bultos': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Recibir el usuario actual
        super().__init__(*args, **kwargs)
        
        # Hacer nombre_proveedor no requerido (se llena automáticamente)
        self.fields['nombre_proveedor'].required = False
        
        # Configurar campo estado según permisos del usuario
        if self.user:
            user_groups = [g.name for g in self.user.groups.all()]
            puede_cambiar_estado = (
                self.user.is_superuser or 
                'Admin' in user_groups or 
                'Logistica_Sup' in user_groups or
                'Logistica' in user_groups
            )
            
            # Solo mostrar estados activos ordenados
            self.fields['estado'].queryset = EstadoTurno.objects.filter(activo=True).order_by('orden_ejecucion')
            
            # Si es un nuevo turno (no tiene pk), asignar estado inicial
            if not self.instance.pk:
                estado_inicial = EstadoTurno.objects.filter(activo=True).order_by('orden_ejecucion').first()
                if estado_inicial:
                    self.fields['estado'].initial = estado_inicial.id_estado
            
            if puede_cambiar_estado:
                # Usuarios autorizados pueden ver y cambiar el estado
                self.fields['estado'].widget.attrs.update({
                    'class': 'form-control estado-select-enabled'
                })
                self.fields['cambiar_estado'].initial = True
            else:
                # Otros usuarios ven el estado pero no pueden cambiarlo
                self.fields['estado'].widget.attrs.update({
                    'class': 'form-control',
                    'disabled': 'disabled'
                })
                self.fields['cambiar_estado'].initial = False
        else:
            # Sin usuario, deshabilitar campo estado
            self.fields['estado'].widget.attrs.update({
                'class': 'form-control',
                'disabled': 'disabled'
            })
        
        # Si estamos editando y la fecha ya pasó, hacer campos readonly
        if self.instance and self.instance.pk:
            hoy = date.today()
            if self.instance.fecha <= hoy:
                # Deshabilitar campos de fecha y hora
                self.fields['fecha'].widget.attrs['readonly'] = True
                self.fields['hora_inicio'].widget.attrs['readonly'] = True
                self.fields['hora_fin'].widget.attrs['readonly'] = True
                
                # Mostrar advertencia
                self.fields['fecha'].help_text = "No se pueden editar turnos del día actual o fechas pasadas"

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        nuevo_estado = cleaned_data.get('estado')
        
        # Validación de orden secuencial de estados (solo al editar)
        if self.instance and self.instance.pk and nuevo_estado:
            estado_actual = self.instance.estado
            
            # Solo validar si hay cambio de estado
            if estado_actual and nuevo_estado != estado_actual:
                orden_actual = estado_actual.orden_ejecucion
                orden_nuevo = nuevo_estado.orden_ejecucion
                
                # Si el nuevo estado tiene un orden mayor, verificar estados requeridos intermedios
                if orden_nuevo > orden_actual:
                    # Buscar estados requeridos que se estén saltando
                    estados_intermedios_requeridos = EstadoTurno.objects.filter(
                        orden_ejecucion__gt=orden_actual,
                        orden_ejecucion__lt=orden_nuevo,
                        es_requerido=True,
                        activo=True
                    ).order_by('orden_ejecucion')
                    
                    if estados_intermedios_requeridos.exists():
                        nombres_estados = ', '.join([e.nombre for e in estados_intermedios_requeridos])
                        raise forms.ValidationError(
                            f"No puede saltarse estados requeridos. Primero debe pasar por: {nombres_estados}"
                        )

        if not all([fecha, hora_inicio, hora_fin]):
            return cleaned_data

        # Validar que hora_fin sea posterior a hora_inicio
        if hora_fin <= hora_inicio:
            raise forms.ValidationError(
                f"La hora de fin ({hora_fin.strftime('%H:%M')}) debe ser posterior a la hora de inicio ({hora_inicio.strftime('%H:%M')}). "
                f"Por favor, ajuste los horarios para que la reserva tenga una duración válida."
            )

        # Validar bloques de 30 minutos
        inicio_dt = datetime.combine(fecha, hora_inicio)
        fin_dt = datetime.combine(fecha, hora_fin)
        duracion_minutos = (fin_dt - inicio_dt).total_seconds() / 60

        if duracion_minutos % 30 != 0:
            raise forms.ValidationError(
                f"La duración del turno ({int(duracion_minutos)} minutos) no es válida. "
                f"Los turnos deben ser en bloques de 30 minutos (30, 60, 90, 120 minutos, etc.). "
                f"Por favor, ajuste la hora de fin para que la duración sea un múltiplo de 30 minutos."
            )

        # Validar que hora_inicio y hora_fin estén en intervalos de 30 minutos
        if hora_inicio.minute not in [0, 30] or hora_fin.minute not in [0, 30]:
            errores = []
            if hora_inicio.minute not in [0, 30]:
                errores.append(f"Hora de inicio: {hora_inicio.strftime('%H:%M')} (debe terminar en :00 o :30)")
            if hora_fin.minute not in [0, 30]:
                errores.append(f"Hora de fin: {hora_fin.strftime('%H:%M')} (debe terminar en :00 o :30)")
            
            raise forms.ValidationError(
                f"Las horas deben estar en intervalos de 30 minutos. Problemas detectados: {', '.join(errores)}. "
                f"Ejemplos de horas válidas: 08:00, 08:30, 09:00, 09:30, etc."
            )

        # Validar disponibilidad del horario (no superponer con otros turnos)
        # Excluir turnos cancelados de la validación
        turnos_existentes = TurnoReserva.objects.filter(
            fecha=fecha
        ).exclude(pk=self.instance.pk if self.instance.pk else None)
        
        # Solo validar contra turnos con estados activos (no cancelados)
        turnos_activos = []
        for turno in turnos_existentes:
            if turno.estado and turno.estado.activo:
                turnos_activos.append(turno)

        for turno in turnos_activos:
            # Verificar superposición
            if not (hora_fin <= turno.hora_inicio or hora_inicio >= turno.hora_fin):
                raise forms.ValidationError(
                    f"El horario seleccionado ({hora_inicio.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}) "
                    f"se superpone con una reserva existente del proveedor {turno.codigo_proveedor} "
                    f"({turno.hora_inicio.strftime('%H:%M')} - {turno.hora_fin.strftime('%H:%M')}). "
                    f"Por favor, seleccione otro horario disponible."
                )

        # Validar límite de 2 turnos consecutivos para usuarios no Admin/Logística
        if self.user:
            user_groups = [g.name for g in self.user.groups.all()]
            is_admin_or_logistica = (
                self.user.is_superuser or 
                'Admin' in user_groups or 
                'Logistica' in user_groups or
                'Logística' in user_groups
            )

            if not is_admin_or_logistica:
                # Calcular cantidad de bloques de 30 minutos
                bloques_solicitados = int(duracion_minutos / 30)
                
                if bloques_solicitados > 2:
                    raise forms.ValidationError(
                        f"Ha solicitado {bloques_solicitados} bloques de 30 minutos ({int(duracion_minutos)} minutos en total). "
                        f"Los usuarios sin permisos de Admin o Logística solo pueden reservar hasta 2 bloques consecutivos (1 hora máximo). "
                        f"Por favor, reduzca la duración de su reserva o contacte al administrador para solicitar permisos especiales."
                    )

        return cleaned_data

    def clean_codigo_proveedor(self):
        codigo = self.cleaned_data.get('codigo_proveedor')
        if codigo:
            codigo = codigo.upper().strip()
        return codigo

    def clean_fecha(self):
        """Validar que no se puedan reservar turnos para hoy o fechas pasadas"""
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            hoy = date.today()
            if fecha < hoy:
                dias_diferencia = (hoy - fecha).days
                raise forms.ValidationError(
                    f"No se puede reservar para una fecha pasada. La fecha seleccionada ({fecha.strftime('%d/%m/%Y')}) "
                    f"fue hace {dias_diferencia} día{'s' if dias_diferencia > 1 else ''}. "
                    f"Por favor, seleccione una fecha a partir de mañana ({(hoy + timedelta(days=1)).strftime('%d/%m/%Y')})."
                )
            elif fecha == hoy:
                raise forms.ValidationError(
                    f"No se puede reservar para el día de hoy ({hoy.strftime('%d/%m/%Y')}). "
                    f"Las reservas deben realizarse con al menos un día de anticipación. "
                    f"La primera fecha disponible es mañana ({(hoy + timedelta(days=1)).strftime('%d/%m/%Y')})."
                )
        return fecha


class EstadoTurnoForm(forms.ModelForm):
    """
    Formulario para gestionar estados de turnos
    Solo accesible para usuarios Admin y Logistica_Sup
    """
    class Meta:
        model = EstadoTurno
        fields = ['nombre', 'descripcion', 'orden_ejecucion', 'es_requerido', 'permite_editar', 'color', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Recepcionado'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del estado'}),
            'orden_ejecucion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'es_requerido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_editar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'color': forms.TextInput(attrs={
                'class': 'form-control', 
                'type': 'color',
                'title': 'Seleccione un color para el estado'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del Estado',
            'descripcion': 'Descripción',
            'orden_ejecucion': 'Orden de Ejecución',
            'es_requerido': '¿Es un estado requerido?',
            'permite_editar': '¿Permite editar turno?',
            'color': 'Color del Estado',
            'activo': '¿Estado activo?'
        }

    def clean_orden_ejecucion(self):
        """Validar que el orden de ejecución no se duplique"""
        orden = self.cleaned_data.get('orden_ejecucion')
        
        # Verificar si ya existe otro estado con el mismo orden
        query = EstadoTurno.objects.filter(orden_ejecucion=orden)
        
        # Si estamos editando, excluir el registro actual
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise forms.ValidationError(
                f"Ya existe un estado con el orden de ejecución {orden}. "
                "Por favor, elija un orden diferente."
            )
        
        return orden

    def clean_nombre(self):
        """Validar que el nombre del estado sea único"""
        nombre = self.cleaned_data.get('nombre')
        
        if nombre:
            nombre = nombre.strip()
            
            # Verificar si ya existe otro estado con el mismo nombre
            query = EstadoTurno.objects.filter(nombre__iexact=nombre)
            
            # Si estamos editando, excluir el registro actual
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise forms.ValidationError(
                    f"Ya existe un estado con el nombre '{nombre}'. "
                    "Por favor, elija un nombre diferente."
                )
        
        return nombre

    def clean_color(self):
        """Validar formato hexadecimal del color"""
        color = self.cleaned_data.get('color')
        
        if color:
            # Asegurar que tenga el formato #RRGGBB
            if not color.startswith('#'):
                color = '#' + color
            
            # Validar longitud
            if len(color) != 7:
                raise forms.ValidationError("El color debe tener el formato #RRGGBB")
            
            # Validar caracteres hexadecimales
            try:
                int(color[1:], 16)
            except ValueError:
                raise forms.ValidationError("El color debe contener solo caracteres hexadecimales (0-9, A-F)")
        
        return color