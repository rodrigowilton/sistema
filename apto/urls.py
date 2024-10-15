from django.urls import path
from . import views
from .views import criar_apartamentos, editar_apartamento


urlpatterns = [
    path('criar-apartamentos/', criar_apartamentos, name='criar_apartamentos'),
    path('editar-apartamento/<int:apartamento_id>/', editar_apartamento, name='editar_apartamento'),  # URL para editar

]
