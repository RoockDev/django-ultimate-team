from django.shortcuts import render
from django.http import JsonResponse
from .models import *

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