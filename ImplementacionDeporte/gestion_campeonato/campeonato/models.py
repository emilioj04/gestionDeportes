from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.IntegerField(unique=True)
    genero = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

class Deportista(models.Model):
    identificacion = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=10)
    numero = models.IntegerField()

    def __str__(self):
        return self.nombre

class Campeonato(models.Model):
    LIGA = 'LIGA'
    MUERTE_SUBITA = 'MUERTE_SUBITA'
    FASE_GRUPOS = 'FASE_GRUPOS'
    TIPOS_CAMPEONATO = [
        (LIGA, 'Liga'),
        (MUERTE_SUBITA, 'Muerte Súbita'),
        (FASE_GRUPOS, 'Fase de Grupos'),
    ]

    nombre = models.CharField(max_length=100)
    tipo_campeonato = models.CharField(max_length=20, choices=TIPOS_CAMPEONATO)
    deporte = models.CharField(max_length=50)
    nro_equipos = models.IntegerField()
    nro_jugadores = models.IntegerField()
    equipos = models.ManyToManyField('Equipo', through='Inscripcion')
    inicializado = models.BooleanField(default=False)

class Inscripcion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    jugadores = models.ManyToManyField(Deportista)

    class Meta:
        unique_together = ('equipo', 'campeonato')

    def __str__(self):
        return f"{self.equipo.nombre} en {self.campeonato.nombre}"

class Posicion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    puntos = models.IntegerField()
    partidos_jugados = models.IntegerField()
    partidos_ganados = models.IntegerField()
    partidos_empatados = models.IntegerField()
    partidos_perdidos = models.IntegerField()

class TablaPosiciones(models.Model):
    campeonato = models.OneToOneField(Campeonato, on_delete=models.CASCADE)
    posiciones = models.ManyToManyField(Posicion)

class Resultado(models.Model):
    equipo_ganador = models.ForeignKey(Equipo, related_name='ganador', on_delete=models.SET_NULL, null=True, blank=True)
    equipo_perdedor = models.ForeignKey(Equipo, related_name='perdedor', on_delete=models.SET_NULL, null=True, blank=True)
    anotacion_equipo1 = models.IntegerField()
    anotacion_equipo2 = models.IntegerField()

class Partido(models.Model):
    nro_partido = models.IntegerField(unique=True)
    fecha = models.DateField()
    equipo1 = models.ForeignKey(Equipo, related_name='equipo1', on_delete=models.CASCADE)
    equipo2 = models.ForeignKey(Equipo, related_name='equipo2', on_delete=models.CASCADE)
    resultado = models.OneToOneField(Resultado, on_delete=models.CASCADE)

class EstadisticaEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    partidos_jugados = models.IntegerField()
    anotaciones = models.IntegerField()

class EstadisticasIndividuales(models.Model):
    deportista = models.ForeignKey(Deportista, on_delete=models.CASCADE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    partidos_jugados = models.IntegerField()
    anotaciones = models.IntegerField()
    asistencias = models.IntegerField()

class EstadisticaCampeonato(models.Model):
    campeonato = models.OneToOneField(Campeonato, on_delete=models.CASCADE)
    equipos = models.ManyToManyField(EstadisticaEquipo)
    deportistas = models.ManyToManyField(EstadisticasIndividuales)
