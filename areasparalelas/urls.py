from django.urls import path
from .views import AreasParalelasView,EditarAreaParalelaView, DeleteAreaParalelaView, buscar_areas_paralelas, adicionar_area_paralela

urlpatterns = [
    path('areas-paralelas/', buscar_areas_paralelas, name='areas_paralelas'),
    path('adicionar_area_paralela/', adicionar_area_paralela, name='adicionar_area_paralela'),
    path('editar-area-paralela/<int:pk>/', EditarAreaParalelaView.as_view(), name='editar_area_paralela'),
    path('deletar-area-paralela/<int:pk>/', DeleteAreaParalelaView.as_view(), name='deletar_area_paralela'),
]
