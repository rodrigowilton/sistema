from django.urls import path
from . import views
from .views import consulta_area, editar_area, deletar_area

urlpatterns = [
    path('criar_area/', views.criar_area, name='criar_area'),
    path('consulta_area/', consulta_area, name='consulta_area'),
    path('editar_area/<int:area_id>/', editar_area, name='editar_area'),  # URL para editar área
    path('deletar_area/<int:area_id>/', deletar_area, name='deletar_area'),  # URL para deletar área


]
