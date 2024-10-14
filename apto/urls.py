from django.urls import path
from . import views
from .views import criar_apartamentos


urlpatterns = [
    path('', views.list_apartamentos, name='list_apartamentos'),
    path('criar-apartamentos/', criar_apartamentos, name='criar_apartamentos'),
    path('editar-apartamento/<int:id>/', views.editar_apartamento, name='editar_apartamento'),

    path('add/', views.add_apartamento, name='add_apartamento'),
    path('edit/<int:id>/', views.edit_apartamento, name='edit_apartamento'),
    path('delete/<int:id>/', views.delete_apartamento, name='delete_apartamento'),
]
