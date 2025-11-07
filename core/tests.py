from django.test import TestCase


from .models import *

class PruebasModeloEquipo(TestCase):

    def test_validar_plantilla_falla_con_mas_de_25_cartas(self):

        usuario_prueba = Usuario.objects.create(
            username='testuser',
            email='test@test.com',
            password='123'
        )
        equipo_prueba = Equipo_usuario.objects.create(
            usuario=usuario_prueba,
            nombre="Equipo de Test"
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


        es_valido, mensaje = equipo_prueba.validar_plantilla()


        self.assertEqual(
            mensaje,
            "El equipo tiene 26 jugadores activos, debe tener entre 23 y 25"
        )

    def test_validar_plantilla_falla_con_menos_de_23_cartas(self):
        usuario_prueba = Usuario.objects.create(
            username='testuser2',
            email='test2@test.com',
            password='123'
        )
        equipo_prueba = Equipo_usuario.objects.create(
            usuario=usuario_prueba,
            nombre="Equipo de Test2"
        )

        pais_prueba = Pais.objects.create(nombre="País de Prueba2")
        liga_prueba = Liga.objects.create(nombre="Liga de Prueba2")
        club_prueba = Club.objects.create(
            nombre="Club de Prueba2",
            pais=pais_prueba,
            liga=liga_prueba
        )

        cartas_de_prueba = []
        for i in range(22):
            carta = Carta_jugador.objects.create(
                nombre=f"Jugador de Prueba {i + 1}",
                pais=pais_prueba,
                liga=liga_prueba,
                club=club_prueba,
                posicion='DC'
            )
            cartas_de_prueba.append(carta)




        equipo_prueba.cartas.set(cartas_de_prueba)


        es_valido, mensaje = equipo_prueba.validar_plantilla()


        self.assertEqual(
            mensaje,
            "El equipo tiene 22 jugadores activos, debe tener entre 23 y 25"
        )





    def test_validar_plantilla_falla_por_limite_porteros(self):

            usuario_prueba = Usuario.objects.create(
                username='testuser_porteros',
                email='test_por@test.com',
                password='123'
            )
            equipo_prueba = Equipo_usuario.objects.create(
                usuario=usuario_prueba,
                nombre="Equipo Test Porteros"
            )
            pais_prueba = Pais.objects.create(nombre="País de Prueba POR")
            liga_prueba = Liga.objects.create(nombre="Liga de Prueba POR")
            club_prueba = Club.objects.create(
                nombre="Club de Prueba POR",
                pais=pais_prueba,
                liga=liga_prueba
            )


            cartas_de_prueba = []


            for i in range(4):
                carta = Carta_jugador.objects.create(
                    nombre=f"Portero de Prueba {i + 1}",
                    pais=pais_prueba,
                    liga=liga_prueba,
                    club=club_prueba,
                    posicion='POR'
                )
                cartas_de_prueba.append(carta)


            for i in range(21):
                carta = Carta_jugador.objects.create(
                    nombre=f"Delantero de Prueba {i + 1}",
                    pais=pais_prueba,
                    liga=liga_prueba,
                    club=club_prueba,
                    posicion='DC'
                )
                cartas_de_prueba.append(carta)


            equipo_prueba.cartas.set(cartas_de_prueba)



            es_valido, mensaje = equipo_prueba.validar_plantilla()



            self.assertFalse(es_valido, "La validación debería fallar por 4 porteros, pero devolvió True.")


            self.assertEqual(
                mensaje,
                "El equipo tiene 4 porteros. Debe tener entre 2 y 3."
            )

    def test_validar_plantilla_equipo_valido_completo(self):

                usuario_prueba = Usuario.objects.create(
                    username='testuser_valido',
                    email='test_valido@test.com',
                    password='123'
                )
                equipo_prueba = Equipo_usuario.objects.create(
                    usuario=usuario_prueba,
                    nombre="Equipo Válido"
                )
                pais_prueba = Pais.objects.create(nombre="País Válido")
                liga_prueba = Liga.objects.create(nombre="Liga Válida")
                club_prueba = Club.objects.create(
                    nombre="Club Válido",
                    pais=pais_prueba,
                    liga=liga_prueba
                )

                cartas_de_prueba = []

                for i in range(3):
                    carta = Carta_jugador.objects.create(
                        nombre=f"Portero Válido {i + 1}",
                        pais=pais_prueba, liga=liga_prueba, club=club_prueba,
                        posicion='POR'
                    )
                    cartas_de_prueba.append(carta)

                for i in range(10):
                    carta = Carta_jugador.objects.create(
                        nombre=f"Defensa Válido {i + 1}",
                        pais=pais_prueba, liga=liga_prueba, club=club_prueba,
                        posicion='DFC'
                    )
                    cartas_de_prueba.append(carta)

                for i in range(6):
                    carta = Carta_jugador.objects.create(
                        nombre=f"Centro Válido {i + 1}",
                        pais=pais_prueba, liga=liga_prueba, club=club_prueba,
                        posicion='MC'
                    )
                    cartas_de_prueba.append(carta)

                for i in range(6):
                    carta = Carta_jugador.objects.create(
                        nombre=f"Delantero Válido {i + 1}",
                        pais=pais_prueba, liga=liga_prueba, club=club_prueba,
                        posicion='DC'
                    )
                    cartas_de_prueba.append(carta)

                equipo_prueba.cartas.set(cartas_de_prueba)

                es_valido, mensaje = equipo_prueba.validar_plantilla()

                self.assertTrue(es_valido, f"La validación debería pasar (True), pero falló y devolvió: {mensaje}")

                self.assertEqual(
                    mensaje,
                    "Plantilla validada"
                )
