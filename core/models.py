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



VALIDADORES_STATS = [MinValueValidator(1), MaxValueValidator(99)]
class Atributos_portero(models.Model):
    carta = models.OneToOneField('Carta_jugador', on_delete=models.CASCADE, primary_key=True,verbose_name="Carta de Jugador")
    salto = models.IntegerField(validators=VALIDADORES_STATS,verbose_name="Salto")
    parada = models.IntegerField(validators=VALIDADORES_STATS,verbose_name="Parada")
    saque = models.IntegerField(validators=VALIDADORES_STATS,verbose_name="Saque")
    reflejos = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Reflejos")
    velocidad = models.IntegerField(validators=VALIDADORES_STATS,verbose_name="Velocidad Portero")
    posicionamiento = models.IntegerField(validators=VALIDADORES_STATS,verbose_name="Posicionamiento Portero")

    def __str__(self):
     return f"Atributos de Portero para {self.carta.nombre}"


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
    ritmo = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Ritmo")
    tiro = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Tiro")
    pase = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Pase")
    regate = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Regate")
    defensa = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Defensa")
    fisico = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Físico")
    liga = models.ForeignKey(Liga,on_delete=models.CASCADE,null=False)
    club = models.ForeignKey(Club,on_delete=models.CASCADE,null=False)
    activo = models.BooleanField(default=True)
    puntuacion_total = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],verbose_name="Puntuación General")



    def __str__(self):
        return self.nombre

    def calcular_valoracion_base(self):
        if self.posicion == 'POR':

                atributos_por = self.atributos_portero

                stats_relevantes = [
                    atributos_por.salto,
                    atributos_por.parada,
                    atributos_por.saque,
                    atributos_por.reflejos,
                    atributos_por.velocidad,
                    atributos_por.posicionamiento
                ]
                media_base = sum(stats_relevantes) / len(stats_relevantes)
        else:
            stats_relevantes = [self.ritmo, self.tiro, self.pase, self.regate, self.defensa, self.fisico]
            media_base = sum(stats_relevantes) / len(stats_relevantes)
            return round(media_base)

    def calcular_bonificacion(self):

        bonificacion = 0
        stats_totales = [self.ritmo, self.tiro, self.pase, self.regate, self.defensa, self.fisico]

        for stat in stats_totales:
            if stat > 95:
                bonificacion += 4
            elif stat > 90:
                bonificacion += 3
            elif stat > 80:
                bonificacion += 2
            elif stat >= 50:
                bonificacion += 1
            else:
                bonificacion -= 1

        return bonificacion

    def save(self, *args, **kwargs):

        puntuacion_base = self.calcular_valoracion_base()
        bonificacion = self.calcular_bonificacion()

        puntuacion_final = puntuacion_base + bonificacion

        if puntuacion_final > 99:
            puntuacion_final = 99
        elif puntuacion_final < 50:
            puntuacion_final = 50

        self.puntuacion_total = puntuacion_final
        super().save(*args, **kwargs)




class Equipo_usuario(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False)
    nombre = models.CharField(max_length=100,verbose_name="Nombre Equipo")
    fecha_creacion = models.DateField(auto_now_add=True)
    cartas = models.ManyToManyField(Carta_jugador)

    def __str__(self):
        return self.nombre

