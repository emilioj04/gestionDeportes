from django import forms
from .models import Campeonato, Equipo, Deportista

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nombre', 'deporte', 'genero', 'tipo', 'nro_equipos', 'nro_deportistas', 'fecha_inicio', 'fecha_fin']

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'genero', 'deporte']

class DeportistaForm(forms.ModelForm):
    class Meta:
        model = Deportista
        fields = ['nombre', 'apellido', 'identificacion', 'genero', 'numero', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class InscripcionEquipoForm(forms.Form):
    campeonato = forms.ModelChoiceField(queryset=Campeonato.objects.all())
    equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
