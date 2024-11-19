from django.urls import path
from . import views

urlpatterns = [
    path('prestadores/', views.lista_prestadores, name='lista_prestadores'),
    path('prestadores/adicionar/', views.adicionar_prestador, name='adicionar_prestador'),
    path('prestadores/editar/<int:pk>/', views.editar_prestador, name='editar_prestador'),
    path('prestadores/deletar/<int:pk>/', views.deletar_prestador, name='deletar_prestador'),
]
