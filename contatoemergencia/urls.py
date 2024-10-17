from django.urls import path
from . import views

urlpatterns = [
    path('criar_contato_emergencia/', views.criar_contato_emergencia, name='criar_contato_emergencia'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
]
