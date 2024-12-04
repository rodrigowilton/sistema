from django.urls import path
from . import views
from .views import verificar_condominio_existe

urlpatterns = [
    path('adicionar/', views.adicionar_controleacesso, name='adicionar_controleacesso'),
    path('carregar_apartamentos/<int:condominio_id>/', views.carregar_apartamentos, name='carregar_apartamentos'),
    path('carregar_pessoas/<int:apartamento_id>/', views.carregar_pessoas, name='carregar_pessoas'),
    path('carregar_sindicos/<int:condominio_id>/', views.carregar_sindicos, name='carregar_sindicos'),
    path('menu_slc/', views.lista_controleacesso_pendente, name='menu_slc'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio,
         name='get_apartamentos_por_condominio'),
    path('get_pessoas_por_apartamento/', views.get_pessoas_por_apartamento, name='get_pessoas_por_apartamento'),
    path('condominios/verificar/', verificar_condominio_existe, name='verificar_condominio_existe'),
    path('get-apartamento-sindico/', views.get_apartamento_sindico, name='get_apartamento_sindico'),

    path('controleacesso/lista/', views.lista_controleacesso, name='lista_controleacesso'),
    path('adicionar_controle_acesso_morador/', views.adicionar_controle_acesso_morador, name='adicionar_controle_acesso_morador'),
    path('adicionar_controle_acesso_sindico/', views.adicionar_controle_acesso_sindico, name='adicionar_controle_acesso_sindico'),
    path('adicionar_controle_acesso_funcionario_condominio/', views.adicionar_controle_acesso_funcionario_condominio, name='adicionar_controle_acesso_funcionario_condominio'),
    path('adicionar_controle_acesso_outros/', views.adicionar_controle_acesso_outros, name='adicionar_controle_acesso_outros'),
    path('get_apartamentos/', views.get_apartamentos, name='get_apartamentos'),
    path('get_pessoas/', views.get_pessoas, name='get_pessoas'),
]

