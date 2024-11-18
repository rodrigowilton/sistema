from django.urls import path
from . import views

urlpatterns = [
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/adicionar/', views.adicionar_empresas, name='adicionar_empresas'),
    path('empresas/editar/<int:pk>/', views.editar_empresas, name='editar_empresas'),
    path('empresas/deletar/<int:pk>/', views.deletar_empresas, name='deletar_empresas'),
]
