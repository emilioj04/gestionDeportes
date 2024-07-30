from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscribir_equipo/', views.inscribir_equipo, name='inscribir_equipo'),
    path('inscribir_jugadores/<int:inscripcion_id>/', views.inscribir_jugadores, name='inscribir_jugadores'),
    # Otras rutas...
]
