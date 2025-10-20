"""
Servidor HTTP Simple - Versión Simplificada
Sirve archivos desde la carpeta media del proyecto
"""

import http.server
import socketserver
import os

PORT = 8080

# Cambiar al directorio media
project_root = r'c:\Users\santos.garcia\Desktop\Adminweb'
media_dir = os.path.join(project_root, 'media')

print("=" * 70)
print("🚀 SERVIDOR HTTP SIMPLE")
print("=" * 70)
print(f"\n📁 Directorio: {media_dir}")

# Verificar que existe
if not os.path.exists(media_dir):
    print(f"\n❌ ERROR: No existe {media_dir}")
    input("\nPresiona Enter para salir...")
    exit(1)

# Verificar plantilla
plantilla = os.path.join(media_dir, 'AltaArtVtex.xls')
if os.path.exists(plantilla):
    size = os.path.getsize(plantilla)
    print(f"✅ Plantilla encontrada: AltaArtVtex.xls ({size} bytes)")
else:
    print("⚠️  Advertencia: Plantilla no encontrada")

print(f"\n🌐 URL: http://localhost:{PORT}/AltaArtVtex.xls")
print("\n💡 Para detener: Ctrl+C")
print("=" * 70)
print()

# Cambiar al directorio media
os.chdir(media_dir)

# Iniciar servidor
Handler = http.server.SimpleHTTPRequestHandler
try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Servidor activo en puerto {PORT}")
        print(f"📂 Sirviendo: {os.getcwd()}")
        print("\n⏳ Esperando conexiones...\n")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n🛑 Servidor detenido")
except OSError as e:
    if e.errno == 10048:
        print(f"\n❌ Error: Puerto {PORT} ya está en uso")
        print("💡 Cierra la aplicación que usa el puerto o cambia PORT en el script")
    else:
        print(f"\n❌ Error: {e}")
    input("\nPresiona Enter para salir...")
