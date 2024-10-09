from django.urls import path
from app.views import home
from .views import  menu_adm

urlpatterns = [
    path('', home, name='home'),
    path('menu_adm/', menu_adm, name='menu_adm'),

]
