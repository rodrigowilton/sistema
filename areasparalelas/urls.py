from django.urls import path
from .views import AreasParalelasView, adicionar_area_paralela, EditarAreaParalelaView, DeleteAreaParalelaView, get_areas

urlpatterns = [
    path('areas-paralelas/', AreasParalelasView.as_view(), name='areas_paralelas'),
    path('adicionar-area-paralela/', adicionar_area_paralela, name='adicionar_area_paralela'),
    path('editar-area-paralela/<int:pk>/', EditarAreaParalelaView.as_view(), name='editar_area_paralela'),
    path('deletar-area-paralela/<int:pk>/', DeleteAreaParalelaView.as_view(), name='deletar_area_paralela'),
    path('get-areas/<int:condominio_id>/', get_areas, name='get_areas'),  # Certifique-se de que está usando get_areas
]
