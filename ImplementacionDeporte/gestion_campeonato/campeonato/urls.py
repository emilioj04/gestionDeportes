from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscribir_equipo/', views.inscribir_equipo, name='inscribir_equipo'),
    path('inscribir_jugadores/<int:inscripcion_id>/', views.inscribir_jugadores, name='inscribir_jugadores'),
    path('agregar_deportista/', views.agregar_deportista, name='agregar_deportista'),
    path('crear_campeonato/', views.crear_campeonato, name='crear_campeonato'),
    path('crear_equipo/', views.crear_equipo, name='crear_equipo'),
    path('listar_equipos_por_campeonato/', views.listar_equipos_por_campeonato, name='listar_equipos_por_campeonato'),
    path('crear_partido/', views.crear_partido, name='crear_partido'),
]
