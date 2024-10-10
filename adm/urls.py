from django.urls import path
from .views import  menu_adm, menu_add

urlpatterns = [
    path('menu_adm/', menu_adm, name='menu_adm'),
    path('menu_add/', menu_add, name='menu_add'),

]
