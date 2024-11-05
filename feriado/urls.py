from django.urls import path
from .views import adicionar_feriados, editar_feriados, deletar_feriados, listar_feriados

urlpatterns = [
    path('adicionar-feriado/', adicionar_feriados, name='adicionar_feriados'),
    path('editar-feriado/<int:feriado_id>/', editar_feriados, name='editar_feriados'),
    path('deletar-feriado/<int:feriado_id>/', deletar_feriados, name='deletar_feriados'),
    path('listar-feriados/', listar_feriados, name='listar_feriados'),  # URL para listar feriados
]
