from django.urls import path
from . import views

urlpatterns = [
    path('lista_servicoempresa/', views.lista_servicoempresa, name='lista_servicoempresa'),
    path('criar_servicoempresa/', views.criar_servicoempresa, name='criar_servicoempresa'),
    path('editar_servicoempresa/<int:pk>/', views.editar_servicoempresa, name='editar_servicoempresa'),
    path('deletar_servicoempresa/<int:pk>/', views.deletar_servicoempresa, name='deletar_servicoempresa'),
]
