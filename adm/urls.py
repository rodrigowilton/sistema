from django.urls import path
from .views import  menu_adm, menu_add, menu_ctr, menu_agd, menu_srv, menu_slc, menu_ocr, menu_tel, menu_inf
from django.urls import path
from .views import *

urlpatterns = [
    path('menu_adm/', menu_adm, name='menu_adm'),
    path('menu_add/', menu_add, name='menu_add'),
    path('menu_ctr/', menu_ctr, name='menu_ctr'),
    path('menu_agd/', menu_agd, name='menu_agd'),
    path('menu_srv/', menu_srv, name='menu_srv'),
    path('menu_slc/', menu_slc, name='menu_slc'),
    path('menu_ocr/', menu_ocr, name='menu_ocr'),
    path('menu_tel/', menu_tel, name='menu_tel'),
    path('menu_inf/', menu_inf, name='menu_inf'),

    # crud condominios


    path('condominios/', list_condominios, name='list_condominios'),
    path('condominios/criar/', criar_condominio, name='create_condominio'),
    path('condominios/<int:id>/', detail_condominio, name='detail_condominio'),
    path('condominios/<int:id>/editar/', update_condominio, name='update_condominio'),
    path('condominios/<int:id>/remover/', delete_condominio, name='delete_condominio'),


]
