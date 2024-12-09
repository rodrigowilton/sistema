from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_controleacesso, name='adicionar_controleacesso'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio,
         name='get_apartamentos_por_condominio'),

    path('controleacesso/lista/', views.lista_controleacesso, name='lista_controleacesso'),
    path('controleacesso/lista_pendente/', views.lista_controleacesso_pendente, name='lista_controleacesso_pendente'),
    path('adicionar_controle_acesso_morador/', views.adicionar_controle_acesso_morador, name='adicionar_controle_acesso_morador'),
    path('adicionar_controle_acesso_sindico/', views.adicionar_controle_acesso_sindico, name='adicionar_controle_acesso_sindico'),
    path('adicionar_controle_acesso_funcionario_condominio/', views.adicionar_controle_acesso_funcionario_condominio, name='adicionar_controle_acesso_funcionario_condominio'),
    path('adicionar_controle_acesso_outros/', views.adicionar_controle_acesso_outros, name='adicionar_controle_acesso_outros'),
    path('get_apartamentos/', views.get_apartamentos, name='get_apartamentos'),
    path('get_pessoas/', views.get_pessoas, name='get_pessoas'),

    path('adicionar-controle-acesso/', views.adicionar_controle_acesso_sindico,name='adicionar_controle_acesso_sindico'),
    path('get_sindicos_por_condominio/<int:condominio_id>/', views.get_sindicos_por_condominio,name='get_sindicos_por_condominio'),

    path('carregar-funcionarios/', views.carregar_funcionarios, name='carregar_funcionarios'),
    path('carregar_funcionarios_condominio/', views.carregar_funcionarios_condominio, name='carregar_funcionarios_condominio'),

]


