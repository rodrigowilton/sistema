from django.urls import path
from . import views

urlpatterns = [
    path('horarioagendamento/', views.listar_agendamento_horarios, name='listar_agendamento_horarios'),
    path('horarioagendamento/adicionar/', views.adicionar_horario_agendamento, name='adicionar_horario_agendamento'),
    path('horarioagendamento/editar/<int:id>/', views.editar_horario_agendamento, name='editar_horario_agendamento'),
    path('horarioagendamento/deletar/<int:id>/', views.deletar_horario_agendamento, name='deletar_horario_agendamento'),
    # Outros paths, se houver
]
