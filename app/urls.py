from django.urls import path
from .views import (home, editar_condominio, consultar_condominio, excluir_condominio, register, lista_autenticacao,
                    configuracao, manage_groups, manage_users_groups_permissions, edit_group_permissions, delete_group,CustomLoginView  )

urlpatterns = [

    path('/app/', home, name='home'),
    path('configuracao/', configuracao, name='configuracao'),
    path('register/', register, name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    # Gerenciamento de Grupos
    path('grupos/', manage_groups, name='manage_groups'),
    path('grupos/<int:group_id>/editar/', edit_group_permissions, name='edit_group_permissions'),
    path('grupos/<int:group_id>/remover/', delete_group, name='delete_group'),

    # Gerenciamento de Usuários e Autenticação
    path('gerenciar_usuarios/', manage_users_groups_permissions, name='manage_users_groups_permissions'),
    path('autenticacao/', lista_autenticacao, name='lista_autenticacao'),

    # Gerenciamento de Condomínios
    path('editar/<int:id>/', editar_condominio, name='editar_condominio'),
    path('consultar/<int:id>/', consultar_condominio, name='consultar_condominio'),
    path('excluir/<int:id>/', excluir_condominio, name='excluir_condominio'),


]
