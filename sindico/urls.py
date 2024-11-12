from django.urls import path
from . import views

urlpatterns = [
    path('sindicos/', views.lista_sindicos, name='lista_sindicos'),
    path('sindicos/criar/', views.criar_sindico, name='criar_sindico'),
    path('sindicos/editar/<int:sindico_id>/', views.editar_sindico, name='editar_sindico'),
    path('sindicos/deletar/<int:sindico_id>/', views.deletar_sindico, name='deletar_sindico'),
]
