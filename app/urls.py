from django.urls import path
from .views import home, editar_condominio, consultar_condominio  # Importar a view

urlpatterns = [
    path('', home, name='home'),
    path('editar_condominio/<int:id>/', editar_condominio, name='editar_condominio'),  # URL para editar
    path('consultar_condominio/<int:id>/', consultar_condominio, name='consultar_condominio'),  # URL para consultar
]
