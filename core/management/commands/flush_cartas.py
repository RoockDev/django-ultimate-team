from django.core.management.base import BaseCommand
from core.models import Carta_jugador

class Command(BaseCommand):

    help = '¡Cuidado! Borra TODAS las cartas de la base de datos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando borrado masivo de cartas...'))

        # Obtenemos todas las cartas y las contamos
        cartas_a_borrar = Carta_jugador.objects.all()
        count = cartas_a_borrar.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('La base de datos de cartas ya estaba vacía. No se ha borrado nada.'))
            return

        self.stdout.write(self.style.WARNING(f'¡Borrando {count} cartas de la base de datos!'))

        # Ejecutamos el borrado
        cartas_a_borrar.delete()

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se han eliminado {count} cartas.'))