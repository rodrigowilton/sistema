from django.urls import path
from . import views

urlpatterns = [
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('adicionar_empresa/', views.adicionar_empresa, name='adicionar_empresa'),
    path('editar_empresas/<int:pk>/', views.editar_empresas, name='editar_empresas'),
    path('deletar_empresas/<int:pk>/', views.deletar_empresas, name='deletar_empresas'),
]
