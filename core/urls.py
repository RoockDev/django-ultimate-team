from django.urls import path


from . import views

urlpatterns = [
path('cartas/',views.listar_cartas)

]