import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_inmuebles.settings")
django.setup()

from gestion_inmuebles.models import Region, Comuna

# Lista completa de regiones y comunas de Chile
regiones_y_comunas = [
    {"region": "Región de Arica y Parinacota", "comunas": ["Arica", "Camarones", "Putre", "General Lagos"]},
    {"region": "Región de Tarapacá", "comunas": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]},
    {"region": "Región de Antofagasta", "comunas": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"]},
    {"region": "Región de Atacama", "comunas": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"]},
    {"region": "Región de Coquimbo", "comunas": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"]},
    {"region": "Región de Valparaíso", "comunas": ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví", "Casablanca", "Juan Fernández", "San Antonio", "Cartagena", "El Quisco", "El Tabo", "Algarrobo", "Quillota", "La Calera", "La Cruz", "Nogales", "Hijuelas", "San Felipe", "Los Andes", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Quilpué", "Villa Alemana", "Limache", "Olmué"]},
    {"region": "Región Metropolitana de Santiago", "comunas": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"]},
    {"region": "Región de O'Higgins", "comunas": ["Rancagua", "Machalí", "Graneros", "Doñihue", "Coltauco", "Coinco", "Olivar", "Requínoa", "Rengo", "Malloa", "San Vicente", "Pichidegua", "Peumo", "Las Cabras", "San Fernando", "Chimbarongo", "Nancagua", "Placilla", "Santa Cruz", "Pumanque", "Palmilla", "Lolol", "Peralillo", "Chépica"]},
    {"region": "Región del Maule", "comunas": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"]},
    {"region": "Región del Ñuble", "comunas": ["Chillán", "Chillán Viejo", "Quillón", "San Ignacio", "El Carmen", "Pemuco", "Yungay", "San Fabián", "Coihueco", "Pinto", "San Carlos", "Ñiquén", "San Nicolás", "Ninhue", "Treguaco", "Quirihue", "Cobquecura", "Coelemu", "Ránquil"]},
    {"region": "Región del Biobío", "comunas": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"]},
    {"region": "Región de La Araucanía", "comunas": ["Temuco", "Padre Las Casas", "Carahue", "Cholchol", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Perquenco", "Pitrufquén", "Pucon", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]},
    {"region": "Región de Los Ríos", "comunas": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"]},
    {"region": "Región de Los Lagos", "comunas": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"]},
    {"region": "Región de Aysén", "comunas": ["Coyhaique", "Lago Verde", "Aysén", "Cisnes", "Guaitecas", "Cochrane", "O’Higgins", "Tortel", "Chile Chico", "Río Ibáñez"]},
    {"region": "Región de Magallanes", "comunas": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos", "Antártica", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"]},
]

# Cargar datos en la base de datos
for region_data in regiones_y_comunas:
    region_nombre = region_data["region"]
    region, created = Region.objects.get_or_create(nombre=region_nombre)
    if created:
        print(f"Región creada: {region.nombre}")

    for comuna_nombre in region_data["comunas"]:
        comuna, created = Comuna.objects.get_or_create(nombre=comuna_nombre, region=region)
        if created:
            print(f"    Comuna creada: {comuna.nombre}")
