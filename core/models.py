from django.db.models import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


class Pais(models.Model):
    nombre = models.CharField(max_length=100,unique=True,verbose_name="País")

    def __str__(self):
        return self.nombre


class Liga(models.Model):
    nombre = models.CharField(max_length=100,unique=True,verbose_name="Liga")

    def __str__(self):
        return self.nombre

class Club(models.Model):
    nombre = models.CharField(max_length=100,unique=True,verbose_name="Nombre Club")
    pais = models.ForeignKey(Pais,on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True,verbose_name="Nombre de Usuario")
    email = models.EmailField(unique=True,verbose_name="Correo Electrónico")
    password = models.CharField(max_length=8, verbose_name="Contraseña")
    nombre = models.CharField(max_length=100,blank=True,verbose_name="Nombre")
    apellidos = models.CharField(max_length=100,blank=True,verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.username

class Carta_jugador(models.Model):

    POSICIONES = [
        ('POR', 'Portero'),
        ('DFC', 'Defensa Central'),
        ('LTI', 'Lateral Izquierdo'),
        ('LTD', 'Lateral Derecho'),
        ('MC', 'Medio Centro'),
        ('MI', 'Medio Izquierdo'),
        ('MD', 'Medio Derecho'),
        ('DC', 'Delantero Centro'),
        ('MP', 'Media Punta'),
    ]
    nombre = models.CharField(max_length=100,verbose_name="Nombre Jugador", null=False)
    pais = models.ForeignKey(Pais,on_delete=models.CASCADE,null=False)
    posicion = models.CharField(max_length=3, choices=POSICIONES,verbose_name="Posicion")
    ritmo = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Ritmo")
    tiro = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Tiro")
    pase = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Pase")
    regate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Regate")
    defensa = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Defensa")
    fisico = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],null=False,verbose_name="Físico")
    liga = models.ForeignKey(Liga,on_delete=models.CASCADE,null=False)
    club = models.ForeignKey(Club,on_delete=models.CASCADE,null=False)
    activo = models.BooleanField(default=True)
    puntuacion_total = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],verbose_name="Puntuación General")

    def __str__(self):
        return self.nombre

class Equipo_usuario(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False)
    nombre = models.CharField(max_length=100,verbose_name="Nombre Equipo")
    fecha_creacion = models.DateField(auto_now_add=True)
    cartas = models.ManyToManyField(Carta_jugador)

    def __str__(self):
        return self.nombre

