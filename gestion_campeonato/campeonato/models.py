from django.db import models

class Participacion(models.Model):
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    campeonato = models.ForeignKey('Campeonato', on_delete=models.CASCADE)
    deportistas = models.ManyToManyField('Deportista', blank=True, related_name='participaciones')

    class Meta:
        unique_together = ('equipo', 'campeonato')

class Campeonato(models.Model):
    DEPORTE_CHOICES = [
        ('futbol', 'Fútbol'),
        ('baloncesto', 'Baloncesto'),
    ]

    GENERO_CHOICES = [
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
    ]

    TIPO_CHOICES = [
        ('liga', 'Liga'),
        ('eliminatoria', 'Eliminatoria'),
        ('grupos', 'Grupos'),
    ]

    nombre = models.CharField(max_length=200)
    deporte = models.CharField(max_length=20, choices=DEPORTE_CHOICES)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nro_equipos = models.PositiveIntegerField()
    nro_deportistas = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    equipos = models.ManyToManyField('Equipo', through='Participacion', blank=True)
    inicializado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    NOMBRE_DEPORTE_CHOICES = [
        ('futbol', 'Fútbol'),
        ('baloncesto', 'Baloncesto'),
    ]

    GENERO_CHOICES = [
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
    ]

    nombre = models.CharField(max_length=200)
    deporte = models.CharField(max_length=20, choices=NOMBRE_DEPORTE_CHOICES)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)

    def __str__(self):
        return self.nombre

class Deportista(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    genero = models.CharField(max_length=20, choices=Equipo.GENERO_CHOICES)
    numero = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField()
    participacion = models.ForeignKey('Participacion', on_delete=models.CASCADE, related_name='deportistas_participacion')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
