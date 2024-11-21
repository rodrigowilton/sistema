from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_controleacesso, name='adicionar_controleacesso'),
    path('carregar_apartamentos/<int:condominio_id>/', views.carregar_apartamentos, name='carregar_apartamentos'),
    path('carregar_pessoas/<int:apartamento_id>/', views.carregar_pessoas, name='carregar_pessoas'),
    path('carregar_sindicos/<int:condominio_id>/', views.carregar_sindicos, name='carregar_sindicos'),
    path('controleacesso/lista/', views.lista_controleacesso, name='lista_controleacesso'),
]
