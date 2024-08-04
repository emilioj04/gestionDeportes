from django.urls import path
from . import views
from .views import detalle_equipo_por_campeonato

urlpatterns = [
    path('', views.home, name='home'),
    path('crear_campeonato/', views.crear_campeonato, name='crear_campeonato'),
    path('crear_equipo/', views.crear_equipo, name='crear_equipo'),
    path('inscribir_equipo/', views.inscribir_equipo, name='inscribir_equipo'),
    path('lista_campeonatos/', views.lista_campeonatos, name='lista_campeonatos'),
    path('detalle_campeonato/<int:campeonato_id>/', views.detalle_campeonato, name='detalle_campeonato'),
    path('detalle_equipo/<int:equipo_id>/<int:campeonato_id>/', views.detalle_equipo_por_campeonato, name='detalle_equipo_por_campeonato'),
    path('agregar_deportista/<int:equipo_id>/<int:campeonato_id>/', views.agregar_deportista, name='agregar_deportista'),
    path('detalle_deportista/<int:deportista_id>/', views.detalle_deportista, name='detalle_deportista'),
    path('eliminar_equipo/<int:equipo_id>/<int:campeonato_id>/', views.eliminar_equipo, name='eliminar_equipo'),
    path('eliminar_deportista/<int:deportista_id>/', views.eliminar_deportista, name='eliminar_deportista'),
    path('inicializar_campeonato/<int:campeonato_id>/', views.inicializar_campeonato, name='inicializar_campeonato'),
]
