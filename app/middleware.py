# app/middleware.py

from django.contrib import messages
from django.db.models.deletion import ProtectedError  # Importação correta

class ProtectedErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ProtectedError):
            # Adiciona uma mensagem de erro à requisição
            messages.error(request, "Não é possível deletar este apartamento, pois ele está referenciado em outras entidades.")
            return None  # Não redireciona, apenas continua a requisição
