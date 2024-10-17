# urls.py

from django.urls import path
from liberacaoacesso import views

urlpatterns = [
    path('criar_liberacao_acesso/', views.criar_liberacao_acesso, name='criar_liberacao_acesso'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('get_pessoas_por_apartamento/', views.get_pessoas_por_apartamento, name='get_pessoas_por_apartamento'),
    # outras URLs...
]
