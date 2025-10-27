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