from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('criar/', criar_pessoa, name='criar_pessoas'),  # URL para criar uma nova pessoa
    path('verificar-cpf/', verificar_cpf, name='verificar_cpf'),
    path('editar/<int:pessoa_id>/', editar_pessoa, name='editar_pessoa'),  # URL para editar uma pessoa
    path('listar/', listar_pessoas, name='listar_pessoas'),  # URL para listar pessoas
    path('get-apartamentos-por-condominio/', get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('deletar/<int:pk>/', DeletarPessoasView.as_view(), name='deletar_pessoas'),  # CBV
    path('get-condominio/<int:apartamento_id>/', views.get_condominio, name='get_condominio'),  # Função para obter condomínio
]
