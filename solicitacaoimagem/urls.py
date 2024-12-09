from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_solicitacaoimagem, name='adicionar_solicitacaoimagem'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio,
         name='get_apartamentos_por_condominio'),

    path('solicitacaoimagem/lista/', views.lista_solicitacaoimagem, name='lista_solicitacaoimagem'),
    path('solicitacaoimagem/lista_pendente/', views.lista_solicitacaoimagem_pendente, name='lista_solicitacaoimagem_pendente'),
    path('adicionar_solicitacao_imagem_morador/', views.adicionar_solicitacaoimagem_morador, name='adicionar_solicitacao_imagem_morador'),
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


