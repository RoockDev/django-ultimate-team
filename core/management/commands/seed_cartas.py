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
            pais, _ = Pais.objects.get_or_create(nombre=fake.unique.country())  # la busca y sino la crea,
            # Si solo pusieramos create y se volviera a crear un nombre ya creado en otra ejecucion del script,
            # daría error. De esta manera lo busca primero y si no esta lo crea. Utizamos _ como papelera ya
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
        
        self.stdout.write(self.style.NOTICE('Iniciando creación de 150 cartas con lógica de stats realistas...'))

        # Creación de 150 cartas (usando .create() para activar el .save())

        posiciones_validas = [pos[0] for pos in Carta_jugador.POSICIONES]  # con pos[0] cogemos solamente la posición
        # de 3 letras (POR, DFC, MC, ...)

        # Definimos rangos de stats para hacer que los jugadores
        # sean más realistas según su posición.
        RANGO_BAJO = (10, 40)
        RANGO_MEDIO = (45, 75)
        RANGO_ALTO = (76, 95)

        cartas_creadas = []
        for _ in range(150):
            posicion_elegida = random.choice(posiciones_validas)

            if posicion_elegida == 'POR':
                # --- PORTERO ---
                ritmo = random.randint(*RANGO_BAJO)
                tiro = random.randint(*RANGO_BAJO)
                pase = random.randint(*RANGO_BAJO)
                regate = random.randint(*RANGO_BAJO)
                defensa = random.randint(*RANGO_BAJO)
                fisico = random.randint(*RANGO_MEDIO)
                salto = random.randint(*RANGO_ALTO)
                parada = random.randint(*RANGO_ALTO)
                saque = random.randint(*RANGO_ALTO)
                reflejos = random.randint(*RANGO_ALTO)
                velocidad = random.randint(*RANGO_MEDIO)
                posicionamiento = random.randint(*RANGO_ALTO)

            elif posicion_elegida in ['DFC', 'LD', 'LI']:
                # --- DEFENSA ---
                ritmo = random.randint(*RANGO_MEDIO)
                tiro = random.randint(*RANGO_BAJO)
                pase = random.randint(*RANGO_MEDIO)
                regate = random.randint(*RANGO_BAJO)
                defensa = random.randint(*RANGO_ALTO)
                fisico = random.randint(*RANGO_ALTO)
                salto = random.randint(*RANGO_MEDIO)
                parada = random.randint(*RANGO_BAJO)
                saque = random.randint(*RANGO_BAJO)
                reflejos = random.randint(*RANGO_BAJO)
                velocidad = random.randint(*RANGO_MEDIO)
                posicionamiento = random.randint(*RANGO_MEDIO)

            elif posicion_elegida in ['MC', 'MCD', 'MCO']:
                # --- CENTROCAMPISTA ---
                ritmo = random.randint(*RANGO_MEDIO)
                tiro = random.randint(*RANGO_MEDIO)
                pase = random.randint(*RANGO_ALTO)
                regate = random.randint(*RANGO_ALTO)
                defensa = random.randint(*RANGO_MEDIO)
                fisico = random.randint(*RANGO_MEDIO)
                salto = random.randint(*RANGO_BAJO)
                parada = random.randint(*RANGO_BAJO)
                saque = random.randint(*RANGO_BAJO)
                reflejos = random.randint(*RANGO_BAJO)
                velocidad = random.randint(*RANGO_MEDIO)
                posicionamiento = random.randint(*RANGO_MEDIO)

            else:
                # --- DELANTERO ---
                ritmo = random.randint(*RANGO_ALTO)
                tiro = random.randint(*RANGO_ALTO)
                pase = random.randint(*RANGO_MEDIO)
                regate = random.randint(*RANGO_ALTO)
                defensa = random.randint(*RANGO_BAJO)
                fisico = random.randint(*RANGO_MEDIO)
                salto = random.randint(*RANGO_MEDIO)
                parada = random.randint(*RANGO_BAJO)
                saque = random.randint(*RANGO_BAJO)
                reflejos = random.randint(*RANGO_BAJO)
                velocidad = random.randint(*RANGO_MEDIO)
                posicionamiento = random.randint(*RANGO_MEDIO)


            # 3. Creamos la carta con las stats generadas
            carta = Carta_jugador.objects.create(
                nombre=fake.first_name() + " " + fake.last_name(),
                pais=random.choice(paises),
                posicion=posicion_elegida,  # Usamos la posición ya elegida

                # Stats de Campo
                ritmo=ritmo,
                tiro=tiro,
                pase=pase,
                regate=regate,
                defensa=defensa,
                fisico=fisico,

                # Stats de Portero
                salto=salto,
                parada=parada,
                saque=saque,
                reflejos=reflejos,
                velocidad=velocidad,
                posicionamiento=posicionamiento,

                # Relaciones
                liga=random.choice(ligas),
                club=random.choice(clubes),

                # Requisitos del Req5
                activo=True,
            )
            cartas_creadas.append(carta)

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se han creado {len(cartas_creadas)} cartas.'))
        self.stdout.write(self.style.NOTICE(
            'Cada carta ha calculado su "puntuacion_total" automáticamente con stats realistas.'))