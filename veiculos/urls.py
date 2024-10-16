from django.urls import path
from .views import criar_veiculos, editar_veiculos, listar_pessoas, get_apartamentos_por_condominio

urlpatterns = [
    path('criar/', criar_veiculos, name='criar_veiculos'),
    path('editar/<int:veiculo_id>/', editar_veiculos, name='editar_veiculos'),
    path('listar/', listar_pessoas, name='listar_pessoas'),
    path('get_apartamentos_por_condominio/', get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
]
