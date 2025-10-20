"""
Servidor Simple para Servir Archivos Media
Este servidor permite probar la descarga de la plantilla sin necesidad
de iniciar Django (útil cuando hay problemas con la base de datos).
"""

import http.server
import socketserver
import os
import webbrowser

# Configuración
PORT = 8080
# Obtener la ruta absoluta de la carpeta media
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEDIA_DIR = os.path.join(PROJECT_ROOT, 'media')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=MEDIA_DIR, **kwargs)
    
    def end_headers(self):
        # Permitir CORS para desarrollo
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def iniciar_servidor():
    print("=" * 70)
    print("🚀 SERVIDOR SIMPLE PARA ARCHIVOS MEDIA")
    print("=" * 70)
    print()
    print(f"📁 Sirviendo archivos desde: {MEDIA_DIR}")
    print(f"🌐 Puerto: {PORT}")
    print()
    
    # Verificar que la carpeta media existe
    if not os.path.exists(MEDIA_DIR):
        print(f"❌ Error: La carpeta media no existe en {MEDIA_DIR}")
        return
    
    # Verificar que la plantilla existe
    plantilla_path = os.path.join(MEDIA_DIR, 'AltaArtVtex.xls')
    if os.path.exists(plantilla_path):
        print(f"✅ Plantilla encontrada: AltaArtVtex.xls")
        size = os.path.getsize(plantilla_path)
        print(f"   Tamaño: {size} bytes")
    else:
        print(f"⚠️  Advertencia: Plantilla no encontrada")
    
    print()
    print("=" * 70)
    print("📝 URLs DISPONIBLES:")
    print("=" * 70)
    print(f"   http://localhost:{PORT}/AltaArtVtex.xls")
    print(f"   http://127.0.0.1:{PORT}/AltaArtVtex.xls")
    print()
    print("💡 Para detener el servidor, presiona Ctrl+C")
    print("=" * 70)
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Servidor iniciado en http://localhost:{PORT}/")
            print(f"🌐 Abriendo navegador...")
            print()
            
            # Abrir navegador automáticamente
            webbrowser.open(f'http://localhost:{PORT}/AltaArtVtex.xls')
            
            print("⏳ Esperando peticiones...")
            print()
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("🛑 Servidor detenido por el usuario")
    except OSError as e:
        if e.errno == 10048:  # Puerto en uso
            print(f"❌ Error: El puerto {PORT} ya está en uso")
            print(f"💡 Solución: Cambia el PORT en este script o cierra la aplicación que está usando el puerto")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        iniciar_servidor()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
