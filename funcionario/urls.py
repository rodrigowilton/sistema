from django.urls import path
from . import views

urlpatterns = [
    path('funcionarios/', views.list_funcionarios, name='lista_funcionarios'),
    path('editar_funcionario/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('deletar_funcionario/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),

]
