from django import forms
from .models import Equipo, Deportista, Campeonato, Inscripcion

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
