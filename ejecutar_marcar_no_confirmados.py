"""
Script para ejecutar automáticamente el marcado de turnos NO CONFIRMADOS
Ejecutar este script mediante Programador de Tareas de Windows
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.local')
sys.path.append(r'C:\Users\eduardo.berga\Desktop\Proyectos\Lakers_Lab\Adminweb')
django.setup()

from apps.home.SQL.Sql_Tango import marcar_turnos_no_confirmados
from datetime import datetime

# Ejecutar marcado
print(f"[{datetime.now()}] Iniciando marcado de turnos NO CONFIRMADOS...")

try:
    turnos_marcados = marcar_turnos_no_confirmados()
    
    if turnos_marcados > 0:
        print(f"[{datetime.now()}] ✓ Se marcaron {turnos_marcados} turno(s) como NO CONFIRMADO")
    else:
        print(f"[{datetime.now()}] ✓ No hay turnos para marcar")
        
except Exception as e:
    print(f"[{datetime.now()}] ✗ Error: {e}")
    sys.exit(1)
