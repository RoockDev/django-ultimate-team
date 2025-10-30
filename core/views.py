import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

#GET obtener todas las cartas
def listar_cartas(request):
    cartas = list(Carta_jugador.objects.values(
        'id',
        'nombre',
        'pais__nombre',
        'posicion',
        'ritmo',
        'tiro',
        'pase',
        'regate',
        'defensa',
        'fisico',
        'liga__nombre',
        'club__nombre',
        'activo'
    ))

    if cartas:
        return  JsonResponse(cartas, safe=False)
    else:
        return  JsonResponse({'mensaje': 'No se encontraron cartas en la base de datos'})

#GET obtener una carta específica
def obtener_carta_id(request, carta_id):
    try:
        carta = Carta_jugador.objects.get(pk=carta_id)
        datos = {
            'id':carta.id,
            'nombre':carta.nombre,
            'posicion': carta.posicion,
            'ritmo': carta.ritmo,
            'tiro': carta.tiro,
            'pase':carta.pase,
            'regate':carta.regate,
            'defensa':carta.defensa,
            'fisico':carta.fisico,
            'club': carta.club.nombre,
            'liga': carta.liga.nombre,
            'pais': carta.pais.nombre,
            'activo': carta.activo
        }
        return JsonResponse(datos)
    except Carta_jugador.DoesNotExist:
        return JsonResponse({'mensaje': 'La carta no existe'},status=404)

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
                ritmo = datos['ritmo'],
                tiro = datos['tiro'],
                pase = datos['pase'],
                regate = datos['regate'],
                defensa = datos['defensa'],
                fisico = datos['fisico'],
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

           carta.nombre = datos['nombre']
           carta.posicion = datos['posicion']
           carta.ritmo = datos['ritmo']
           carta.tiro = datos['tiro']
           carta.pase = datos['pase']
           carta.regate = datos['regate']
           carta.defensa = datos['defensa']
           carta.fisico = datos['fisico']
           carta.club = club
           carta.pais = pais
           carta.liga = liga
           carta.save()

           return JsonResponse({"mensaje": "Carta actualizada con exito"})
       except Carta_jugador.DoesNotExist:
           return JsonResponse({'mensaje': 'La carta no existe'},status=404)
       except Exception as e:
           return JsonResponse({'error': str(e)},status=400)

   return JsonResponse({'error': 'Este endpoint no soporta peticiones PUT'},status=405)

# PATCH Updatear carta campos específicos
@csrf_exempt
def actualizar_campos_especificos_carta(request, carta_id):
    if request.method == 'PATCH':
        try:
            carta = Carta_jugador.objects.get(pk=carta_id)
            datos = json.loads(request.body)

            carta.nombre = datos.get('nombre', carta.nombre)
            carta.posicion = datos.get('posicion', carta.posicion)
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
