from django.urls import path
from . import views

urlpatterns = [
    path('criar_recados/', views.criar_recados, name='criar_recados'),
    path('get_apartamentos_por_condominio/', views.get_apartamentos_por_condominio, name='get_apartamentos_por_condominio'),
    path('get_pessoas_por_apartamento/', views.get_pessoas_por_apartamento, name='get_pessoas_por_apartamento'),

]
