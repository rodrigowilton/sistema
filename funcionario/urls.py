from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('adicionar_funcionario/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('editar_funcionario/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('deletar_funcionario/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),
    path('condominios/verificar/', verificar_condominio_existe, name='verificar_condominio_existe'),

]
