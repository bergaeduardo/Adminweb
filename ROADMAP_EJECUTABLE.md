# 🚀 Roadmap Ejecutable - Modernización Adminweb
## Guía Paso a Paso para Agente de Codificación

**Versión**: 1.0  
**Fecha**: 28 de noviembre de 2025  
**Duración Total**: 35 semanas  
**Progreso**: 0% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜

---

## 📋 Índice Rápido
- [Fase 1: Fundamentos](#fase-1-fundamentos) (6 semanas)
- [Fase 2: Backend](#fase-2-backend) (8 semanas)
- [Fase 3: UI Tabler](#fase-3-ui-tabler) (12 semanas)
- [Fase 4: Performance](#fase-4-performance) (4 semanas)
- [Fase 5: Testing](#fase-5-testing) (5 semanas)

---

## FASE 1: Fundamentos
**Duración**: 6 semanas | **Progreso**: [ ] 0/18 tareas

### 1.1 Actualización Django Core ⏳
**Objetivo**: Django 3.2.6 → 5.1.3

#### Tareas
- [ ] **T1.1.1** Auditar `requirements.txt` - identificar incompatibilidades
  ```powershell
  # Revisar cada paquete manualmente
  pip list --outdated
  ```

- [ ] **T1.1.2** Actualizar `requirements.txt`
  ```python
  # Cambiar en requirements.txt:
  Django==5.1.3  # era 3.2.6
  mssql-django==1.5  # era 1.1.2
  djangorestframework==3.15.2  # era 3.15.1
  ```

- [ ] **T1.1.3** Crear entorno virtual limpio
  ```powershell
  deactivate
  Remove-Item -Recurse -Force .\env
  python -m venv env
  .\env\Scripts\activate
  pip install -r requirements.txt
  ```

- [ ] **T1.1.4** Actualizar `core/settings.py`
  ```python
  # Agregar al final de settings.py:
  DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
  ```

- [ ] **T1.1.5** Ejecutar migraciones
  ```powershell
  python manage.py migrate --database=default
  python manage.py migrate --database=mi_db_3
  ```

- [ ] **T1.1.6** Probar vistas críticas manualmente
  - Login/Logout
  - Dashboard
  - Stock Central
  - Ubicaciones WMS

**✅ DoD**: Django 5.1.3 corriendo sin errores, 4 BD conectadas

---

### 1.2 Build Frontend (Vite) ⏳
**Objetivo**: Configurar bundler moderno

#### Tareas
- [ ] **T1.2.1** Inicializar npm e instalar Vite
  ```powershell
  npm init -y
  npm install -D vite @vitejs/plugin-vue vite-plugin-static-copy
  npm install -D sass postcss autoprefixer cssnano
  ```

- [ ] **T1.2.2** Crear estructura de directorios
  ```powershell
  mkdir apps\static\src
  mkdir apps\static\src\css
  mkdir apps\static\src\js
  mkdir apps\static\src\images
  mkdir apps\static\dist
  ```

- [ ] **T1.2.3** Crear `vite.config.js` en raíz
  ```javascript
  import { defineConfig } from 'vite';
  import { resolve } from 'path';
  
  export default defineConfig({
    root: 'apps/static/src',
    base: '/static/',
    build: {
      outDir: '../dist',
      manifest: true,
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'apps/static/src/js/main.js'),
          styles: resolve(__dirname, 'apps/static/src/css/main.scss'),
        }
      }
    },
    server: {
      port: 5173,
      origin: 'http://localhost:5173'
    }
  });
  ```

- [ ] **T1.2.4** Crear archivos base CSS/JS
  ```powershell
  # apps/static/src/css/main.scss
  echo "@import 'variables';" > apps\static\src\css\main.scss
  
  # apps/static/src/js/main.js
  echo "console.log('Vite loaded');" > apps\static\src\js\main.js
  ```

- [ ] **T1.2.5** Crear template tag `vite_tags.py`
  ```powershell
  mkdir apps\home\templatetags
  New-Item apps\home\templatetags\__init__.py
  ```
  
  Contenido de `apps/home/templatetags/vite_tags.py`:
  ```python
  import json
  from django import template
  from django.conf import settings
  from django.utils.safestring import mark_safe
  
  register = template.Library()
  
  @register.simple_tag
  def vite_asset(path):
      if settings.DEBUG:
          return mark_safe(f'<script type="module" src="http://localhost:5173/{path}"></script>')
      # Production: cargar desde manifest.json
      with open('apps/static/dist/manifest.json') as f:
          manifest = json.load(f)
          file_path = manifest[path]['file']
          return mark_safe(f'<script src="/static/{file_path}"></script>')
  ```

- [ ] **T1.2.6** Configurar `package.json` scripts
  ```json
  {
    "scripts": {
      "dev": "vite",
      "build": "vite build",
      "preview": "vite preview"
    }
  }
  ```

- [ ] **T1.2.7** Probar Vite en desarrollo
  ```powershell
  npm run dev
  # Debería abrir en http://localhost:5173
  ```

**✅ DoD**: `npm run dev` funciona, HMR activo

---

### 1.3 Infraestructura Testing ⏳
**Objetivo**: Configurar pytest y CI

#### Tareas
- [ ] **T1.3.1** Instalar dependencias testing
  ```powershell
  pip install pytest pytest-django pytest-cov pytest-xdist
  pip install factory-boy faker freezegun pytest-mock responses
  ```

- [ ] **T1.3.2** Crear `pytest.ini` en raíz
  ```ini
  [pytest]
  DJANGO_SETTINGS_MODULE = core.local
  python_files = tests.py test_*.py *_tests.py
  python_classes = Test*
  python_functions = test_*
  addopts = 
      --verbose
      --cov=apps
      --cov=consultasTango
      --cov=consultasWMS
      --cov-report=html
      --cov-report=term-missing
      --reuse-db
  ```

- [ ] **T1.3.3** Crear `conftest.py` en raíz
  ```python
  import pytest
  from django.db import connections
  
  @pytest.fixture(scope='session')
  def django_db_setup(django_db_setup, django_db_blocker):
      """Configurar fixtures para multi-DB"""
      with django_db_blocker.unblock():
          pass
  
  @pytest.fixture
  def tango_db():
      """Conexión a Tango (mi_db_2)"""
      return connections['mi_db_2']
  
  @pytest.fixture
  def wms_db():
      """Conexión a WMS (mi_db_3)"""
      return connections['mi_db_3']
  ```

- [ ] **T1.3.4** Crear test de ejemplo
  ```powershell
  mkdir apps\home\tests
  New-Item apps\home\tests\__init__.py
  ```
  
  En `apps/home/tests/test_example.py`:
  ```python
  import pytest
  
  def test_example():
      assert 1 + 1 == 2
  
  @pytest.mark.django_db
  def test_database_connection(db):
      from django.contrib.auth.models import User
      user = User.objects.create_user('test', 'test@test.com', 'pass')
      assert user.username == 'test'
  ```

- [ ] **T1.3.5** Ejecutar tests
  ```powershell
  pytest
  # Debe pasar 2 tests
  ```

- [ ] **T1.3.6** Crear workflow GitHub Actions
  ```powershell
  mkdir .github\workflows
  ```
  
  En `.github/workflows/test.yml`:
  ```yaml
  name: Tests
  on: [push, pull_request]
  
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: '3.11'
        - name: Install dependencies
          run: pip install -r requirements.txt
        - name: Run tests
          run: pytest --cov
  ```

**✅ DoD**: pytest ejecuta correctamente, CI configurado

---

## FASE 2: Backend
**Duración**: 8 semanas | **Progreso**: [ ] 0/24 tareas

### 2.1 Capa de Servicios ⏳
**Objetivo**: Desacoplar lógica de vistas

#### Tareas
- [ ] **T2.1.1** Crear estructura de servicios
  ```powershell
  mkdir apps\home\services
  mkdir herramientas\services
  mkdir consultasTango\services
  mkdir consultasWMS\services
  
  New-Item apps\home\services\__init__.py
  New-Item herramientas\services\__init__.py
  New-Item consultasTango\services\__init__.py
  New-Item consultasWMS\services\__init__.py
  ```

- [ ] **T2.1.2** Crear `BaseService`
  
  En `apps/home/services/base.py`:
  ```python
  from typing import Optional
  from django.contrib.auth.models import User
  import logging
  
  logger = logging.getLogger(__name__)
  
  class BaseService:
      """Clase base para servicios de negocio."""
      
      def __init__(self, user: Optional[User] = None):
          self.user = user
      
      def validate_permissions(self, required_permission: str) -> bool:
          """Validar permisos del usuario."""
          if not self.user:
              return False
          return self.user.has_perm(required_permission)
      
      def log_action(self, action: str, details: dict):
          """Registrar acción en logs."""
          logger.info(f"Action: {action} | User: {self.user} | Details: {details}")
  ```

- [ ] **T2.1.3** Migrar primera función de vista a servicio
  
  Ejemplo en `herramientas/services/turno_service.py`:
  ```python
  from apps.home.services.base import BaseService
  from typing import Dict, Any
  
  class TurnoService(BaseService):
      """Servicio para gestión de turnos."""
      
      def crear_turno(self, data: Dict[str, Any]) -> Dict[str, Any]:
          """
          Crear un nuevo turno.
          
          Args:
              data: Diccionario con datos del turno
                    {'proveedor': str, 'fecha': str, 'hora': str}
          
          Returns:
              Dict con resultado {'success': bool, 'turno_id': int}
          """
          # Lógica de negocio aquí
          self.log_action('crear_turno', data)
          return {'success': True, 'turno_id': 123}
  ```

- [ ] **T2.1.4** Refactorizar vista para usar servicio
  
  En `herramientas/views.py`:
  ```python
  # ANTES:
  def registro_turno(request):
      if request.method == 'POST':
          # 50 líneas de lógica aquí
          pass
  
  # DESPUÉS:
  from herramientas.services.turno_service import TurnoService
  
  def registro_turno(request):
      service = TurnoService(user=request.user)
      if request.method == 'POST':
          result = service.crear_turno(request.POST.dict())
          if result['success']:
              messages.success(request, 'Turno creado')
          return redirect('turno_list')
      return render(request, 'herramientas/turno_form.html')
  ```

- [ ] **T2.1.5** Repetir para 10+ funciones más críticas
  - `herramientas/views.py`: `get_nombre_proveedor`, `editar_turno`, `eliminar_turno`
  - `consultasTango/views.py`: funciones de stock
  - `consultasWMS/views.py`: funciones de ubicaciones

**✅ DoD**: 50% vistas usando servicios

---

### 2.2 Refactorización SQL ⏳
**Objetivo**: Eliminar SQL injection

#### Tareas
- [ ] **T2.2.1** Auditar `apps/home/SQL/Sql_Tango.py`
  ```powershell
  # Identificar líneas con concatenación de strings:
  Select-String -Path "apps\home\SQL\Sql_Tango.py" -Pattern "sql = .*\+.*'"
  ```

- [ ] **T2.2.2** Refactorizar `validar_factManualCargada()`
  
  **Antes**:
  ```python
  def validar_factManualCargada(sucursal, factura):
      sql = "DECLARE @COMPROBANTE VARCHAR(14) = '" + factura + "';"
      cursor.execute(sql)  # ⚠️ VULNERABLE
  ```
  
  **Después**:
  ```python
  def validar_factManualCargada(sucursal: str, factura: str) -> int:
      """
      Valida si una factura manual fue cargada.
      
      Args:
          sucursal: Código de sucursal (ej: '01')
          factura: Número de comprobante (ej: 'B0001-00012345')
      
      Returns:
          int: Cantidad de facturas encontradas
      """
      with connections['mi_db_4'].cursor() as cursor:
          sql = """
              SET DATEFORMAT DMY;
              DECLARE @terminal VARCHAR(20) = SUBSTRING(%s, 2, CHARINDEX('-', %s) - 2);
              DECLARE @factura INT = CAST(SUBSTRING(%s, CHARINDEX('-', %s) + 1, LEN(%s)) AS INT) - 1;
              -- resto del query
          """
          cursor.execute(sql, [factura, factura, factura, factura, factura, sucursal])
          resultado = cursor.fetchone()
          return resultado[0] if resultado else 0
  ```

- [ ] **T2.2.3** Refactorizar `validar_articulo()`
- [ ] **T2.2.4** Refactorizar `cargar_articulo()`
- [ ] **T2.2.5** Refactorizar `validar_pedido()`
- [ ] **T2.2.6** Refactorizar todas las funciones en `Sql_WMS.py`

- [ ] **T2.2.7** Ejecutar `bandit` para validar
  ```powershell
  pip install bandit
  bandit -r apps/home/SQL/ -f json -o security_report.json
  # Debe reportar 0 vulnerabilidades SQL injection
  ```

**✅ DoD**: 0 concatenación de strings en SQL

---

### 2.3 Consolidación Templates ⏳
**Objetivo**: Eliminar duplicación

#### Tareas
- [ ] **T2.3.1** Identificar templates duplicados
  ```powershell
  # Buscar archivos con nombres similares
  Get-ChildItem -Path apps\templates -Recurse -Filter "*Plantilla*"
  ```

- [ ] **T2.3.2** Crear `IframeBaseView`
  
  En `apps/home/views/base.py`:
  ```python
  from django.contrib.auth.mixins import LoginRequiredMixin
  from django.views.generic import TemplateView
  
  class IframeBaseView(LoginRequiredMixin, TemplateView):
      """Vista base para embedear iframes externos."""
      template_name = 'layouts/iframe_wrapper.html'
      iframe_url = None
      iframe_title = None
      
      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['iframe_url'] = self.iframe_url
          context['iframe_title'] = self.iframe_title
          return context
  ```

- [ ] **T2.3.3** Crear template `layouts/iframe_wrapper.html`
  ```django
  {% extends "layouts/base.html" %}
  
  {% block content %}
  <div class="content-wrapper">
    <div class="content-header">
      <h1>{{ iframe_title }}</h1>
    </div>
    <div class="content">
      <iframe src="{{ iframe_url }}" 
              width="100%" 
              height="800px" 
              frameborder="0">
      </iframe>
    </div>
  </div>
  {% endblock %}
  ```

- [ ] **T2.3.4** Refactorizar vista iframe de ejemplo
  
  En `herramientas/views.py`:
  ```python
  # ANTES:
  def AnularRemitos(request):
      url = settings.URL_ANULAR_REMITOS
      return render(request, 'iframe_wrapper.html', {'url': url})
  
  # DESPUÉS:
  class AnularRemitosView(IframeBaseView):
      iframe_url = settings.URL_ANULAR_REMITOS
      iframe_title = 'Anular Remitos'
  ```

- [ ] **T2.3.5** Actualizar `urls.py`
  ```python
  # En herramientas/urls.py
  from .views import AnularRemitosView
  
  urlpatterns = [
      path('anular-remitos/', AnularRemitosView.as_view(), name='anular_remitos'),
  ]
  ```

- [ ] **T2.3.6** Repetir para 20+ vistas iframe
- [ ] **T2.3.7** Eliminar templates duplicados
  ```powershell
  # Después de migrar, eliminar:
  Remove-Item apps\templates\home\Plantillareportes.html
  Remove-Item apps\templates\home\Plantillareportes2.html
  ```

**✅ DoD**: Reducción 120 → 80 templates

---

## FASE 3: UI Tabler
**Duración**: 12 semanas | **Progreso**: [ ] 0/35 tareas

### 3.1 Setup Tabler ⏳
**Objetivo**: Instalar y configurar Tabler UI

#### Tareas
- [ ] **T3.1.1** Instalar Tabler
  ```powershell
  npm install @tabler/core @tabler/icons-webfont
  npm install bootstrap@5.3.0
  ```

- [ ] **T3.1.2** Crear tema Lakers
  
  En `apps/static/src/css/tabler-theme.scss`:
  ```scss
  @import '@tabler/core/src/scss/tabler';
  
  // Variables Lakers
  $primary: #1e3a8a;      // Azul Lakers
  $secondary: #fbbf24;    // Amarillo Lakers
  $success: #10b981;
  $danger: #ef4444;
  
  // Sobrescribir estilos
  .navbar-brand-image {
    height: 2.5rem;
  }
  ```

- [ ] **T3.1.3** Actualizar `vite.config.js`
  ```javascript
  resolve: {
    alias: {
      '@tabler': resolve(__dirname, 'node_modules/@tabler/core'),
    }
  }
  ```

- [ ] **T3.1.4** Crear página demo
  
  En `apps/templates/demo/components.html`:
  ```django
  {% extends "layouts/base.html" %}
  {% load vite_tags %}
  
  {% block content %}
  <h1>Componentes Tabler</h1>
  
  <!-- Buttons -->
  <button class="btn btn-primary">Primary</button>
  <button class="btn btn-secondary">Secondary</button>
  
  <!-- Cards -->
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">Card Title</h3>
    </div>
    <div class="card-body">
      Card content
    </div>
  </div>
  {% endblock %}
  ```

**✅ DoD**: Tabler compilando, demo accesible

---

### 3.2 Migración Templates Base ⏳
**Objetivo**: Crear layouts Tabler

#### Tareas Semana 1-2
- [ ] **T3.2.1** Crear `layouts/base_tabler.html`
  ```django
  <!DOCTYPE html>
  <html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Lakers Lab{% endblock %}</title>
    {% load vite_tags %}
    {% vite_asset 'css/tabler-theme.scss' %}
  </head>
  <body>
    <div class="page">
      {% include 'includes/header_tabler.html' %}
      {% include 'includes/sidebar_tabler.html' %}
      
      <div class="page-wrapper">
        <div class="page-body">
          {% block content %}{% endblock %}
        </div>
      </div>
    </div>
    {% vite_asset 'js/main.js' %}
  </body>
  </html>
  ```

- [ ] **T3.2.2** Crear `includes/header_tabler.html`
  ```django
  <header class="navbar navbar-expand-md navbar-light">
    <div class="container-xl">
      <button class="navbar-toggler" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
      <h1 class="navbar-brand">
        <img src="{% static 'assets/logo-lakers.png' %}" alt="Lakers Lab">
      </h1>
      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item dropdown">
          <a href="#" class="nav-link" data-bs-toggle="dropdown">
            {{ user.username }}
          </a>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="{% url 'logout' %}">Logout</a>
          </div>
        </div>
      </div>
    </div>
  </header>
  ```

- [ ] **T3.2.3** Crear `includes/sidebar_tabler.html`
  ```django
  <aside class="navbar navbar-vertical navbar-expand-lg">
    <div class="container-fluid">
      <div class="navbar-collapse">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="{% url 'home' %}">
              <span class="nav-link-icon">📊</span>
              <span class="nav-link-title">Dashboard</span>
            </a>
          </li>
          
          <!-- Categoría Inventario -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#navbar-inventario" 
               data-bs-toggle="dropdown">
              <span class="nav-link-icon">📦</span>
              <span class="nav-link-title">Inventario</span>
            </a>
            <div class="dropdown-menu" id="navbar-inventario">
              <a class="dropdown-item" href="#">Stock Central</a>
              <a class="dropdown-item" href="#">Ubicaciones WMS</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </aside>
  ```

- [ ] **T3.2.4** Crear `includes/footer_tabler.html`

#### Tareas Semana 3-6: Migrar App `home`
- [ ] **T3.2.5** Migrar `accounts/login.html`
  ```django
  {% extends "layouts/base_tabler.html" %}
  
  {% block content %}
  <div class="page-single">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title">Login</h2>
              <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                  <label class="form-label">Usuario</label>
                  <input type="text" name="username" class="form-control">
                </div>
                <div class="mb-3">
                  <label class="form-label">Contraseña</label>
                  <input type="password" name="password" class="form-control">
                </div>
                <button type="submit" class="btn btn-primary">Entrar</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  {% endblock %}
  ```

- [ ] **T3.2.6** Migrar `home/index.html` (dashboard)
- [ ] **T3.2.7** Migrar 10 templates de `appConsultasTango/`

#### Tareas Semana 7-8: Migrar App `herramientas`
- [ ] **T3.2.8** Migrar templates de turnos
- [ ] **T3.2.9** Migrar templates de ecommerce

#### Tareas Semana 9-10: Migrar Apps restantes
- [ ] **T3.2.10** Migrar `reportes/` (15 templates)
- [ ] **T3.2.11** Migrar `dashboard/` (8 templates)
- [ ] **T3.2.12** Migrar `extras/` (5 templates)

#### Tareas Semana 11-12: Limpieza
- [ ] **T3.2.13** Eliminar AdminLTE de `INSTALLED_APPS`
  ```python
  # En core/settings.py, COMENTAR o ELIMINAR:
  INSTALLED_APPS = [
      # 'adminlte3',           # ELIMINAR
      # 'adminlte3_theme',     # ELIMINAR
      # ... resto
  ]
  ```

- [ ] **T3.2.14** Eliminar archivos AdminLTE
  ```powershell
  Remove-Item -Recurse apps\static\admin-lte
  ```

- [ ] **T3.2.15** Actualizar todas las vistas
  ```powershell
  # Buscar y reemplazar en todos los templates:
  # {% extends "layouts/base.html" %}
  # Por:
  # {% extends "layouts/base_tabler.html" %}
  ```

**✅ DoD**: 100% templates en Tabler, AdminLTE removido

---

### 3.3 Componentes Reutilizables ⏳
**Objetivo**: Crear biblioteca de componentes

#### Tareas
- [ ] **T3.3.1** Crear directorio
  ```powershell
  mkdir apps\templates\components
  ```

- [ ] **T3.3.2** Componente `table.html`
  ```django
  {# components/table.html #}
  <div class="card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      {% if searchable %}
      <div class="card-actions">
        <input type="search" class="form-control" placeholder="Buscar...">
      </div>
      {% endif %}
    </div>
    <div class="table-responsive">
      <table class="table table-vcenter card-table">
        <thead>
          <tr>
            {% for header in headers %}
            <th>{{ header }}</th>
            {% endfor %}
          </tr>
        </thead>
        <tbody>
          {% block table_body %}{% endblock %}
        </tbody>
      </table>
    </div>
  </div>
  ```

- [ ] **T3.3.3** Componente `form.html`
- [ ] **T3.3.4** Componente `modal.html`
- [ ] **T3.3.5** Componente `card.html`
- [ ] **T3.3.6** Componente `alert.html`
- [ ] **T3.3.7** Componente `skeleton.html`

**✅ DoD**: 7 componentes creados y documentados

---

### 3.4 Django Admin Tabler ⏳
**Objetivo**: Personalizar admin

#### Tareas
- [ ] **T3.4.1** Crear templates admin
  ```powershell
  mkdir apps\templates\admin
  ```

- [ ] **T3.4.2** Crear `admin/base_site.html`
  ```django
  {% extends "admin/base.html" %}
  {% load vite_tags %}
  
  {% block extrastyle %}
    {{ block.super }}
    {% vite_asset 'css/admin-tabler.scss' %}
  {% endblock %}
  
  {% block branding %}
  <h1 class="navbar-brand">
    <img src="{% static 'assets/logo-lakers.png' %}" alt="Lakers Lab">
    Admin Panel
  </h1>
  {% endblock %}
  ```

- [ ] **T3.4.3** Crear estilos admin
  
  En `apps/static/src/css/admin-tabler.scss`:
  ```scss
  @import 'tabler-theme';
  
  #header {
    background: $primary;
    color: white;
  }
  
  .module {
    @extend .card;
  }
  
  input[type="text"],
  input[type="password"],
  select,
  textarea {
    @extend .form-control;
  }
  ```

**✅ DoD**: Admin con estilos Tabler

---

## FASE 4: Performance
**Duración**: 4 semanas | **Progreso**: [ ] 0/12 tareas

### 4.1 Auditoría Baseline ⏳

#### Tareas
- [ ] **T4.1.1** Instalar Lighthouse CI
  ```powershell
  npm install -g @lhci/cli
  ```

- [ ] **T4.1.2** Ejecutar Lighthouse en 10 páginas
  ```powershell
  # Para cada página:
  lhci autorun --url=http://localhost:8000/
  lhci autorun --url=http://localhost:8000/accounts/login/
  # ... etc
  ```

- [ ] **T4.1.3** Documentar métricas baseline
  
  Crear `docs/PERFORMANCE_BASELINE.md`:
  ```markdown
  # Baseline Performance
  
  | Página | LCP (ms) | INP (ms) | CLS | Score |
  |--------|----------|----------|-----|-------|
  | Home   | 4500     | 400      | 0.2 | 45    |
  | Login  | ...      | ...      | ... | ...   |
  ```

- [ ] **T4.1.4** Instalar django-debug-toolbar
  ```python
  # En core/local.py
  INSTALLED_APPS += ['debug_toolbar']
  MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
  INTERNAL_IPS = ['127.0.0.1']
  ```

- [ ] **T4.1.5** Identificar N+1 queries
  ```powershell
  # Navegar a páginas críticas con debug toolbar activo
  # Documentar queries duplicadas
  ```

**✅ DoD**: Baseline documentado

---

### 4.2 Optimización Frontend ⏳

#### Tareas
- [ ] **T4.2.1** Code splitting en `vite.config.js`
  ```javascript
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['@tabler/core', 'bootstrap'],
          'charts': ['chart.js'],
        }
      }
    }
  }
  ```

- [ ] **T4.2.2** Lazy loading de imágenes
  ```django
  {# En templates, cambiar: #}
  <img src="{{ image.url }}" alt="{{ image.alt }}">
  {# Por: #}
  <img src="{{ image.url }}" loading="lazy" alt="{{ image.alt }}">
  ```

- [ ] **T4.2.3** Minificación
  ```javascript
  // En vite.config.js
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      }
    }
  }
  ```

- [ ] **T4.2.4** Configurar nginx compresión
  
  En `nginx/appseed-app.conf`:
  ```nginx
  gzip on;
  gzip_types text/plain text/css application/json application/javascript;
  gzip_min_length 1000;
  ```

**✅ DoD**: Bundle <1MB, LCP <2.5s

---

### 4.3 Optimización Backend ⏳

#### Tareas
- [ ] **T4.3.1** Agregar `select_related()` en querysets
  ```python
  # ANTES:
  ubicaciones = Ubicacion.objects.all()
  
  # DESPUÉS:
  ubicaciones = Ubicacion.objects.select_related('rack', 'modulo').all()
  ```

- [ ] **T4.3.2** Configurar cache Redis
  ```python
  # En core/settings.py
  CACHES = {
      'default': {
          'BACKEND': 'django_redis.cache.RedisCache',
          'LOCATION': 'redis://127.0.0.1:6379/1',
      }
  }
  ```

- [ ] **T4.3.3** Implementar paginación
  ```python
  from django.core.paginator import Paginator
  
  def stock_list(request):
      stock_list = StockCentral.objects.all()
      paginator = Paginator(stock_list, 50)
      page = request.GET.get('page')
      stock = paginator.get_page(page)
      return render(request, 'stock_list.html', {'stock': stock})
  ```

**✅ DoD**: TTFB <600ms, 0 N+1 queries

---

## FASE 5: Testing & Docs
**Duración**: 5 semanas | **Progreso**: [ ] 0/15 tareas

### 5.1 Tests Unitarios ⏳

#### Tareas
- [ ] **T5.1.1** Tests servicios `herramientas/`
  
  En `herramientas/tests/test_turno_service.py`:
  ```python
  import pytest
  from herramientas.services.turno_service import TurnoService
  
  @pytest.mark.django_db
  class TestTurnoService:
      def test_crear_turno_valido(self, user):
          service = TurnoService(user=user)
          data = {'proveedor': 'PROV001', 'fecha': '2025-12-01'}
          turno = service.crear_turno(data)
          assert turno['success'] == True
  ```

- [ ] **T5.1.2** Tests funciones SQL
- [ ] **T5.1.3** Alcanzar 80% coverage

**✅ DoD**: Coverage >80%

---

### 5.2 Tests E2E ⏳

#### Tareas
- [ ] **T5.2.1** Instalar Playwright
  ```powershell
  npm install -D @playwright/test
  npx playwright install
  ```

- [ ] **T5.2.2** Crear `playwright.config.ts`
  ```typescript
  import { defineConfig } from '@playwright/test';
  
  export default defineConfig({
    testDir: './tests/e2e',
    use: {
      baseURL: 'http://localhost:8000',
    },
  });
  ```

- [ ] **T5.2.3** Test login
  
  En `tests/e2e/auth.spec.ts`:
  ```typescript
  import { test, expect } from '@playwright/test';
  
  test('login flow', async ({ page }) => {
    await page.goto('/accounts/login/');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/');
  });
  ```

- [ ] **T5.2.4** Tests para 5 flujos críticos

**✅ DoD**: 5 flujos E2E pasando

---

### 5.3 Documentación ⏳

#### Tareas
- [ ] **T5.3.1** Actualizar `README.md`
  
  ```markdown
  # Lakers Lab AdminWeb
  
  ## Stack
  - Django 5.1.3
  - Tabler UI
  - Vite
  
  ## Instalación
  \`\`\`powershell
  python -m venv env
  .\env\Scripts\activate
  pip install -r requirements.txt
  npm install
  npm run dev  # Terminal separada
  python manage.py runserver --settings=core.local
  \`\`\`
  ```

- [ ] **T5.3.2** Crear `docs/ARCHITECTURE.md`
- [ ] **T5.3.3** Crear `docs/API.md`
- [ ] **T5.3.4** Crear `docs/CONTRIBUTING.md`

**✅ DoD**: Docs completas

---

## 📊 Tracking de Progreso

### Resumen por Fase
```
Fase 1: ⬜⬜⬜⬜⬜⬜ 0/18 (0%)
Fase 2: ⬜⬜⬜⬜⬜⬜ 0/24 (0%)
Fase 3: ⬜⬜⬜⬜⬜⬜ 0/35 (0%)
Fase 4: ⬜⬜⬜⬜⬜⬜ 0/12 (0%)
Fase 5: ⬜⬜⬜⬜⬜⬜ 0/15 (0%)

TOTAL: 0/104 tareas (0%)
```

### Velocidad Estimada
- **Tareas/Semana**: 3-4 tareas
- **Semanas Totales**: 35 semanas
- **Completado**: 0 semanas

### Próxima Tarea
🎯 **T1.1.1**: Auditar `requirements.txt`

---

## 🚀 Comandos Rápidos

### Desarrollo
```powershell
# Backend
.\env\Scripts\activate
python manage.py runserver --settings=core.local

# Frontend (terminal separada)
npm run dev

# Tests
pytest
pytest --cov

# E2E
npx playwright test
```

### Build Production
```powershell
npm run build
python manage.py collectstatic --noinput
```

### Git Workflow
```powershell
# Nueva feature
git checkout -b feature/nombre-tarea
# ... trabajar en código ...
git add .
git commit -m "feat: descripción de la tarea"
git push origin feature/nombre-tarea
# Crear Pull Request
```

---

## 📝 Notas para Agente de Codificación

### Convenciones
- ✅ Marcar tarea como completa solo cuando pasa todos los tests
- 📝 Documentar decisiones técnicas en comentarios
- 🧪 Escribir tests antes de implementar (TDD cuando sea posible)
- 🔍 Ejecutar `bandit` y `pytest` antes de cada commit

### Prioridades
1. **Seguridad**: Eliminar SQL injection es crítico
2. **Tests**: Mantener coverage >70%
3. **Performance**: LCP <2.5s en páginas clave
4. **UX**: Responsive en mobile/tablet/desktop

### Recursos
- [Roadmap Completo](./ROADMAP_MODERNIZACION.md)
- [Copilot Instructions](./.github/copilot-instructions.md)
- Django Docs: https://docs.djangoproject.com/en/5.1/
- Tabler Docs: https://tabler.io/docs

---

**Última actualización**: 28/11/2025  
**Próxima revisión**: Al completar Fase 1
