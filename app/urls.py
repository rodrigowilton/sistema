from django.urls import path
from .views import home, editar_condominio, consultar_condominio, excluir_condominio

urlpatterns = [
    path('', home, name='home'),
    path('editar/<int:id>/', editar_condominio, name='editar_condominio'),
    path('consultar/<int:id>/', consultar_condominio, name='consultar_condominio'),
    path('excluir/<int:id>/', excluir_condominio, name='excluir_condominio'),
]
