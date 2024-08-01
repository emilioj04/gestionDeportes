from django.shortcuts import render, redirect
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

def crear_partido(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            # Crear un resultado y luego el partido
            anotacion_equipo1 = form.cleaned_data['anotacion_equipo1']
            anotacion_equipo2 = form.cleaned_data['anotacion_equipo2']
            empate = form.cleaned_data['empate']
            equipo1 = form.cleaned_data['equipo1']
            equipo2 = form.cleaned_data['equipo2']
            
            resultado = Resultado(
                anotacion_equipo1=anotacion_equipo1,
                anotacion_equipo2=anotacion_equipo2,
                empate=empate,
                equipo_ganador=equipo1 if anotacion_equipo1 > anotacion_equipo2 else equipo2,
                equipo_perdedor=equipo2 if anotacion_equipo1 > anotacion_equipo2 else equipo1
            )
            if empate:
                resultado.equipo_ganador = None
                resultado.equipo_perdedor = None
            resultado.save()
            
            partido = Partido(
                nro_partido=form.cleaned_data['nro_partido'],
                fecha=form.cleaned_data['fecha'],
                equipo1=equipo1,
                equipo2=equipo2,
                resultado=resultado
            )
            partido.save()

            return redirect('home')
    else:
        form = PartidoForm()
    return render(request, 'campeonato/crear_partido.html', {'form': form})
