import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from django.contrib.auth.hashers import make_password, check_password


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

        self.assertEqual(
            mensaje,
            "Plantilla validada"
        )


class PruebasModeloCarta(TestCase):

    def setUp(self):
        # esto lo creo porque esto lo voy a utilizar en los demas test
        self.pais_prueba = Pais.objects.create(nombre="País de Prueba Cartas")
        self.liga_prueba = Liga.objects.create(nombre="Liga de Prueba Cartas")
        self.club_prueba = Club.objects.create(
            nombre="Club de Prueba Cartas",
            pais=self.pais_prueba,
            liga=self.liga_prueba
        )

    def test_calculo_puntuacion_portero(self):
        """
        Prueba que .save() calcula la puntuacion_total
        usando las stats de portero
        """
        carta_portero = Carta_jugador.objects.create(
            nombre="Test Portero",
            pais=self.pais_prueba,
            liga=self.liga_prueba,
            club=self.club_prueba,
            posicion='POR',
            salto=81,
            parada=81,
            saque=81,
            reflejos=81,
            velocidad=81,
            posicionamiento=81
        )
        self.assertEqual(
            carta_portero.puntuacion_total,
            93,
            f"El cálculo para POR falló. Se esperaba 93, pero se obtuvo {carta_portero.puntuacion_total}"
        )

    def test_calculo_puntuacion_delantero(self):
        carta_delantero = Carta_jugador.objects.create(
            nombre="Test Delantero",
            pais=self.pais_prueba,
            liga=self.liga_prueba,
            club=self.club_prueba,
            posicion='DC',
            ritmo=81,
            tiro=81,
            pase=81,
            regate=81,
            defensa=81,
            fisico=81,
        )
        self.assertEqual(
            carta_delantero.puntuacion_total,
            93,
            f"El cálculo para Delantero falló. Se esperaba 93, pero se obtuvo {carta_delantero.puntuacion_total}"
        )

    def test_puntuacion_se_limita_a_99(self):
        carta_max = Carta_jugador.objects.create(
            nombre="Test Tope 99",
            pais=self.pais_prueba,
            liga=self.liga_prueba,
            club=self.club_prueba,
            posicion='DC',
            ritmo=99,
            tiro=99,
            pase=99,
            regate=99,
            defensa=99,
            fisico=99
        )
        self.assertEqual(
            carta_max.puntuacion_total,
            99,
            f"El límite de 99 falló. Se esperaba 99, pero se obtuvo {carta_max.puntuacion_total}"
        )

    def test_puntuacion_se_limita_a_50(self):
        carta_min = Carta_jugador.objects.create(
            nombre="Test  50",
            pais=self.pais_prueba,
            liga=self.liga_prueba,
            club=self.club_prueba,
            posicion='DC',
            ritmo=1,
            tiro=1,
            pase=1,
            regate=1,
            defensa=1,
            fisico=1
        )
        self.assertEqual(
            carta_min.puntuacion_total,
            50,
            f"El límite de 50 falló. Se esperaba 50, pero se obtuvo {carta_min.puntuacion_total}"
        )


class PruebasAPIUsuario(TestCase):

    def setUp(self):
        """
        Prepara los datos que necesitaremos para todas las pruebas
        del crud de Usuario.
        """
        # Creamos un usuario de prueba para poder probar

        self.usuario_existente = Usuario.objects.create(
            username='usuario_de_prueba',
            email='prueba@api.com',
            password='123',
            nombre='Test',
            apellidos='Api'
        )

    def test_listar_usuarios_ok(self):
        # uso el "Postman de django" (self.client) para llamar a la URL
        respuesta = self.client.get('/api/usuarios/')

        self.assertEqual(
            respuesta.status_code,
            200,
            f"La ruta /api/usuarios/ falló. Se esperaba 200 OK, se obtuvo {respuesta.status_code}"

        )

        # se comprueba que el json es correcto
        datos_json = respuesta.json()

        # se comprueba que la respuesta es una lista
        self.assertIsInstance(datos_json, list)

        # se comprueba que la lista tiene 1 elemento, que es el que se crea en setup
        self.assertEqual(len(datos_json), 1)
        # se comprueba que el username del usuario esta en la bbdd
        self.assertEqual(datos_json[0]['username'], 'usuario_de_prueba')

    def test_obtener_usuario_id_ok(self):
        """
        Prueba que la ruta GET /usuarios/<id>/ funciona
        y devuelve un 200 OK con los datos del usuario correcto
        """
        url = f'/api/usuarios/{self.usuario_existente.id}/'
        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 200)

        datos_json = respuesta.json()

        self.assertEqual(datos_json['username'], 'usuario_de_prueba')

        self.assertEqual(datos_json['id'], self.usuario_existente.id)

    def test_obtener_usuario_id_404_not_found(self):
        """
        Prueba que la ruta GET /usuarios/<id>/ devuelve un 404
        si el id del usuario no existe
        """
        url = '/api/usuarios/9999/'

        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 404)

        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'El usuario no existe')

    def test_crear_usuario_ok(self):
        """
        Prueba que la ruta POST /usuarios/crear/ crea un nuevo
        usuario y devuelve un 201 Created.
        """
        nuevos_datos_usuario = {
            "username": "usuario_creado_test",
            "email": "creado@test.com",
            "password": "pass_segura_123"
        }

        # se cuentan los usuarios que hay para despues ver que cuando se crea uno nuevo hay + 1
        conteo_antes = Usuario.objects.count()

        #    data=nuevos_datos_usuario: lo que se quiere enviar
        #     content_type='application/json':
        #      le dice a Django que estamos enviando un json
        #      para que sepa como leer el body
        respuesta = self.client.post(
            '/api/usuarios/crear/',
            data=nuevos_datos_usuario,
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 201)

        #  se comprueba que el usuario se ha creado
        conteo_despues = Usuario.objects.count()
        # ahora tiene que haber uno
        self.assertEqual(conteo_despues, conteo_antes + 1)

        # se comprueba que el usuario existe en la BBDD
        usuario_nuevo = Usuario.objects.get(username="usuario_creado_test")
        self.assertEqual(usuario_nuevo.email, "creado@test.com")

        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'Usuario creado con éxito')

    def test_actualizar_usuario_ok(self):
        """
        Prueba que la ruta PUT /usuarios/actualizar/<id>/
        actualiza un usuario existente y devuelve 200 OK.
        """
        url = f'/api/usuarios/actualizar/{self.usuario_existente.id}/'

        datos_actualizados = {
            "username": "usuario_actualizado",
            "email": "actualizado@test.com",
            "nombre": "Nombre Cambiado",
            "apellidos": "Apellido Cambiado",
            "fecha_nacimiento": "2000-01-01",
            "password": "456"
        }

        respuesta = self.client.put(
            url,
            data=datos_actualizados,
            content_type='application/json'
        )

        self.assertEqual(respuesta.status_code, 200)

        #  refresca con los nuevos datos de la BBDD.
        self.usuario_existente.refresh_from_db()

        self.assertEqual(self.usuario_existente.username, "usuario_actualizado")
        self.assertEqual(self.usuario_existente.nombre, "Nombre Cambiado")

        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'Usuario actualizado con éxito')

    def test_borrar_usuario_ok(self):
        """
        Prueba que la ruta DELETE /usuarios/borrar/<id>/
        elimina un usuario existente y devuelve 200 OK.
        """
        url = f'/api/usuarios/borrar/{self.usuario_existente.id}/'
        conteo_antes = Usuario.objects.count()
        respuesta = self.client.delete(url)
        self.assertEqual(respuesta.status_code, 200)
        conteo_despues = Usuario.objects.count()
        # ahora debe ser 1 menos que antes
        self.assertEqual(conteo_despues, conteo_antes - 1)

        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'Usuario eliminado (físicamente) con éxito')


class PruebasAPICarta(TestCase):
    def setUp(self):
        """
        Prepara los datos que necesitaremos para todos los test
        del crud de Cartas.
        """
        pais_carta = Pais.objects.create(nombre="País Carta Test")
        liga_carta = Liga.objects.create(nombre="Liga Carta Test")
        self.club_carta = Club.objects.create(
            nombre="Club Carta Test",
            pais=pais_carta,
            liga=liga_carta
        )

        self.carta_existente = Carta_jugador.objects.create(
            nombre="Carta de Prueba API",
            pais=pais_carta,
            liga=liga_carta,
            club=self.club_carta,
            posicion='DC',
            ritmo=90, tiro=90, pase=90, regate=90, defensa=90, fisico=90
        )

    def test_listar_cartas_ok(self):
        """
        Prueba que la ruta GET /cartas/ funciona
        y devuelve la carta que creamos arriba
        """
        respuesta = self.client.get('/api/cartas/')

        self.assertEqual(respuesta.status_code, 200)
        datos_json = respuesta.json()
        self.assertIsInstance(datos_json, list)

        # se comprueba que tiene 1 carta
        self.assertEqual(len(datos_json), 1)

    def test_obtener_carta_id_ok(self):
        """
        Prueba que la ruta GET /cartas/<id>/ funciona
        y devuelve un 200 OK con los datos de la carta correcta.
        """
        url = f'/api/cartas/{self.carta_existente.id}/'

        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 200)

        datos_json = respuesta.json()

        # se comprueba que el id es el correcto
        self.assertEqual(datos_json['id'], self.carta_existente.id)

    def test_obtener_carta_id_404_not_found(self):
        """
        Prueba que la ruta GET /cartas/<id>/ devuelve un 404
        si el id de la carta no existe.
        """
        url = '/api/cartas/9999/'

        respuesta = self.client.get(url)

        self.assertEqual(respuesta.status_code, 404)
        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'La carta no existe')

    def test_borrar_carta_logico_ok(self):
        """
        Prueba que la ruta DELETE /cartas/borrar/<id>/
        se desactiva el borrado lógico de una carta y devuelve 200 OK.
        """
        url = f'/api/cartas/borrar/{self.carta_existente.id}/'

        conteo_antes = Carta_jugador.objects.count()

        #    se verifca que la carta este activa antes del test
        self.assertTrue(self.carta_existente.activo)

        respuesta = self.client.delete(url)
        self.assertEqual(respuesta.status_code, 200)

        # se comprueba que la carta no se ha borrado de verdad
        conteo_despues = Carta_jugador.objects.count()
        self.assertEqual(conteo_despues, conteo_antes)

        # se comprueba que la carta ahora este desactivada

        # se refresca el objeto desde la BBDD
        # para ver el cambio que hizo la vista en el campo activo
        self.carta_existente.refresh_from_db()

        # se comprueba que activo es false
        self.assertFalse(self.carta_existente.activo)
        datos_json = respuesta.json()
        self.assertEqual(datos_json['mensaje'], 'Carta desactivada con exito')


class PruebasAPIEquipo(TestCase):

    def setUp(self):
        """
        Prepara los datos que necesitaremos para todas las pruebas
        de las APIs de Equipo (asignar, eliminar, consultar, añadir).
        """
        self.client = Client()

        self.pais = Pais.objects.create(nombre="España")
        self.liga = Liga.objects.create(nombre="La Liga")
        self.club = Club.objects.create(nombre="Equipo Ficticio", pais=self.pais, liga=self.liga)

        # Creamos dos usuarios de prueba
        pw = make_password('1234')
        self.usuario1 = Usuario.objects.create(username="usuario1", email="u1@test.com", password=pw)
        self.usuario2 = Usuario.objects.create(username="usuario2", email="u2@test.com", password=pw)

        # Creamos un equipo para el usuario 1
        self.equipo1 = Equipo_usuario.objects.create(usuario=self.usuario1, nombre="Mi Equipo 1")

        # Creamos 10 porteros
        self.porteros = []
        for i in range(10):
            self.porteros.append(
                Carta_jugador.objects.create(
                    nombre=f"Portero {i}", posicion="POR", puntuacion_total=85,
                    pais=self.pais, liga=self.liga, club=self.club, activo=True
                )
            )

        # Creamos 10 defensas
        lista_defensas = []
        for i in range(10):
            lista_defensas.append(
                Carta_jugador.objects.create(
                    nombre=f"Defensa {i}", posicion="DFC", puntuacion_total=85,
                    pais=self.pais, liga=self.liga, club=self.club, activo=True
                )
            )

        # Creamos 10 centrocampistas
        lista_centros = []
        for i in range(10):
            lista_centros.append(
                Carta_jugador.objects.create(
                    nombre=f"Centro {i}", posicion="MC", puntuacion_total=85,
                    pais=self.pais, liga=self.liga, club=self.club, activo=True
                )
            )

        # Creamos 10 delanteros
        self.delantero_para_anadir = Carta_jugador.objects.create(
            nombre="Delantero para añadir", posicion="DC", puntuacion_total=90,
            pais=self.pais, liga=self.liga, club=self.club, activo=True
        )
        lista_delanteros = [self.delantero_para_anadir]
        for i in range(9):
            lista_delanteros.append(
                Carta_jugador.objects.create(
                    nombre=f"Delantero {i}", posicion="DC", puntuacion_total=85,
                    pais=self.pais, liga=self.liga, club=self.club, activo=True
                )
            )

        # Creamos una lista de 25 cartas válidas para el test de límite total
        self.cartas_para_llenar = (
                self.porteros[:3] + lista_defensas[:10] + lista_centros[:6] + lista_delanteros[:6]
        )

        # Creamos una carta inactiva para el test de filtro
        self.carta_inactiva = Carta_jugador.objects.create(
            nombre="Jugador Inactivo", posicion="MC", puntuacion_total=80,
            pais=self.pais, liga=self.liga, club=self.club, activo=False
        )

        # Definimos las URLs
        self.url_asignar = f'/api/equipo/asignar/{self.usuario2.id}/'
        self.url_asignar_fail_404 = f'/api/equipo/asignar/999/'
        self.url_asignar_fail_400 = f'/api/equipo/asignar/{self.usuario1.id}/'
        self.url_eliminar = f'/api/equipo/eliminar/{self.usuario1.id}/'
        self.url_eliminar_fail = f'/api/equipo/eliminar/{self.usuario2.id}/'
        self.url_consultar = f'/api/equipo/consultar/{self.usuario1.id}/'
        self.url_anadir = f'/api/equipos/{self.equipo1.id}/anadir_carta/'

    def test_asignar_equipo_201_creado(self):
        """
        Prueba que la ruta POST /equipo/asignar/<id>/
        crea un equipo con una plantilla aleatoria y devuelve 201.
        """
        datos_json = json.dumps({'nombre': 'Equipo Nuevo'})
        response = self.client.post(self.url_asignar, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Equipo_usuario.objects.count(), 2)
        self.assertIn('Equipo creado y rellenado', response.json()['mensaje'])

    def test_asignar_equipo_400_ya_tiene(self):
        """
        Prueba que POST /equipo/asignar/<id>/ devuelve 400
        si el usuario ya tiene un equipo asignado.
        """
        datos_json = json.dumps({'nombre': 'Equipo Repetido'})
        response = self.client.post(self.url_asignar_fail_400, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('ya tiene un equipo', response.json()['mensaje'])

    def test_asignar_equipo_404_no_existe(self):
        """
        Prueba que POST /equipo/asignar/<id>/ devuelve 404
        si el usuario no existe.
        """
        datos_json = json.dumps({'nombre': 'Equipo Fantasma'})
        response = self.client.post(self.url_asignar_fail_404, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn('usuario no existe', response.json()['mensaje'])


    def test_eliminar_equipo_200_ok(self):
        """
        Prueba que DELETE /equipo/eliminar/<id>/
        borra el equipo de un usuario existente.
        """
        response = self.client.delete(self.url_eliminar)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Equipo eliminado con éxito', response.json()['mensaje'])
        self.assertEqual(Equipo_usuario.objects.filter(usuario=self.usuario1).count(), 0)

    def test_eliminar_equipo_error_no_tiene(self):
        """
        Prueba que DELETE /equipo/eliminar/<id>/
        devuelve un mensaje correcto si el usuario no tiene equipo.
        """
        response = self.client.delete(self.url_eliminar_fail)

        self.assertEqual(response.status_code, 200)
        self.assertIn('no hay ningun equipo', response.json()['mensaje'])

    def test_consultar_equipo_200_ok(self):
        """
        Prueba que GET /equipo/consultar/<id>/
        devuelve los datos del equipo del usuario.
        """
        response = self.client.get(self.url_consultar)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nombre_equipo'], 'Mi Equipo 1')
        self.assertEqual(response.json()['propietario_username'], 'usuario1')

    def test_consultar_equipo_filtro_activo(self):
        """
        Prueba que GET /equipo/consultar/<id>/ (Req6)
        solo devuelve las cartas con activo=True.
        """
        self.equipo1.cartas.add(self.delantero_para_anadir)
        self.equipo1.cartas.add(self.carta_inactiva)

        response = self.client.get(self.url_consultar)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['cartas_activas']), 1)
        self.assertEqual(response.json()['total_cartas_activas'], 1)
        self.assertEqual(response.json()['cartas_activas'][0]['nombre'], 'Delantero para añadir')


    def test_anadir_carta_200_ok(self):
        """
        Prueba que POST /equipos/<id>/anadir_carta/ (Req7)
        añade una carta con éxito.
        """
        datos_json = json.dumps({'carta_id': self.delantero_para_anadir.id})
        response = self.client.post(self.url_anadir, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('añadida al equipo', response.json()['mensaje'])
        self.assertEqual(self.equipo1.cartas.count(), 1)

    def test_anadir_carta_400_duplicada(self):
        """
        Prueba que la vista (Req7)
        devuelve un error 400 si la carta ya está en el equipo.
        """
        self.equipo1.cartas.add(self.delantero_para_anadir)

        datos_json = json.dumps({'carta_id': self.delantero_para_anadir.id})
        response = self.client.post(self.url_anadir, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('carta ya existe', response.json()['error'])

    def test_anadir_carta_400_limite_posicion(self):
        """
        Prueba que la vista (Req7 / Req3.1)
        devuelve un error 400 si se supera el límite de posición.
        """
        self.equipo1.cartas.add(self.porteros[0], self.porteros[1], self.porteros[2])
        self.assertEqual(self.equipo1.cartas.filter(posicion='POR').count(), 3)

        datos_json = json.dumps({'carta_id': self.porteros[3].id})
        response = self.client.post(self.url_anadir, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Límite de Porteros alcanzado', response.json()['error'])

    def test_anadir_carta_400_limite_total(self):
        """
        Prueba que la vista (Req7)
        devuelve un error 400 si se supera el límite de 25 cartas.
        """
        self.equipo1.cartas.set(self.cartas_para_llenar)
        self.assertEqual(self.equipo1.cartas.filter(activo=True).count(), 25)

        # Usamos un portero que sabemos que no está en la lista de 25
        datos_json = json.dumps({'carta_id': self.porteros[3].id})
        response = self.client.post(self.url_anadir, data=datos_json, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('máximo de 25 cartas', response.json()['error'])