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
    path('listar_jugadores_equipo/<int:inscripcion_id>/', views.listar_jugadores_equipo, name='listar_jugadores_equipo'),
    path('agregar_jugador/<int:inscripcion_id>/', views.agregar_jugador, name='agregar_jugador'),
    path('editar_jugador/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('eliminar_jugador/<int:jugador_id>/', views.eliminar_jugador, name='eliminar_jugador'),
    path('detalles_campeonato/<int:campeonato_id>/', views.detalles_campeonato, name='detalles_campeonato'),
    path('inicializar_campeonato/<int:campeonato_id>/', views.inicializar_campeonato, name='inicializar_campeonato'),
    path('eliminar_campeonato/<int:campeonato_id>/', views.eliminar_campeonato, name='eliminar_campeonato'),
]


