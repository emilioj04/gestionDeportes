from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def agregar_deportista(request):
    if request.method == 'POST':
        form = InscripcionDeportistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InscripcionDeportistaForm()
    return render(request, 'campeonato/agregar_deportista.html', {'form': form})


def inscribir_equipo(request):
    if request.method == 'POST':
        form = InscripcionEquipoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            return redirect('inscribir_jugadores', inscripcion_id=inscripcion.id)
    else:
        form = InscripcionEquipoForm()
    return render(request, 'campeonato/inscripcion_equipo_form.html', {'form': form})

def inscribir_jugadores(request, inscripcion_id):
    inscripcion = Inscripcion.objects.get(id=inscripcion_id)
    if request.method == 'POST':
        form = InscripcionJugadoresForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            return redirect('campeonato_list')
    else:
        form = InscripcionJugadoresForm(instance=inscripcion)
    return render(request, 'campeonato/inscripcion_jugadores_form.html', {'form': form})

def home(request):
    return render(request, 'campeonato/home.html')

def crear_campeonato(request):
    if request.method == 'POST':
        form = CampeonatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CampeonatoForm()
    return render(request, 'campeonato/crear_campeonato.html', {'form': form})

def crear_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EquipoForm()
    return render(request, 'campeonato/crear_equipo.html', {'form': form})

def listar_equipos_por_campeonato(request):
    campeonatos = Campeonato.objects.all()
    campeonatos_equipos = []
    for campeonato in campeonatos:
        equipos = Inscripcion.objects.filter(campeonato=campeonato).select_related('equipo')
        campeonatos_equipos.append((campeonato, equipos))
    return render(request, 'campeonato/listar_equipos_por_campeonato.html', {'campeonatos_equipos': campeonatos_equipos})

def listar_jugadores_equipo(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    jugadores = inscripcion.jugadores.all()
    return render(request, 'campeonato/listar_jugadores_equipo.html', {'inscripcion': inscripcion, 'jugadores': jugadores})


def agregar_jugador(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    if request.method == 'POST':
        form = InscripcionDeportistaForm(request.POST)
        if form.is_valid():
            jugador = form.save()
            inscripcion.jugadores.add(jugador)
            return redirect('listar_jugadores_equipo', inscripcion_id=inscripcion_id)
    else:
        form = InscripcionDeportistaForm()
    return render(request, 'campeonato/agregar_jugador.html', {'form': form, 'inscripcion': inscripcion})


def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(Deportista, id=jugador_id)
    if request.method == 'POST':
        form = InscripcionDeportistaForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            inscripcion_id = jugador.inscripcion_set.first().id  # Obtener el ID de la inscripción
            return redirect('listar_jugadores_equipo', inscripcion_id=inscripcion_id)
    else:
        form = InscripcionDeportistaForm(instance=jugador)
    return render(request, 'campeonato/editar_jugador.html', {'form': form, 'jugador': jugador})

def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(Deportista, id=jugador_id)
    inscripcion_id = jugador.inscripcion_set.first().id  # Obtener el ID de la inscripción
    if request.method == 'POST':
        jugador.delete()
        return redirect('listar_jugadores_equipo', inscripcion_id=inscripcion_id)
    return render(request, 'campeonato/eliminar_jugador.html', {'jugador': jugador})
