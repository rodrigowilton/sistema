from django.urls import path
from .views import (AreasParalelasView, adicionar_area_paralela, EditarAreaParalelaView,
                    DeleteAreaParalelaView, get_areas, fetch_areas)

urlpatterns = [
    path('areas-paralelas/', AreasParalelasView.as_view(), name='areas_paralelas'),
    path('areas-paralelas/adicionar/', adicionar_area_paralela, name='adicionar_area_paralela'),
    path('areas-paralelas/editar/<int:pk>/', EditarAreaParalelaView.as_view(), name='editar_area_paralela'),
    path('areas-paralelas/deletar/<int:pk>/', DeleteAreaParalelaView.as_view(), name='deletar_area_paralela'),
    path('api/areas/<int:condominio_id>/', get_areas, name='get_areas'),  # Endpoint para obter áreas
    path('fetch-areas/<int:condominio_id>/', fetch_areas, name='fetch_areas'),

]
