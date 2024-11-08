# Em urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('agendamentos/', views.lista_agendamento, name='lista_agendamento'),
    path('agendamentos/novo/', views.criar_agendamento, name='criar_agendamento'),
    path('agendamentos/editar/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamentos/deletar/<int:pk>/', views.deletar_agendamento, name='deletar_agendamento'),
]
