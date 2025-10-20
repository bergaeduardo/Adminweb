# Lakers Lab Admin Web - Instrucciones para Agentes de IA

## Arquitectura del Sistema

Este es un sistema Django multi-base de datos que integra tres sistemas empresariales:
- **Tango (ERP)**: Base SQL Server para inventario, ventas y contabilidad (`mi_db_2`)
- **WMS (Warehouse)**: Sistema de ubicaciones y movimientos de stock (`mi_db_3`) 
- **Lakers Bis**: Sistema de locales y operaciones (`mi_db_4`)
- **PostgreSQL**: Base principal para autenticación y configuración (`default`)

### Estructura de Apps Críticas

```
core/                   # Configuración central
├── settings.py        # Config base (usa local.py o production.py)
├── local.py          # Configuración desarrollo con 4 bases de datos
├── production.py     # Configuración producción
└── urls.py           # Rutas principales

consultasTango/       # Modelos ERP (Tango) - Solo lectura
consultasWMS/         # Modelos WMS/Warehouse - Lectura/escritura
consultasLakersBis/   # Modelos locales Lakers - Solo lectura
apps/home/           # Core web y autenticación
```

## Patrones de Configuración Específicos

### Multi-Database Setup
- **Database Routers**: Cada app tiene su router específico (`MiApp2Router`, `MiApp3Router`, `MiApp4Router`)
- **Modelos**: Usan `managed = False` para vistas de solo lectura (Tango, Lakers Bis)
- **Nombres DB**: `mi_db_2` (Tango), `mi_db_3` (WMS), `mi_db_4` (Lakers Bis)

### Configuración de Entorno
```python
# Siempre usar decouple para configuración
from decouple import config
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')
```

### AdminLTE Integration
- Usa `adminlte3` y `adminlte3_theme` packages
- Templates en `apps/templates/`
- Static files en `apps/static/`
- Configuración específica de Argentina: `TIME_ZONE = 'America/Argentina/Buenos_Aires'`

## Flujos de Trabajo Críticos

### Desarrollo Local
```bash
# Activar entorno virtual
.\env\Scripts\activate
# Usar configuración local (4 bases de datos)
python manage.py runserver --settings=core.local
```

### Base de Datos
- **NO** ejecutar migraciones en apps con `managed = False`
- Solo migrar app `default` (PostgreSQL) y `consultasWMS`
- Usar `python manage.py migrate --database=mi_db_3` para WMS específicamente

### API y CORS
- REST Framework configurado con documentación en `/docs/`
- CORS habilitado para dominios específicos (`app.xl.com.ar`, localhost)
- Headers personalizados: `USERNAME`, `PASSWORD` para APIs externas

## Patrones de Código Específicos

### Modelos de Solo Lectura (Tango/Lakers Bis)
```python
class StockCentral(models.Model):
    articulo = models.CharField(db_column='COD_ARTICU', max_length=15, primary_key=True)
    # ... campos mapeados a columnas SQL Server
    
    class Meta:
        managed = False  # NUNCA cambiar esto
        db_table = 'STOCK_CENTRAL'
```

### Modelos Editables (WMS)
```python
class Ubicacion(models.Model):
    # ... campos normales de Django
    
    class Meta:
        managed = True  # Permite migraciones
        db_table = 'Ubicacion'
```

### Database Router Pattern
Cada app externa tiene su router que direcciona operaciones a la base correcta:
```python
def db_for_read(self, model, **hints):
    if model._meta.app_label == 'consultasTango':
        return 'mi_db_2'
    return None
```

## Integración con Sistemas Externos

### APIs Externas (carpeta ApiUY/)
- Scripts Python independientes para integración con sistemas Jauser, Taiga, XL
- Usar tokens de autenticación específicos para cada servicio
- Archivos de configuración separados por ambiente

### Sesiones y Autenticación
- Sesiones caducan al cerrar navegador: `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- Duración de sesión: 12 horas (`SESSION_COOKIE_AGE = 12 * 60 * 60`)
- Redirect después de login: `LOGIN_REDIRECT_URL = "home"`

## Interacción Directa con Bases de Datos

### Módulos SQL Personalizados (`apps/home/SQL/`)
Para operaciones complejas que requieren SQL nativo, usa los módulos especializados:

**`Sql_Tango.py`** - Funciones para base Tango (ERP):
```python
from apps.home.SQL.Sql_Tango import validar_factManualCargada, validar_articulo, cargar_articulo

# Validar factura manual en sucursal específica
resultado = validar_factManualCargada(sucursal='01', factura='B0001-00012345')

# Validar si artículo existe y obtener descripción
descripcion = validar_articulo('ART001234')

# Cargar nuevo artículo en tabla temporal
cargar_articulo('ART001234', 'Descripción del producto')
```

**`Sql_WMS.py`** - Funciones para base WMS (Warehouse):
```python
from apps.home.SQL.Sql_WMS import validar_ubicacion, actualizar_ubicacion

# Validar ubicación y obtener ID (retorna 0 si no existe)
id_ubicacion = validar_ubicacion('A01-02-03')

# Actualizar datos de ubicación
actualizar_ubicacion(
    Id_ubicacion='123',
    nombre_ubicacion='Pasillo A Nivel 2',
    tipo_ubicacion='PICKING',
    estado_u='ACT',
    rack=1, modulo=2, altura=3
)
```

### Patrón de Conexión Directa
**CRUCIAL**: Siempre usar `connections['nombre_db']` para SQL directo:
```python
from django.db import connections

# Para Tango (ERP)
with connections['mi_db_2'].cursor() as cursor:
    sql = "SELECT COUNT(*) FROM STA11 WHERE COD_ARTICU = %s"
    cursor.execute(sql, [codigo_articulo])
    resultado = cursor.fetchone()

# Para WMS 
with connections['mi_db_3'].cursor() as cursor:
    sql = "UPDATE Ubicacion SET Estado_U = %s WHERE id_Ubicacion = %s"
    cursor.execute(sql, ['ACT', ubicacion_id])

# Para Lakers Bis
with connections['mi_db_4'].cursor() as cursor:
    sql = "SELECT * FROM CTA02 WHERE NRO_SUCURS = %s"
    cursor.execute(sql, [sucursal])
```

### Directrices de Seguridad SQL
1. **Usar parámetros**: NUNCA concatenar strings directamente en SQL
2. **Transacciones**: Para operaciones críticas, usar transacciones explícitas
3. **Stored Procedures**: Preferir SP existentes (ej: `EXEC SP_EB_DescArt_VtxAr`)

## Comandos Específicos del Proyecto

```bash
# Desarrollo
python manage.py runserver --settings=core.local

# Producción 
python manage.py runserver --settings=core.production

# Migraciones solo para bases editables
python manage.py migrate                    # PostgreSQL default
python manage.py migrate --database=mi_db_3 # WMS únicamente
```

## Creación de Nuevas Páginas Web con CRUD

### Pasos para crear página CRUD en app "herramientas" (Ejemplo: tabla `EB_sincArt_volumen` en `mi_db_2`)

**1. Crear funciones SQL en `apps/home/SQL/Sql_Tango.py`:**
```python
def obtener_todos_sinc_art_volumen():
    with connections['mi_db_2'].cursor() as cursor:
        sql = "SELECT Id, Articulo, Volumen, FechaActualizacion FROM EB_sincArt_volumen ORDER BY FechaActualizacion DESC"
        cursor.execute(sql)
        return cursor.fetchall()

def crear_sinc_art_volumen(articulo, volumen):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "INSERT INTO EB_sincArt_volumen (Articulo, Volumen, FechaActualizacion) VALUES (%s, %s, GETDATE())"
        cursor.execute(sql, [articulo, volumen])

def actualizar_sinc_art_volumen(id_registro, articulo, volumen):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "UPDATE EB_sincArt_volumen SET Articulo = %s, Volumen = %s, FechaActualizacion = GETDATE() WHERE Id = %s"
        cursor.execute(sql, [articulo, volumen, id_registro])

def eliminar_sinc_art_volumen(id_registro):
    with connections['mi_db_2'].cursor() as cursor:
        sql = "DELETE FROM EB_sincArt_volumen WHERE Id = %s"
        cursor.execute(sql, [id_registro])
```

**2. Crear formulario en `herramientas/forms.py` (crear archivo si no existe):**
```python
from django import forms

class SincArtVolumenForm(forms.Form):
    articulo = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    volumen = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
```

**3. Crear vista en `herramientas/views.py`:**
```python
from apps.home.SQL.Sql_Tango import obtener_todos_sinc_art_volumen, crear_sinc_art_volumen
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SincArtVolumenForm

@login_required(login_url="/login/")
def sinc_art_volumen_list(request):
    registros = obtener_todos_sinc_art_volumen()
    form = SincArtVolumenForm()
    
    if request.method == 'POST':
        form = SincArtVolumenForm(request.POST)
        if form.is_valid():
            crear_sinc_art_volumen(
                form.cleaned_data['articulo'],
                form.cleaned_data['volumen']
            )
            messages.success(request, 'Registro creado exitosamente')
            return redirect('sinc_art_volumen_list')
    
    return render(request, 'herramientas/sinc_art_volumen.html', {
        'registros': registros,
        'form': form
    })
```

**4. Crear template en `herramientas/templates/herramientas/sinc_art_volumen.html`:**
```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %} Sincronización Artículo Volumen {% endblock %}

{% block content %}
<div class="content-wrapper">
    <div class="container-fluid">
        <h1>Gestión EB_sincArt_volumen</h1>
        
        <!-- Formulario de creación -->
        <form method="post" class="mb-4">
            {% csrf_token %}
            <div class="row">
                <div class="col-md-4">
                    {{ form.articulo.label_tag }}
                    {{ form.articulo }}
                </div>
                <div class="col-md-4">
                    {{ form.volumen.label_tag }}
                    {{ form.volumen }}
                </div>
                <div class="col-md-4 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Crear</button>
                </div>
            </div>
        </form>
        
        <!-- Tabla de registros -->
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Artículo</th>
                    <th>Volumen</th>
                    <th>Fecha Actualización</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for registro in registros %}
                <tr>
                    <td>{{ registro.0 }}</td>
                    <td>{{ registro.1 }}</td>
                    <td>{{ registro.2 }}</td>
                    <td>{{ registro.3 }}</td>
                    <td>
                        <a href="{% url 'sinc_art_volumen_edit' registro.0 %}" class="btn btn-sm btn-warning">Editar</a>
                        <a href="{% url 'sinc_art_volumen_delete' registro.0 %}" class="btn btn-sm btn-danger">Eliminar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

**5. Agregar URLs en `herramientas/urls.py` (ya existe):**
```python
from django.urls import path
from . import views

# Agregar a las URLs existentes
urlpatterns = [
    # ... URLs existentes ...
    path('sinc-art-volumen/', views.sinc_art_volumen_list, name='sinc_art_volumen_list'),
    path('sinc-art-volumen/edit/<int:id>/', views.sinc_art_volumen_edit, name='sinc_art_volumen_edit'),
    path('sinc-art-volumen/delete/<int:id>/', views.sinc_art_volumen_delete, name='sinc_art_volumen_delete'),
]
```

**6. Las URLs de herramientas ya están incluidas en `core/urls.py`:**
```python
path("Herramientas/", include("herramientas.urls")),
```

### Estructura de Archivos para Nuevas Funcionalidades en App "herramientas"
```
nueva_funcionalidad_herramientas/
├── apps/home/SQL/Sql_[Sistema].py        # Funciones SQL específicas
├── herramientas/forms.py                 # Formularios Django (crear si no existe)
├── herramientas/views.py                 # Lógica de vistas (modificar existente)
├── herramientas/urls.py                  # URLs (agregar a existentes)
└── herramientas/templates/herramientas/  # Templates AdminLTE
```

**Nota**: La app "herramientas" ya existe y tiene estructura establecida. Solo agregar nuevas funciones a archivos existentes.

## Archivos Clave para Entender el Sistema

- `core/local.py`: Configuración completa de 4 bases de datos
- `modeloTango.py`, `modeloWMS.py`: Modelos generados automáticamente
- `consultasTango/routers.py`: Lógica de enrutamiento de base de datos
- `requirements.txt`: Dependencias específicas (mssql, psycopg2, adminlte3)

**IMPORTANTE**: Este sistema maneja datos críticos de inventario y ventas. Siempre verificar el entorno de base de datos antes de realizar cambios que afecten stock o transacciones.