import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django
from django.conf import settings

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

from gestion_inmuebles.models import Inmueble

def consultar_inmuebles_por_region():
    # Obtener todos los inmuebles con solo los campos 'nombre' y 'descripcion', agrupados por región
    inmuebles = Inmueble.objects.values('comuna__region__nombre', 'nombre', 'descripcion').order_by('comuna__region__nombre')

    # Abrir archivo de texto para guardar los resultados
    with open('listado_inmuebles_por_region.txt', 'w', encoding='utf-8') as file:
        # Escribir cabecera
        file.write("Listado de Inmuebles para Arriendo - Separado por Regiones\n")
        file.write("="*50 + "\n\n")
        
        # Escribir los inmuebles por región
        current_region = None
        for inmueble in inmuebles:
            region_nombre = inmueble['comuna__region__nombre']
            if region_nombre != current_region:
                # Escribir el nombre de la región como encabezado
                file.write(f"\nRegión: {region_nombre}\n")
                file.write("-" * 50 + "\n")
                current_region = region_nombre
            
            # Escribir el nombre y la descripción del inmueble
            file.write(f"Nombre: {inmueble['nombre']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write("-" * 50 + "\n")
    
    print("Consulta completada y guardada en 'listado_inmuebles_por_region.txt'.")

# Ejecutar la consulta
if __name__ == "__main__":
    consultar_inmuebles_por_region()
