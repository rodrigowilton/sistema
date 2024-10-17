# urls.py

from django.urls import path
from .views import criar_liberacao_acesso

urlpatterns = [
    path('criar_liberacao_acesso/', criar_liberacao_acesso, name='criar_liberacao_acesso'),
    # outras URLs...
]
