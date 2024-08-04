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
    campeonato = inscripcion.campeonato
    if campeonato.inicializado:
        return redirect('detalles_campeonato', campeonato_id=campeonato.id)

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

def detalles_campeonato(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    inscripciones = Inscripcion.objects.filter(campeonato=campeonato)
    es_liga = campeonato.tipo_campeonato == 'Liga'
    tabla_posiciones = []

    if es_liga:
        for inscripcion in inscripciones:
            equipo = inscripcion.equipo
            partidos = Partido.objects.filter(equipo=equipo, campeonato=campeonato)
            puntos = sum([puntos_partido(partido, equipo) for partido in partidos])
            partidos_ganados = partidos.filter(resultado='G').count()
            partidos_empatados = partidos.filter(resultado='E').count()
            partidos_perdidos = partidos.filter(resultado='P').count()
            goles_hechos = sum([partido.goles_hechos for partido in partidos])
            goles_contra = sum([partido.goles_contra for partido in partidos])
            goles_diferencia = goles_hechos - goles_contra

            tabla_posiciones.append({
                'equipo': equipo,
                'puntos': puntos,
                'partidos_ganados': partidos_ganados,
                'partidos_empatados': partidos_empatados,
                'partidos_perdidos': partidos_perdidos,
                'goles_hechos': goles_hechos,
                'goles_contra': goles_contra,
                'goles_diferencia': goles_diferencia
            })

        tabla_posiciones.sort(key=lambda x: (x['puntos'], x['goles_diferencia']), reverse=True)

    return render(request, 'campeonato/detalles_campeonato.html', {
        'campeonato': campeonato,
        'inscripciones': inscripciones,
        'es_liga': es_liga,
        'tabla_posiciones': tabla_posiciones
    })

def inicializar_campeonato(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    campeonato.inicializado = True
    campeonato.save()
    return redirect('detalles_campeonato', campeonato_id=campeonato_id)

def puntos_partido(partido, equipo):
    if partido.resultado == 'G':
        return 3
    elif partido.resultado == 'E':
        return 1
    return 0

def eliminar_campeonato(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    if request.method == 'POST':
        campeonato.delete()
        return redirect('listar_equipos_por_campeonato')
    return render(request, 'campeonato/eliminar_campeonato.html', {'campeonato': campeonato})