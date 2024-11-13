from django.urls import path
from . import views

urlpatterns = [
    path('sindicos/', views.lista_sindicos, name='lista_sindicos'),
    path('criar_sindico/', views.criar_sindico, name='criar_sindico'),
    path('get_apartamentos/<int:condominio_id>/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('get_pessoas/<int:apartamento_id>/', views.get_pessoas_por_apartamento, name='get_pessoas_por_apartamento'),
    path('sindicos/editar/<int:sindico_id>/', views.editar_sindico, name='editar_sindico'),
    path('sindicos/deletar/<int:sindico_id>/', views.deletar_sindico, name='deletar_sindico'),
]
