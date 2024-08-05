from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from django.db.models import Sum



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

def inscribir_equipo(request):
    if request.method == 'POST':
        form = InscripcionEquipoForm(request.POST)
        if form.is_valid():
            campeonato = form.cleaned_data['campeonato']
            equipo = form.cleaned_data['equipo']
            if campeonato.inicializado:
                return render(request, 'campeonato/inscribir_equipo.html', {
                    'form': form,
                    'error': 'No se pueden inscribir equipos en un campeonato ya inicializado.'
                })
            if equipo not in campeonato.equipos.all():
                if equipo.genero == campeonato.genero and equipo.deporte == campeonato.deporte:
                    if campeonato.equipos.count() < campeonato.nro_equipos:
                        campeonato.equipos.add(equipo)
                        campeonato.save()
                    else:
                        return render(request, 'campeonato/inscribir_equipo.html', {
                            'form': form,
                            'error': 'El campeonato ya ha alcanzado el número máximo de equipos.'
                        })
                else:
                    return render(request, 'campeonato/inscribir_equipo.html', {
                        'form': form,
                        'error': 'El género y/o deporte del equipo no coinciden con el del campeonato.'
                    })
            return redirect('lista_campeonatos')
    else:
        form = InscripcionEquipoForm()
    return render(request, 'campeonato/inscribir_equipo.html', {'form': form})

def lista_campeonatos(request):
    campeonatos = Campeonato.objects.all()
    return render(request, 'campeonato/lista_campeonatos.html', {'campeonatos': campeonatos})

def detalle_campeonato(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    equipos = campeonato.equipos.all()
    partidos = Partido.objects.filter(campeonato=campeonato)
    
    # Calcular posiciones
    posiciones = tabla_posiciones(campeonato)

    equipos_sin_deportistas_suficientes = []
    error_message = None

    if equipos.count() < 2:
        error_message = "Se necesitan al menos dos equipos para inicializar el campeonato."
    else:
        for equipo in equipos:
            deportistas_count = Deportista.objects.filter(participacion__equipo=equipo, participacion__campeonato=campeonato).count()
            if deportistas_count < 1:
                equipos_sin_deportistas_suficientes.append(equipo.nombre)
        
        if equipos_sin_deportistas_suficientes:
            error_message = "Los siguientes equipos necesitan al menos un deportista: " + ", ".join(equipos_sin_deportistas_suficientes)

    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.campeonato = campeonato
            partido.save()
            return redirect('detalle_campeonato', campeonato_id=campeonato.id)
    else:
        form = PartidoForm()

    return render(request, 'campeonato/detalle_campeonato.html', {
        'campeonato': campeonato,
        'equipos': equipos,
        'partidos': partidos,
        'posiciones': posiciones,
        'form': form,
        'error_message': error_message
    })


def detalle_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    participaciones = Participacion.objects.filter(equipo=equipo)
    campeonatos = [participacion.campeonato for participacion in participaciones]
    deportistas = Deportista.objects.filter(participacion__in=participaciones)

    puede_agregar_deportista = any(
        participacion.deportistas.count() < participacion.campeonato.nro_deportistas
        for participacion in participaciones
    )

    return render(request, 'campeonato/detalle_equipo.html', {
        'equipo': equipo,
        'deportistas': deportistas,
        'campeonatos': campeonatos,
        'puede_agregar_deportista': puede_agregar_deportista,
    })

def agregar_deportista(request, equipo_id, campeonato_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    
    try:
        participacion = Participacion.objects.get(equipo=equipo, campeonato=campeonato)
    except Participacion.DoesNotExist:
        return HttpResponse("No se encontró la participación para este equipo en el campeonato especificado.", status=404)

    if request.method == 'POST':
        form = DeportistaForm(request.POST)
        if form.is_valid():
            deportista = form.save(commit=False)
            deportista.participacion = participacion
            deportista.save()
            return redirect('detalle_equipo_por_campeonato', equipo_id=equipo.id, campeonato_id=campeonato.id)
        else:
            return render(request, 'campeonato/agregar_deportista.html', {
                'form': form,
                'equipo': equipo,
                'campeonato': campeonato,
                'error': 'Error al agregar el deportista.'
            })
    else:
        form = DeportistaForm()
    return render(request, 'campeonato/agregar_deportista.html', {'form': form, 'equipo': equipo, 'campeonato': campeonato})

def detalle_deportista(request, deportista_id):
    deportista = get_object_or_404(Deportista, id=deportista_id)
    return render(request, 'campeonato/detalle_deportista.html', {'deportista': deportista})

def eliminar_equipo(request, equipo_id, campeonato_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    
    try:
        participacion = Participacion.objects.get(equipo=equipo, campeonato=campeonato)
        participacion.delete()
    except Participacion.DoesNotExist:
        return HttpResponse("El equipo no está inscrito en este campeonato.", status=404)

    return redirect('detalle_campeonato', campeonato_id=campeonato_id)

def eliminar_deportista(request, deportista_id):
    deportista = get_object_or_404(Deportista, id=deportista_id)
    equipo_id = deportista.equipo.id
    deportista.delete()
    return redirect('detalle_equipo', equipo_id=equipo_id)

def inicializar_campeonato(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    equipos = campeonato.equipos.all()
    equipos_faltantes = []
    equipos_sin_deportistas_suficientes = []
    
    # Verifica si hay menos de dos equipos
    if equipos.count() < 2:
        return HttpResponse("Se necesitan al menos dos equipos para inicializar el campeonato.", status=400)
    
    # Verifica si cada equipo tiene al menos un deportista
    for equipo in equipos:
        try:
            participacion = Participacion.objects.get(equipo=equipo, campeonato=campeonato)
            if participacion.deportistas.count() < 1:
                equipos_sin_deportistas_suficientes.append(equipo.nombre)
        except Participacion.DoesNotExist:
            equipos_sin_deportistas_suficientes.append(equipo.nombre)
    
    # Verifica si se cumplen las advertencias
    if equipos.count() < campeonato.nro_equipos:
        equipos_faltantes.append(f'El campeonato tiene solo {equipos.count()} de los {campeonato.nro_equipos} equipos necesarios.')
    
    if any([not participacion.deportistas.count() for participacion in Participacion.objects.filter(campeonato=campeonato)]):
        equipos_sin_deportistas_suficientes.append("Algunos equipos no tienen deportistas suficientes.")
    
    if request.method == 'POST':
        if 'confirmar' in request.POST and request.POST['confirmar'] == 'si':
            # Guardar el estado de inicialización
            campeonato.inicializado = True
            campeonato.save()
            return redirect('detalle_campeonato', campeonato_id=campeonato_id)
        else:
            return redirect('detalle_campeonato', campeonato_id=campeonato_id)

    context = {
        'campeonato': campeonato,
        'equipos_faltantes': equipos_faltantes,
        'equipos_sin_deportistas_suficientes': equipos_sin_deportistas_suficientes
    }
    
    return render(request, 'campeonato/inicializar_campeonato.html', context)



def detalle_equipo_por_campeonato(request, equipo_id, campeonato_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)  
    participacion = Participacion.objects.filter(equipo=equipo, campeonato=campeonato).first()
    deportistas = Deportista.objects.filter(participacion=participacion) if participacion else []

    puede_agregar_deportista = participacion.deportistas.count() < campeonato.nro_deportistas if participacion else False

    return render(request, 'campeonato/detalle_equipo_por_campeonato.html', {
        'equipo': equipo,
        'campeonato': campeonato,
        'deportistas': deportistas,
        'puede_agregar_deportista': puede_agregar_deportista
    })

def crear_partido(request, campeonato_id):
    campeonato = get_object_or_404(Campeonato, id=campeonato_id)
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            partido = form.save(commit=False)
            if partido.equipo_local == partido.equipo_visitante:
                form.add_error('equipo_visitante', 'Un equipo no puede jugar contra sí mismo.')
            elif partido.campeonato != campeonato:
                form.add_error('campeonato', 'El partido debe pertenecer al mismo campeonato.')
            else:
                partido.save()
                return redirect('detalle_campeonato', campeonato_id=campeonato_id)
    else:
        form = PartidoForm(initial={'campeonato': campeonato})
    return render(request, 'campeonato/crear_partido.html', {'form': form, 'campeonato': campeonato})

def tabla_posiciones(campeonato):
    equipos = campeonato.equipos.all()
    posiciones = []

    for equipo in equipos:
        partidos_local = Partido.objects.filter(campeonato=campeonato, equipo_local=equipo)
        partidos_visitante = Partido.objects.filter(campeonato=campeonato, equipo_visitante=equipo)
        
        puntos_local = sum([partido.puntos_local for partido in partidos_local])
        puntos_visitante = sum([partido.puntos_visitante for partido in partidos_visitante])
        
        puntos = puntos_local + puntos_visitante
        
        posiciones.append({'equipo': equipo, 'puntos': puntos})

    return sorted(posiciones, key=lambda x: x['puntos'], reverse=True)


