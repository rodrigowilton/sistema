from django.urls import path
from appmorador import views

urlpatterns = [
    path('app_morador/', views.app_morador, name='app_morador'),

]
