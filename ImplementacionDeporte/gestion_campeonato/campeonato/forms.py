from django import forms
from .models import *
from django.shortcuts import render, redirect


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'identificacion', 'genero']

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nombre', 'tipo_campeonato', 'deporte', 'nro_equipos', 'nro_jugadores']


class InscripcionEquipoForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['equipo', 'campeonato']

class InscripcionDeportistaForm(forms.ModelForm):
    class Meta:
        model = Deportista
        fields = ['identificacion', 'nombre', 'genero', 'numero']

class InscripcionJugadoresForm(forms.ModelForm):
    jugadores = forms.ModelMultipleChoiceField(queryset=Deportista.objects.all())

    class Meta:
        model = Inscripcion
        fields = ['jugadores']

    def clean(self):
        cleaned_data = super().clean()
        equipo = cleaned_data.get('equipo')
        campeonato = cleaned_data.get('campeonato')
        jugadores = cleaned_data.get('jugadores')

        if len(jugadores) != campeonato.nro_jugadores:
            raise forms.ValidationError(f"El número de jugadores debe ser {campeonato.nro_jugadores}.")

        return cleaned_data

class PartidoForm(forms.ModelForm):
    equipo1 = forms.ModelChoiceField(queryset=Equipo.objects.all())
    equipo2 = forms.ModelChoiceField(queryset=Equipo.objects.all())
    anotacion_equipo1 = forms.IntegerField()
    anotacion_equipo2 = forms.IntegerField()
    empate = forms.BooleanField(required=False)

    class Meta:
        model = Partido
        fields = ['nro_partido', 'fecha', 'equipo1', 'equipo2', 'anotacion_equipo1', 'anotacion_equipo2', 'empate']

    def clean(self):
        cleaned_data = super().clean()
        equipo1 = cleaned_data.get('equipo1')
        equipo2 = cleaned_data.get('equipo2')
        anotacion_equipo1 = cleaned_data.get('anotacion_equipo1')
        anotacion_equipo2 = cleaned_data.get('anotacion_equipo2')
        empate = cleaned_data.get('empate')

        if equipo1 == equipo2:
            raise forms.ValidationError("Los equipos no pueden ser iguales.")

        if anotacion_equipo1 == anotacion_equipo2 and not empate:
            raise forms.ValidationError("Si las anotaciones son iguales, el partido debe ser marcado como empate.")

        if anotacion_equipo1 != anotacion_equipo2 and empate:
            raise forms.ValidationError("Si las anotaciones son diferentes, el partido no puede ser marcado como empate.")

        return cleaned_data

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
