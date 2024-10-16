from django.urls import path
from .views import ListPessoasView, criar_pessoa, DeletarPessoasView,get_apartamentos_por_condominio
from . import views

urlpatterns = [
    path('criar/', criar_pessoa, name='criar_pessoas'),
    path('get-apartamentos-por-condominio/', get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('', ListPessoasView.as_view(), name='list_pessoas'),  # CBV - View baseada em classe
    path('deletar/<int:pk>/', DeletarPessoasView.as_view(), name='deletar_pessoas'),  # CBV
    path('get-condominio/<int:apartamento_id>/', views.get_condominio, name='get_condominio'),  # Função para obter condomínio
]
