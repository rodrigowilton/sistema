from django.urls import path
from permissaoacesso import views

urlpatterns = [
    # URL para criar permissões de acesso
    path('permissoes_acesso/criar/', views.criar_permissao_acesso, name='criar_permissao_acesso'),
    # URL para buscar apartamentos por condomínio via AJAX
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
]
