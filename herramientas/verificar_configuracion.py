"""
Script de Verificación - Plantilla VTEX
Este script verifica que todo esté configurado correctamente para servir
la plantilla AltaArtVtex.xls en desarrollo local.
"""

import os
import sys

def verificar_configuracion():
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN - PLANTILLA VTEX")
    print("=" * 70)
    print()
    
    # Obtener la ruta base del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    errores = []
    advertencias = []
    exitos = []
    
    # 1. Verificar que existe la plantilla
    print("1️⃣  Verificando plantilla...")
    plantilla_path = os.path.join(project_root, 'media', 'AltaArtVtex.xls')
    if os.path.exists(plantilla_path):
        size = os.path.getsize(plantilla_path)
        exitos.append(f"✅ Plantilla existe: {plantilla_path}")
        exitos.append(f"   Tamaño: {size} bytes")
    else:
        errores.append(f"❌ Plantilla NO existe: {plantilla_path}")
        print("   💡 Solución: Ejecutar crear_plantilla_vtex.py")
    print()
    
    # 2. Verificar .env
    print("2️⃣  Verificando archivo .env...")
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            contenido = f.read()
            if 'DEBUG=True' in contenido:
                exitos.append("✅ .env existe con DEBUG=True")
            else:
                advertencias.append("⚠️  .env existe pero DEBUG no es True")
                print("   💡 Asegúrate de tener DEBUG=True en .env")
    else:
        errores.append("❌ Archivo .env NO existe")
    print()
    
    # 3. Verificar settings.py
    print("3️⃣  Verificando settings.py...")
    settings_path = os.path.join(project_root, 'core', 'settings.py')
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'MEDIA_ROOT' in contenido and 'MEDIA_URL' in contenido:
                exitos.append("✅ settings.py tiene MEDIA_ROOT y MEDIA_URL")
            else:
                errores.append("❌ settings.py NO tiene configuración de MEDIA")
    else:
        errores.append("❌ settings.py NO existe")
    print()
    
    # 4. Verificar urls.py
    print("4️⃣  Verificando urls.py...")
    urls_path = os.path.join(project_root, 'core', 'urls.py')
    if os.path.exists(urls_path):
        with open(urls_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'static(settings.MEDIA_URL' in contenido:
                exitos.append("✅ urls.py tiene configuración de static() para media")
            else:
                errores.append("❌ urls.py NO tiene static() para MEDIA_URL")
                print("   💡 Solución: Agregar al final de urls.py:")
                print("   if settings.DEBUG:")
                print("       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)")
    else:
        errores.append("❌ urls.py NO existe")
    print()
    
    # 5. Verificar carpeta media
    print("5️⃣  Verificando carpeta media...")
    media_dir = os.path.join(project_root, 'media')
    if os.path.exists(media_dir):
        archivos = os.listdir(media_dir)
        exitos.append(f"✅ Carpeta media existe con {len(archivos)} archivo(s)")
        if 'AltaArtVtex.xls' in archivos:
            exitos.append("✅ AltaArtVtex.xls está en la carpeta media")
    else:
        errores.append("❌ Carpeta media NO existe")
    print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print()
    
    if exitos:
        print("✅ ÉXITOS:")
        for exito in exitos:
            print(f"   {exito}")
        print()
    
    if advertencias:
        print("⚠️  ADVERTENCIAS:")
        for advertencia in advertencias:
            print(f"   {advertencia}")
        print()
    
    if errores:
        print("❌ ERRORES:")
        for error in errores:
            print(f"   {error}")
        print()
        print("🔧 ACCIONES REQUERIDAS:")
        print("   1. Corregir los errores listados arriba")
        print("   2. Reiniciar el servidor Django")
        print("   3. Ejecutar este script nuevamente")
        print()
        return False
    else:
        print("🎉 ¡TODO ESTÁ CORRECTO!")
        print()
        print("📝 PRÓXIMOS PASOS:")
        print("   1. Asegúrate de que el servidor Django esté corriendo:")
        print("      python manage.py runserver")
        print()
        print("   2. Prueba la URL directa en tu navegador:")
        print("      http://127.0.0.1:8000/media/AltaArtVtex.xls")
        print()
        print("   3. Ve a la interfaz web y haz clic en 'Descargar plantilla'")
        print()
        return True

if __name__ == "__main__":
    try:
        resultado = verificar_configuracion()
        sys.exit(0 if resultado else 1)
    except Exception as e:
        print(f"❌ Error al ejecutar verificación: {e}")
        sys.exit(1)
