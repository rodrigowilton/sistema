from django.urls import path
from .views import home, editar_condominio, consultar_condominio, excluir_condominio,register, lista_autenticacao, configuracao

urlpatterns = [
    path('', home, name='home'),
    path('configuracao/', configuracao, name='configuracao'),
    path('register/', register, name='register'),
    path('autenticacao/', lista_autenticacao, name='lista_autenticacao'),
    path('editar/<int:id>/', editar_condominio, name='editar_condominio'),
    path('consultar/<int:id>/', consultar_condominio, name='consultar_condominio'),
    path('excluir/<int:id>/', excluir_condominio, name='excluir_condominio'),
]
