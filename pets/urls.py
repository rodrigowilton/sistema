from django.urls import path
from . import views

urlpatterns = [
    path('criar_pets/', views.criar_pets, name='criar_pets'),
    # URL para buscar apartamentos por condomínio
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('get_racas_por_tipo_raca/', views.get_racas_por_tipo_raca, name='get_racas_por_tipo_raca'),

]
