from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Arrendador(Persona):
    empresa = models.CharField(max_length=100, blank=True, null=True)
    experiencia = models.IntegerField(default=0, help_text="Años de experiencia como Arrendador.")

    def __str__(self):
        return f"Arrendador: {self.nombres} {self.apellidos}"


class Arrendatario(Persona):
    ingresos_mensuales = models.DecimalField(max_digits=10, decimal_places=2, help_text="Ingresos mensuales del Arrendatario")
    ocupacion = models.CharField(max_length=100, help_text="Ocupación del arrendatario")
    referencias = models.TextField(blank=True, null=True, help_text="Referencias anteriores")

    def __str__(self):
        return f"Arrendatario: {self.nombres} {self.apellidos}"

class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('oficina', 'Oficina'),
        ('local_comercial', 'Local Comercial'),
        ('terreno', 'Terreno'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    m2_construidos = models.DecimalField(max_digits=5, decimal_places=2)
    m2_totales = models.DecimalField(max_digits=5, decimal_places=2)
    estacionamientos = models.IntegerField(default=0)
    habitaciones = models.IntegerField(default=1)
    banos = models.IntegerField(default=1)
    direccion = models.CharField(max_length=200)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='inmuebles')
    tipo_inmueble = models.CharField(max_length=50, choices=TIPO_INMUEBLE_CHOICES, default='casa')
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    arrendador = models.ForeignKey(Arrendador, on_delete=models.CASCADE, null=True, blank=True, related_name='inmuebles')

    class Meta:
        permissions = [
            ("can_view_inmueble", "Puede ver inmueble"),
            ("can_edit_inmueble", "Puede editar inmueble"),
            ("can_delete_inmueble", "Puede eliminar inmueble"),
        ]

    def __str__(self):
        return self.nombre


class SolicitudArriendo(models.Model):
    ESTADO_SOLICITUD_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='solicitudes')
    arrendatario = models.ForeignKey(Arrendatario, on_delete=models.CASCADE, related_name='solicitudes')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')
    comentario = models.TextField(blank=True, null=True, help_text="Comentarios adicionales")

    def __str__(self):
        return f"Solicitud de {self.arrendatario} para {self.inmueble} - {self.estado}"
