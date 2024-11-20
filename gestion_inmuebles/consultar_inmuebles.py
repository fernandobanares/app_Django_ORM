import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django
from django.conf import settings

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_inmuebles.settings')
django.setup()

from gestion_inmuebles.models import Inmueble, Comuna

def consultar_inmuebles():
    # Obtener todos los inmuebles con solo los campos 'nombre' y 'descripcion', agrupados por comuna
    inmuebles = Inmueble.objects.values('comuna__nombre', 'nombre', 'descripcion').order_by('comuna__nombre')

    # Abrir archivo de texto para guardar los resultados
    with open('listado_inmuebles.txt', 'w', encoding='utf-8') as file:
        # Escribir cabecera
        file.write("Listado de Inmuebles para Arriendo - Separado por Comunas\n")
        file.write("="*50 + "\n\n")
        
        # Escribir los inmuebles por comuna
        current_comuna = None
        for inmueble in inmuebles:
            comuna_nombre = inmueble['comuna__nombre']
            if comuna_nombre != current_comuna:
                # Escribir el nombre de la comuna como encabezado
                file.write(f"\nComuna: {comuna_nombre}\n")
                file.write("-" * 50 + "\n")
                current_comuna = comuna_nombre
            
            # Escribir el nombre y la descripción del inmueble
            file.write(f"Nombre: {inmueble['nombre']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write("-" * 50 + "\n")
    
    print("Consulta completada y guardada en 'listado_inmuebles.txt'.")

# Ejecutar la consulta
if __name__ == "__main__":
    consultar_inmuebles()
