from django.contrib import admin
from .models import Campeonato, Equipo, Deportista, Participacion

class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'deporte', 'genero', 'tipo', 'nro_equipos', 'nro_deportistas', 'fecha_inicio', 'fecha_fin', 'inicializado')
    search_fields = ('nombre', 'deporte')
    list_filter = ('deporte', 'genero', 'tipo')
    ordering = ('-fecha_inicio',)

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'deporte', 'genero')
    search_fields = ('nombre', 'deporte')
    list_filter = ('deporte', 'genero')
    ordering = ('nombre',)

class DeportistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'identificacion', 'genero', 'numero', 'fecha_nacimiento', 'participacion')
    search_fields = ('nombre', 'apellido', 'identificacion', 'participacion__equipo__nombre')
    list_filter = ('genero', 'participacion__equipo')
    ordering = ('apellido', 'nombre')

admin.site.register(Campeonato, CampeonatoAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Deportista, DeportistaAdmin)
admin.site.register(Participacion)
