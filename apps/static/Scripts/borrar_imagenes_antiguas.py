import os
import time
import logging
from datetime import datetime, timedelta
from core.settings import MEDIA_ROOT

# Configurar el logging
logging.basicConfig(filename='log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Directorio donde se encuentran las imágenes
ruta = MEDIA_ROOT

# Fecha límite (últimos 120 días)
fecha_limite = datetime.now() - timedelta(days=120)

# Extensiones de imágenes permitidas
extensiones_imagenes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def borrar_imagenes_antiguas(carpeta):
    directorio = os.path.join(ruta, carpeta)
    # print("Directorio:", directorio)
    try:
        for filename in os.listdir(directorio):
            ruta_archivo = os.path.join(directorio, filename)
            if os.path.isfile(ruta_archivo):
                extension = os.path.splitext(filename)[1].lower()
                if extension in extensiones_imagenes:
                    tiempo_creacion = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
                    if tiempo_creacion < fecha_limite:
                        try:
                            os.remove(ruta_archivo)
                            print(f"Archivo borrado: {filename}")
                        except Exception as e:
                            logging.error(f"No se pudo borrar el archivo {filename}")
    except Exception as e:
        logging.error(f"Error al borrar archivos: {e}")

if __name__ == "__main__":
    borrar_imagenes_antiguas('images')
    borrar_imagenes_antiguas('imgTempEcommerce')
    logging.info(f"Proceso ejecutado correctamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # print("Proceso completado. Revise el archivo log.txt para ver si hubo errores.")
