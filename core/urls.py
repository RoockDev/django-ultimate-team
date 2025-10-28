from django.urls import path


from . import views

urlpatterns = [
   path('cartas/',views.listar_cartas),
   path('cartas/<int:carta_id>/',views.obtener_carta_id),
   path('cartas/crear/',views.crear_carta),
   path('cartas/actualizar/<int:carta_id>/',views.actualizar_carta),
   path('cartas/actualizar_especifica/<int:carta_id>/',views.actualizar_campos_especificos_carta),
   path('cartas/borrar/<int:carta_id>/',views.borrar_carta)

]