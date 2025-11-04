import json
from wsgiref.util import request_uri

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from .models import *

#GET obtener todas las cartas
def listar_cartas(request):
    #    obtenemos todos los objetos de carta completos.
    #    .select_related() es una optimización clave: le dice a Django
    #    que también coja los datos de club, pais y liga en la misma
    #    consulta. Esto evita muchas consultas extra a la BBDD.
    todas_las_cartas = Carta_jugador.objects.all().select_related('club','liga','pais')
    cartas_para_json = []

    for carta in todas_las_cartas:
        datos_carta = {
            'id':carta.id,
            'nombre':carta.nombre,
            'posicion':carta.posicion,
            'puntuacion_total':carta.puntuacion_total,
            'club':carta.club.nombre,
            'liga':carta.liga.nombre,
            'pais':carta.pais.nombre,
            'activo':carta.activo
        }

        if carta.posicion == 'POR':
            datos_carta.update({
                'salto':carta.salto,
                'parada':carta.parada,
                'saque':carta.saque,
                'reflejos':carta.reflejos,
                'velocidad':carta.velocidad,
                'posicionamiento':carta.posicionamiento
            })
        else:
            datos_carta.update({
                'ritmo':carta.ritmo,
                'tiro':carta.tiro,
                'pase':carta.pase,
                'regate':carta.regate,
                'defensa':carta.defensa,
                'fisico':carta.fisico
            })
        cartas_para_json.append(datos_carta)

        if cartas_para_json:
            return JsonResponse(cartas_para_json,safe=False)
        else:
            return JsonResponse({'mensaje': 'No se encontraton cartas en la base de datos'})

#GET obtener una carta específica
def obtener_carta_id(request, carta_id):
    try:
        carta = Carta_jugador.objects.select_related('club', 'liga', 'pais').get(pk=carta_id)

        datos_carta = {
            'id': carta.id,
            'nombre': carta.nombre,
            'posicion': carta.posicion,
            'puntuacion_total': carta.puntuacion_total,
            'club': carta.club.nombre,
            'pais': carta.pais.nombre,
            'liga': carta.liga.nombre,
            'activo': carta.activo
        }
        if carta.posicion == 'POR':
            datos_carta.update({
                'salto':carta.salto,
                'parada':carta.parada,
                'saque':carta.saque,
                'reflejos':carta.reflejos,
                'velocidad':carta.velocidad,
                'posicionamiento':carta.posicionamiento
            })
        else:
          datos_carta.update({
              'ritmo': carta.ritmo,
              'tiro':carta.tiro,
              'pase':carta.pase,
              'regate':carta.regate,
              'defensa':carta.regate,
              'fisico':carta.fisico
          })

        return JsonResponse(datos_carta)
    except Carta_jugador.DoesNotExist:
        return  JsonResponse({'mensaje': 'La carta no existe'},status=404)






#POST crear una carta
@csrf_exempt
def crear_carta(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            club = Club.objects.get(pk=datos['club_id'])
            pais = Pais.objects.get(pk=datos['pais_id'])
            liga = Liga.objects.get(pk=datos['liga_id'])

            nueva_carta = Carta_jugador.objects.create(
                nombre = datos['nombre'],
                posicion = datos['posicion'],
                #Atributos de campo
                ritmo = datos.get('ritmo',30),
                tiro = datos.get('tiro',30),
                pase = datos.get('pase',30),
                regate = datos.get('regate',30),
                defensa = datos.get('defensa',30),
                fisico = datos.get('fisico',30),


                #Atributos portero
                salto = datos.get('salto',30),
                parada = datos.get('parada',30),
                saque = datos.get('saque',30),
                reflejos = datos.get('reflejos',30),
                velocidad = datos.get('velocidad',30),
                posicionamiento = datos.get('posicionamiento',30),

                club = club,
                pais = pais,
                liga = liga
            )

            return JsonResponse({"mensaje": "Carta creada con exito", "id": nueva_carta.id},status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)},status=400)

    return JsonResponse({"error": "Este endpoint solo soporta peticiones POST"},status=405)


#PUT updatear carta
@csrf_exempt
def actualizar_carta(request, carta_id):

    if request.method == 'PUT':
        try:

            carta = Carta_jugador.objects.get(pk=carta_id)


            datos = json.loads(request.body)


            club = Club.objects.get(pk=datos['club_id'])
            liga = Liga.objects.get(pk=datos['liga_id'])
            pais = Pais.objects.get(pk=datos['pais_id'])

            carta.nombre = datos.get('nombre', carta.nombre)
            carta.posicion = datos.get('posicion', carta.posicion)

            # atributos de campo
            carta.ritmo = datos.get('ritmo', 30)
            carta.tiro = datos.get('tiro', 30)
            carta.pase = datos.get('pase', 30)
            carta.regate = datos.get('regate', 30)
            carta.defensa = datos.get('defensa', 30)
            carta.fisico = datos.get('fisico', 30)

            # atributos de portero
            carta.salto = datos.get('salto', 30)
            carta.parada = datos.get('parada', 30)
            carta.saque = datos.get('saque', 30)
            carta.reflejos = datos.get('reflejos', 30)
            carta.velocidad = datos.get('velocidad', 30)
            carta.posicionamiento = datos.get('posicionamiento', 30)


            carta.club = club
            carta.pais = pais
            carta.liga = liga

            carta.save()

            return JsonResponse({"mensaje": "Carta actualizada con exito"})

        except Carta_jugador.DoesNotExist:
            return JsonResponse({'mensaje': 'La carta no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Este endpoint no soporta peticiones PUT'}, status=405)


# PATCH Updatear carta campos específicos
@csrf_exempt
def actualizar_campos_especificos_carta(request, carta_id):
    if request.method == 'PATCH':
        try:
            carta = Carta_jugador.objects.get(pk=carta_id)
            datos = json.loads(request.body)

            carta.nombre = datos.get('nombre', carta.nombre)
            carta.posicion = datos.get('posicion', carta.posicion)

            if carta.posicion == 'POR':
                carta.salto = datos.get('salto',carta.salto)
                carta.parada = datos.get('parada',carta.parada)
                carta.saque = datos.get('saque',carta.saque)
                carta.reflejos = datos.get('reflejos',carta.reflejos)
                carta.posicionamiento = datos.get('posicionamiento',carta.posicionamiento)
            else:

              carta.ritmo = datos.get('ritmo', carta.ritmo)
              carta.tiro = datos.get('tiro', carta.tiro)
              carta.pase = datos.get('pase', carta.pase)
              carta.regate = datos.get('regate', carta.regate)
              carta.defensa = datos.get('defensa', carta.defensa)
              carta.fisico = datos.get('fisico', carta.fisico)

            if 'club_id' in datos:
                carta.club = Club.objects.get(pk=datos['club_id'])
            if 'pais_id' in datos:
                carta.pais = Pais.objects.get(pk=datos['pais_id'])
            if 'liga_id' in datos:
                carta.liga = Liga.objects.get(pk=datos['liga_id'])

            carta.save()

            return JsonResponse({'mensaje': 'Carta actualizada con exito'})
        except Carta_jugador.DoesNotExist:
            return JsonResponse({"mensaje": "La carta no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Este endpoint solo soporta peticiones PATCH'})

# DELETE borrado lógico de carta
@csrf_exempt
def borrar_carta(request, carta_id):
    if request.method == 'DELETE':
        try:
            carta = Carta_jugador.objects.get(pk=carta_id)
            carta.activo = False
            carta.save()
            return JsonResponse({'mensaje': 'Carta desactivada con exito'})
        except Carta_jugador.DoesNotExist:
            return JsonResponse({'mensaje': 'La carta no existe'},status=404)
        except Exception as e:
            return JsonResponse({'error': str(3)},status=400)

    return JsonResponse({'error': 'Este endpoint solo soporta peticiones DELETE'})

def listar_usuarios(request):
    usuarios = list(Usuario.objects.values(
        'id',
        'username',
        'email',
        'nombre',
        'apellidos',
        'fecha_nacimiento'
    ))

    if usuarios:
        return JsonResponse(usuarios, safe=False)
    else:
        return JsonResponse({'mensaje': 'No se encontraron usuarios'})


def obtener_usuario_id(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
        datos = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'nombre': usuario.nombre,
            'apellidos': usuario.apellidos,
            'fecha_nacimiento': usuario.fecha_nacimiento,
        }
        return JsonResponse(datos)
    except Usuario.DoesNotExist:
        return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)



@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            if 'password' not in datos or not datos['password']:
                return JsonResponse({"error": "La contraseña es obligatoria"}, status=400)

            hashed_password = make_password(datos['password'])

            nuevo_usuario = Usuario.objects.create(
                username=datos['username'],
                email=datos['email'],
                password=hashed_password,
                nombre=datos.get('nombre', ''),
                apellidos=datos.get('apellidos', ''),
                fecha_nacimiento=datos.get('fecha_nacimiento', None)
            )

            return JsonResponse({"mensaje": "Usuario creado con éxito", "id": nuevo_usuario.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Este endpoint solo soporta peticiones POST"}, status=405)

@csrf_exempt
def actualizar_usuario(request, usuario_id):
    if request.method == 'PUT':
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            datos = json.loads(request.body)

            usuario.username = datos['username']
            usuario.email = datos['email']
            usuario.nombre = datos.get('nombre', usuario.nombre)
            usuario.apellidos = datos.get('apellidos', usuario.apellidos)
            usuario.fecha_nacimiento = datos.get('fecha_nacimiento', usuario.fecha_nacimiento)

            if 'password' in datos and datos['password']:
                usuario.password = make_password(datos['password'])

            usuario.save()

            return JsonResponse({"mensaje": "Usuario actualizado con éxito"})
        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Este endpoint no soporta peticiones PUT'}, status=405)

@csrf_exempt
def actualizar_campos_especificos_usuario(request, usuario_id):
    if request.method == 'PATCH':
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            datos = json.loads(request.body)

            usuario.username = datos.get('username', usuario.username)
            usuario.email = datos.get('email', usuario.email)
            usuario.nombre = datos.get('nombre', usuario.nombre)
            usuario.apellidos = datos.get('apellidos', usuario.apellidos)
            usuario.fecha_nacimiento = datos.get('fecha_nacimiento', usuario.fecha_nacimiento)

            if 'password' in datos and datos['password']:
                usuario.password = make_password(datos['password'])

            usuario.save()

            return JsonResponse({'mensaje': 'Usuario actualizado con éxito'})
        except Usuario.DoesNotExist:
            return JsonResponse({"mensaje": "El usuario no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Este endpoint solo soporta peticiones PATCH'}, status=405)

@csrf_exempt
def borrar_usuario(request, usuario_id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(pk=usuario_id)

            usuario.delete()

            return JsonResponse({'mensaje': 'Usuario eliminado (físicamente) con éxito'})
        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Este endpoint solo soporta peticiones DELETE'}, status=405)


# Asignación de equipo a usuario
@csrf_exempt
def asignar_equipo_a_usuario(request, usuario_id):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(pk=usuario_id)

            equipo_existente = Equipo_usuario.objects.filter(usuario=usuario)

            if equipo_existente.exists():
                return JsonResponse({'mensaje': 'El usuario ya tiene un equipo. Debe eliminarlo primero'},status=400)
            datos = json.loads(request.body)
            nombre_equipo = datos.get('nombre')

            if not nombre_equipo:
                return JsonResponse({'error': 'El nombre del equipo es obligatorio en el body'},status=400)

            nuevo_equipo = Equipo_usuario.objects.create(
                usuario = usuario,
                nombre = nombre_equipo
            )

            return JsonResponse({
                'mensaje': 'Equipo creado y asignado con éxito',
                'equipo_id': nuevo_equipo.id,
                'nombre_equipo': nuevo_equipo.nombre,
                'usuario_id': usuario.id
            },status=201)


        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje':'El usuario no existe'},status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)
    else:
        return JsonResponse({'error': 'Este endpoint solo soporta peticiones POST'},status=405)

# Eliminacion de equipo a un usuario
@csrf_exempt
def eliminar_equipo_de_usuario(request, usuario_id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(pk=usuario_id)

            equipo = Equipo_usuario.objects.filter(usuario=usuario)
            if not equipo.exists():
                return JsonResponse({'mensaje': 'no hay ningun equipo asignado a este usuario'})
            equipo.delete()
            return JsonResponse({'mensaje': 'Equipo eliminado con éxito'}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje': 'el usuario no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Este endpoint solo soporta peticiones DELETE'},status=405)


def consultar_equipo_usuario(request, usuario_id):

    if request.method == 'GET':
        try:
            # Buscamos el equipo que pertenezca a ese usuario_id.
            # Usamos select_related('usuario') para que también traiga
            # los datos del usuario en la misma consulta (más eficiente).
            equipo = Equipo_usuario.objects.select_related('usuario').get(usuario__id=usuario_id)

            # Obtenemos las cartas del equipo, pero solo las activas (Req6)
            cartas_activas = equipo.cartas.filter(activo=True).select_related('club', 'liga', 'pais')

            # Cconvertimos a JSON las cartas
            lista_cartas_json = []
            for carta in cartas_activas:
                datos_carta = {
                    'id': carta.id,
                    'nombre': carta.nombre,
                    'posicion': carta.posicion,
                    'puntuacion_total': carta.puntuacion_total,
                    'club': carta.club.nombre,
                    'liga': carta.liga.nombre,
                    'pais': carta.pais.nombre,
                }

                # Añadimos las stats correctas según la posición (solo mostramos las stats relevantes)
                if carta.posicion == 'POR':
                    datos_carta.update({
                        'salto': carta.salto,
                        'parada': carta.parada,
                        'saque': carta.saque,
                        'reflejos': carta.reflejos,
                        'velocidad': carta.velocidad,
                        'posicionamiento': carta.posicionamiento
                    })
                else:
                    datos_carta.update({
                        'ritmo': carta.ritmo,
                        'tiro': carta.tiro,
                        'pase': carta.pase,
                        'regate': carta.regate,
                        'defensa': carta.defensa,
                        'fisico': carta.fisico
                    })
                lista_cartas_json.append(datos_carta)

            # JSON de los datos del equipo
            respuesta_final = {
                'equipo_id': equipo.id,
                'nombre_equipo': equipo.nombre,
                'fecha_creacion': equipo.fecha_creacion,
                'propietario_username': equipo.usuario.username,
                'cartas_activas': lista_cartas_json,
                'total_cartas_activas': len(lista_cartas_json)
            }

            return JsonResponse(respuesta_final, safe=False)

        # Controlamos los errores
        except Equipo_usuario.DoesNotExist:
            # Comprobamos si es que el usuario no existe, o si solo no tiene equipo
            if not Usuario.objects.filter(pk=usuario_id).exists():
                return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)
            else:
                return JsonResponse({'mensaje': 'Este usuario no tiene ningún equipo asignado'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Este endpoint solo soporta peticiones GET'}, status=405)


@csrf_exempt
def anadir_carta_a_equipo(request, equipo_id):

    if request.method != 'POST':
        return JsonResponse({'error': 'Este endpoint solo soporta peticiones POST'}, status=405)

    try:
        # Buscamos el equipo al que queremos añadir la carta
        equipo = Equipo_usuario.objects.get(pk=equipo_id)

        datos = json.loads(request.body)
        carta_id_a_anadir = datos['carta_id']

        # Buscamos la carta que queremos añadir
        carta_a_anadir = Carta_jugador.objects.get(pk=carta_id_a_anadir)

        # Validaciones (Req7 y Req3.1)

        # Validación 1: Que la carta esté activa
        if not carta_a_anadir.activo:
            return JsonResponse({'error': 'La carta que intentas añadir no está activa'}, status=400)

        # Validación 2: Que la carta no esté ya en el equipo (Req7)
        if equipo.cartas.filter(pk=carta_a_anadir.pk).exists():
            return JsonResponse({'error': 'Esta carta ya existe en el equipo'}, status=400)

        # Validación 3: Límite total de cartas activas (Req7)
        cartas_activas_equipo = equipo.cartas.filter(activo=True)
        conteo_total_activas = cartas_activas_equipo.count()

        if conteo_total_activas >= 25:
            return JsonResponse({'error': 'El equipo ya tiene el máximo de 25 cartas activas'}, status=400)

        # Validación 4: Límites por posición (Req7 y Req3.1)

        # Definimos los límites por tipo de posición
        LIMITES_POSICION = {
            'Portero': 3,
            'Defensa': 10,
            'Centrocampista': 9,
            'Delantero': 6,
        }

        # Definimos un mapa para convertir la posición (ej. 'DFC') a un tipo (ej.
        # Agrupamos jugadores por una posicion más genérica
        POSICION_TIPO_MAP = {
            'POR': 'Portero',
            'DFC': 'Defensa', 'LTI': 'Defensa', 'LTD': 'Defensa',
            'MC': 'Centrocampista', 'MI': 'Centrocampista', 'MD': 'Centrocampista',
            'DC': 'Delantero', 'MP': 'Delantero',
        }

        # Obtenemos el tipo de la carta que queremos añadir
        tipo_carta_nueva = POSICION_TIPO_MAP.get(carta_a_anadir.posicion)

        if not tipo_carta_nueva:
            return JsonResponse({'error': f'La posición "{carta_a_anadir.posicion}" de la carta no es válida'},
                                status=400)

        # Contamos cuántas cartas de ese tipo ya hay en el equipo
        conteo_actual_tipo = 0
        if tipo_carta_nueva == 'Portero':
            conteo_actual_tipo = cartas_activas_equipo.filter(posicion='POR').count()
        elif tipo_carta_nueva == 'Defensa':
            conteo_actual_tipo = cartas_activas_equipo.filter(posicion__in=['DFC', 'LTI', 'LTD']).count()
        elif tipo_carta_nueva == 'Centrocampista':
            conteo_actual_tipo = cartas_activas_equipo.filter(posicion__in=['MC', 'MI', 'MD']).count()
        elif tipo_carta_nueva == 'Delantero':
            conteo_actual_tipo = cartas_activas_equipo.filter(posicion__in=['DC', 'MP']).count()

        # Comprobamos si hemos alcanzado el límite para ese tipo
        limite_para_este_tipo = LIMITES_POSICION[tipo_carta_nueva]
        if conteo_actual_tipo >= limite_para_este_tipo:
            return JsonResponse({
                'error': f'Límite de {tipo_carta_nueva}s alcanzado.',
                'mensaje': f'Ya tienes {conteo_actual_tipo} de {limite_para_este_tipo} (máximo) permitidos.'
            }, status=400)

        # Si todas las validaciones pasan, añadimos la carta a la relación
        # "Muchos a Muchos" (ManyToManyField)
        equipo.cartas.add(carta_a_anadir)

        return JsonResponse(
            {'mensaje': f'Carta "{carta_a_anadir.nombre}" añadida al equipo "{equipo.nombre}" con éxito'}, status=200)

    except Equipo_usuario.DoesNotExist:
        return JsonResponse({'error': 'El equipo especificado no existe'}, status=404)
    except Carta_jugador.DoesNotExist:
        return JsonResponse({'error': 'La carta especificada no existe'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido en el body de la petición. Asegúrate de enviar {"carta_id": X}'},
                            status=400)
    except Exception as e:
        return JsonResponse({'error': f'Ha ocurrido un error inesperado: {str(e)}'}, status=500)