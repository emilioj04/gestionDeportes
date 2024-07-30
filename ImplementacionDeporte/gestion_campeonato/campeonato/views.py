from django.shortcuts import render, redirect
from .models import Campeonato, Equipo, Deportista, Inscripcion
from .forms import InscripcionEquipoForm, InscripcionJugadoresForm

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