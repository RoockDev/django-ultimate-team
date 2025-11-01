from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Usuario
from django.contrib.auth.hashers import make_password
import random

fake = Faker('es_ES')


class Command(BaseCommand):
    help = 'Inserta 30 usuarios de prueba en la base de datos usando bulk_create'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando script de carga masiva de usuarios...'))

        # Comprobación de seguridad (Abortar si hay datos)
        if Usuario.objects.exists():
            self.stdout.write(self.style.ERROR('Error: Ya existen usuarios en la base de datos.'))
            self.stdout.write(
                self.style.WARNING('Por favor, vacía la tabla de usuarios si quieres volver a ejecutar este comando.'))
            return  # Detiene la ejecución

        self.stdout.write(self.style.SUCCESS('La base de datos está vacía de usuarios, preparando 30 usuarios...'))

        usuarios_para_crear = []

        for i in range(30):
            nombre = fake.first_name()
            apellidos = fake.last_name()
            username = fake.unique.user_name()
            email = fake.unique.email()
            fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=70)

            password_plana = '1234'
            password_hasheada = make_password(password_plana)

            # Creamos el objeto Usuario (en memoria, no en BBDD)
            usuario = Usuario(
                username=username,
                email=email,
                password=password_hasheada,
                nombre=nombre,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento
            )
            usuarios_para_crear.append(usuario)

        # Creación en Base de Datos (1 sola consulta gracias al bulk_create). Es mucho más eficiente
        try:
            Usuario.objects.bulk_create(usuarios_para_crear)
            self.stdout.write(
                self.style.SUCCESS(f'¡Éxito! Se han creado {len(usuarios_para_crear)} usuarios en una sola operación.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al usar bulk_create: {e}'))