from django import forms
from .models import Campeonato, Equipo, Deportista, Participacion, Partido

class CampeonatoForm(forms.ModelForm):
    nro_grupos = forms.IntegerField(required=False)
    equipos_por_grupo = forms.IntegerField(required=False, disabled=True)

    class Meta:
        model = Campeonato
        fields = ['nombre', 'deporte', 'genero', 'tipo', 'nro_equipos', 'nro_deportistas', 'fecha_inicio', 'fecha_fin', 'nro_grupos', 'equipos_por_grupo']
        
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        nro_equipos = cleaned_data.get("nro_equipos")
        nro_deportistas = cleaned_data.get("nro_deportistas")
        nro_grupos = cleaned_data.get("nro_grupos")

        if nro_equipos < 2:
            self.add_error('nro_equipos', 'El número de equipos debe ser al menos 2.')
        
        if nro_deportistas < 1:
            self.add_error('nro_deportistas', 'El número de deportistas debe ser al menos 1.')

        if tipo == 'eliminatoria':
            if not (nro_equipos and (nro_equipos & (nro_equipos - 1) == 0)):
                self.add_error('nro_equipos', 'El número de equipos debe ser una potencia de dos para campeonatos de eliminatoria.')
        
        if tipo == 'grupos':
            if not nro_grupos:
                self.add_error('nro_grupos', 'El número de grupos es requerido para campeonatos de grupos.')
            elif nro_equipos and nro_grupos and nro_equipos % nro_grupos != 0:
                self.add_error('nro_grupos', 'El número de equipos debe ser divisible por el número de grupos.')
                self.add_error('nro_equipos', 'El número de equipos debe ser divisible por el número de grupos.')
            else:
                cleaned_data['equipos_por_grupo'] = nro_equipos // nro_grupos + (nro_equipos % nro_grupos > 0)

        return cleaned_data

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

class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['fecha', 'equipo_local', 'equipo_visitante', 'goles_local', 'goles_visitante']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }