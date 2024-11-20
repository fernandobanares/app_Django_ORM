from django.contrib import admin
from .models import Inmueble, Region, Comuna

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_inmueble', 'precio_mensual', 'comuna', 'arrendador')
    search_fields = ('nombre', 'descripcion', 'direccion', 'comuna__nombre')
    list_filter = ('tipo_inmueble', 'comuna', 'arrendador')

admin.site.register(Inmueble, InmuebleAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre',) 
    search_fields = ('nombre',)
    list_filter = ('nombre',)

admin.site.register(Region, RegionAdmin)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    search_fields = ('nombre', 'region__nombre')
    list_filter = ('region',)

admin.site.register(Comuna, ComunaAdmin)


