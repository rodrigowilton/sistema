from django.urls import path
from .views import  menu_adm, menu_add, menu_ctr, menu_agd, menu_srv, menu_slc, menu_ocr

urlpatterns = [
    path('menu_adm/', menu_adm, name='menu_adm'),
    path('menu_add/', menu_add, name='menu_add'),
    path('menu_ctr/', menu_ctr, name='menu_ctr'),
    path('menu_agd/', menu_agd, name='menu_agd'),
    path('menu_srv/', menu_srv, name='menu_srv'),
    path('menu_slc/', menu_slc, name='menu_slc'),
    path('menu_ocr/', menu_ocr, name='menu_ocr'),

]
