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
    # Atributos de campo
    ritmo = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Ritmo",default=30)
    tiro = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Tiro",default=30)
    pase = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Pase",default=30)
    regate = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Regate",default=30)
    defensa = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Defensa",default=30)
    fisico = models.IntegerField(validators=VALIDADORES_STATS,null=False,verbose_name="Físico",default=30)

    # Atributos de portero
    salto = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Salto",default=30)
    parada = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Parada",default=30)
    saque = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Saque",default=30)
    reflejos = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Reflejos",default=30)
    velocidad = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Velocidad Portero",default=30)
    posicionamiento = models.IntegerField(validators=VALIDADORES_STATS, verbose_name="Posicionamiento Portero",default=30)

    liga = models.ForeignKey(Liga,on_delete=models.CASCADE,null=False)
    club = models.ForeignKey(Club,on_delete=models.CASCADE,null=False)
    activo = models.BooleanField(default=True)
    puntuacion_total = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(99)],verbose_name="Puntuación General")



    def __str__(self):
        return self.nombre

    def calcular_valoracion_base(self):
        if self.posicion == 'POR':



                stats_relevantes = [self.salto,self.parada,self.saque,self.reflejos,self.velocidad,self.posicionamiento]

        else:
            stats_relevantes = [self.ritmo, self.tiro, self.pase, self.regate, self.defensa, self.fisico]

        if not stats_relevantes:
            return 0
        media_base = sum(stats_relevantes)/len(stats_relevantes)
        return round(media_base)

    def calcular_bonificacion(self):

        bonificacion = 0
        if self.posicion == 'POR':



            stats_totales = [self.salto, self.parada, self.saque, self.reflejos, self.velocidad,
                                self.posicionamiento]

        else:
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

    def validar_plantilla(self):
        cartas_activas = self.cartas.filter(activo=True)
        total_cartas_activas = self.cartas.filter(activo=True).count()

        if total_cartas_activas < 23 or total_cartas_activas > 25:
            return(False, f"El equipo tiene {total_cartas_activas} jugadores activos, debe tener entre 23 y 25")


        """
        porteros entre 2 y 3
        defensas entre 8 y 10
        centrocampistas entre 6 y 9
        delanteros entre 5 y 6
        """
        total_porteros = cartas_activas.filter(posicion = 'POR').count()
        total_defensas = cartas_activas.filter(posicion__in=['DFC','LTI','LTD']).count()
        total_centrocampistas = cartas_activas.filter(posicion__in=['MC','MI','MD']).count()
        total_delanteros = cartas_activas.filter(posicion__in=['DC','MP']).count()
        if not (2 <= total_porteros <=3):
            return (False, f"El equipo tiene {total_porteros} porteros. Debe tener entre 2 y 3.")

        elif not (8 <= total_defensas <= 10):
            return (False, f"El equipo tiene {total_defensas} defensas. Debe tener entre 8 y 10.")

        elif not (6 <= total_centrocampistas <= 9):
            return (False, f"El equipo tiene {total_centrocampistas} centrocampistas. Debe tener entre 6 y 9.")

        elif not (5 <= total_delanteros <= 6):
            return (False, f"El equipo tiene {total_delanteros} delanteros. Debe tener entre 5 y 6.")



        return (True, "Plantilla validada")










