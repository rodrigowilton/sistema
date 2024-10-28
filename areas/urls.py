from django.urls import path
from . import views

urlpatterns = [
    path('criar_area/', views.criar_area, name='criar_area'),
]
