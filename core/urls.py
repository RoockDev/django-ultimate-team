from django.urls import path


from . import views

urlpatterns = [
   path('cartas/',views.listar_cartas),
   path('cartas/<int:carta_id>/',views.obtener_carta_id),
   path('cartas/crear/',views.crear_carta)

]