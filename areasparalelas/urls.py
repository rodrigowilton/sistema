from django.urls import path
from .views import AreasParalelasView,editar_area_paralela, DeleteAreaParalelaView, buscar_areas_paralelas, adicionar_area_paralela
from .views import get_areas

urlpatterns = [
    path('areas-paralelas/', buscar_areas_paralelas, name='areas_paralelas'),
    path('adicionar_area_paralela/', adicionar_area_paralela, name='adicionar_area_paralela'),
    path('editar-area-paralela/<int:pk>/', editar_area_paralela, name='editar_area_paralela'),
    path('deletar-area-paralela/<int:pk>/', DeleteAreaParalelaView.as_view(), name='deletar_area_paralela'),
    path('get-areas/', get_areas, name='get_areas'),  # URL para a view AJAX

]
