import random
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Carta_jugador, Club, Liga, Pais

fake = Faker('es_ES')


class Command(BaseCommand):
    help = 'Inserta 150 cartas de prueba (con stats de campo y portero). Usa .create() para ejecutar el .save() personalizado.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando script de carga masiva de cartas...'))

        # Comprobación de seguridad (Abortar si hay datos)
        if Carta_jugador.objects.exists():
            self.stdout.write(self.style.ERROR('Error: Ya existen cartas en la base de datos.'))
            self.stdout.write(
                self.style.WARNING('Por favor, vacía la tabla de cartas si quieres volver a ejecutar este comando.'))
            return

        #  Creación de Países, Ligas y Clubes
        self.stdout.write(self.style.NOTICE('Creando Países, Ligas, Clubes...'))

        paises = []
        for _ in range(5):
            pais, _ = Pais.objects.get_or_create(nombre=fake.unique.country()) # la busca y sino la crea,
            # Si solo pusieramos create y se volviera a crear un nombre ya creado en otra ejecucion del script,
            #daría error. De esta manera lo busca primero y si no esta lo crea. Utizamos _ como papelera ya
            # que no nos interesa el booleano que nos da la función
            paises.append(pais)

        ligas = []
        for _ in range(3):
            liga, _ = Liga.objects.get_or_create(nombre=fake.unique.company() + " League")
            ligas.append(liga)

        clubes = []
        for _ in range(10):
            club, _ = Club.objects.get_or_create(
                nombre=fake.unique.company(),
                pais=random.choice(paises),
                liga=random.choice(ligas)
            )
            clubes.append(club)

        self.stdout.write(self.style.SUCCESS(
            f'Dependencias creadas: {len(paises)} Países, {len(ligas)} Ligas, {len(clubes)} Clubes.'))
        self.stdout.write(self.style.NOTICE('Iniciando creación de 150 cartas. Esto puede tardar unos segundos...'))

        # Creación de 150 cartas (usando .create() para activar el .save())

        posiciones_validas = [pos[0] for pos in Carta_jugador.POSICIONES] # con pos[0] cogemos solamente la posición
        # de 3 letras (POR, DFC, MC, ...)

        cartas_creadas = []
        for _ in range(150):
            carta = Carta_jugador.objects.create(
                nombre=fake.first_name() + " " + fake.last_name(),
                pais=random.choice(paises),
                posicion=random.choice(posiciones_validas),

                # Stats de Campo
                ritmo=random.randint(50, 99),
                tiro=random.randint(50, 99),
                pase=random.randint(50, 99),
                regate=random.randint(50, 99),
                defensa=random.randint(30, 99),
                fisico=random.randint(40, 99),

                # Stats de Portero
                salto=random.randint(50, 99),
                parada=random.randint(50, 99),
                saque=random.randint(50, 99),
                reflejos=random.randint(50, 99),
                velocidad=random.randint(50, 99),
                posicionamiento=random.randint(50, 99),

                # Relaciones
                liga=random.choice(ligas),
                club=random.choice(clubes),

                # Requisitos del Req5
                activo=True,

            )
            cartas_creadas.append(carta)

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se han creado {len(cartas_creadas)} cartas.'))
        self.stdout.write(self.style.NOTICE(
            'Cada carta ha calculado su "puntuacion_total" automáticamente gracias al método .save().'))