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

