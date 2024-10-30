from django.urls import path
from .views import AreasParalelasView, EditarAreaParalelaView, DeleteAreaParalelaView

urlpatterns = [
    # outras URLs
    path('areas-paralelas/', AreasParalelasView.as_view(), name='areas_paralelas'),
    path('areas-paralelas/editar/<int:pk>/', EditarAreaParalelaView.as_view(), name='editar_area_paralela'),
    path('areas-paralelas/deletar/<int:pk>/', DeleteAreaParalelaView.as_view(), name='deletar_area_paralela'),
]
