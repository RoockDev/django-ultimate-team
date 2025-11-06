from django.test import TestCase


from .models import *

class PruebasModeloEquipo(TestCase):
    def test_validar_plantilla_falla_con_mas_de_25_cartas(self):
        """
        Prueba que validar_plantilla() devuelve (False, ...) si un equipo
        tiene más de 25 cartas activas.
        """
        usuario_prueba = Usuario.objects.create(
            username = 'testuser',
            email='test@test.com',
            password = '123'
        )

        equipo_prueba = Equipo_usuario.objects.create(
            usuario = usuario_prueba,
            nombre = 'Equipo de test'
        )

        pais_prueba = Pais.objects.create(nombre="País de Prueba")
        liga_prueba = Liga.objects.create(nombre="Liga de Prueba")
        club_prueba = Club.objects.create(
            nombre="Club de Prueba",
            pais=pais_prueba,
            liga=liga_prueba
        )

        cartas_de_prueba = []
        for i in range(26):
            carta = Carta_jugador.objects.create(
                nombre=f"Jugador de Prueba {i + 1}",
                pais=pais_prueba,
                liga=liga_prueba,
                club=club_prueba,
                posicion='DC'
            )
            cartas_de_prueba.append(carta)
            equipo_prueba.cartas.set(cartas_de_prueba)
            es_valido,mensaje = equipo_prueba.validar_plantilla()


            self.assertEqual(
                mensaje,
                "El equipo tiene 26 jugadores activos, debe tener entre 23 y 25"
            )

