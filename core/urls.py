from django.urls import path


from . import views

urlpatterns = [
   path('cartas/',views.listar_cartas),
   path('cartas/<int:carta_id>/',views.obtener_carta_id),
   path('cartas/crear/',views.crear_carta),
   path('cartas/actualizar/<int:carta_id>/',views.actualizar_carta),
   path('cartas/actualizar_especifica/<int:carta_id>/',views.actualizar_campos_especificos_carta),
   path('cartas/borrar/<int:carta_id>/',views.borrar_carta),
   path('usuarios/', views.listar_usuarios),
   path('usuarios/<int:usuario_id>/', views.obtener_usuario_id),
   path('usuarios/crear/', views.crear_usuario),
   path('usuarios/actualizar/<int:usuario_id>/', views.actualizar_usuario),
   path('usuarios/actualizar_especifica/<int:usuario_id>/', views.actualizar_campos_especificos_usuario),
   path('usuarios/borrar/<int:usuario_id>/', views.borrar_usuario),
   path('equipo/asignar/<int:usuario_id>/',views.asignar_equipo_a_usuario),
   path('equipo/eliminar/<int:usuario_id>/',views.eliminar_equipo_de_usuario),
   path('equipo/consultar/<int:usuario_id>/', views.consultar_equipo_usuario),
   path('equipos/<int:equipo_id>/anadir_carta/', views.anadir_carta_a_equipo)
]