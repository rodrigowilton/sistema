from django.shortcuts import render, get_object_or_404
from .models import Condominios

def home(request):
    # Tente obter todos os condomínios do banco de dados
    try:
        condominios = Condominios.objects.all()
    except Exception as e:
        print(f"Erro ao buscar condomínios: {e}")
        condominios = []

    context = {
        'condominios': condominios,
    }

    return render(request, 'home.html', context)

def editar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para editar o condomínio aqui
    return render(request, 'editar_condominio.html', {'condominio': condominio})

def consultar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para consultar o condomínio aqui
    return render(request, 'consultar_condominio.html', {'condominio': condominio})