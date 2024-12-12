from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/', views.adicionar_solicitacaoaudio, name='adicionar_solicitacaoaudio'),
    path('solicitacaoaudio/lista/', views.lista_solicitacaoaudio, name='lista_solicitacaoaudio'),
    path('solicitacaoaudio/lista_pendente/', views.lista_solicitacaoaudio_pendente, name='lista_solicitacaoaudio_pendente'),
    path('adicionar_solicitacao_audio_morador/', views.adicionar_solicitacaoaudio_morador, name='adicionar_solicitacao_audio_morador'),
    path('adicionar_solicitacao_audio_sindico/', views.adicionar_solicitacaoaudio_sindico, name='adicionar_solicitacao_audio_sindico'),
    path('adicionar_solicitacao_audio_funcionario_condominio/', views.adicionar_solicitacaoaudio_funcionario_condominio, name='adicionar_solicitacao_audio_funcionario_condominio'),
    path('adicionar_solicitacao_audio_outros/', views.adicionar_solicitacaoaudio_outros, name='adicionar_solicitacao_audio_outros'),

    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio,name='get_apartamentos_por_condominio'),
    path('get_apartamentos/', views.get_apartamentos, name='get_apartamentos'),
    path('get_pessoas/', views.get_pessoas, name='get_pessoas'),
    path('get_sindicos_por_condominio/<int:condominio_id>/', views.get_sindicos_por_condominio,name='get_sindicos_por_condominio'),

    path('carregar-funcionarios/', views.carregar_funcionarios, name='carregar_funcionarios'),
    path('carregar_funcionarios_condominio/', views.carregar_funcionarios_condominio, name='carregar_funcionarios_condominio'),

]


