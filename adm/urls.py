from django.urls import path
from .views import  menu_adm

urlpatterns = [
    path('menu_adm/', menu_adm, name='menu_adm'),

]
