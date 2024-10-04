from django.shortcuts import render, get_object_or_404, redirect
from .models import Condominios
from django.contrib import messages

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

def excluir_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)

    if request.method == 'POST':
        condominio.delete()
        messages.success(request, 'Condomínio excluído com sucesso!')
        return redirect('home')  # Redireciona para a página inicial após a exclusão

    return render(request, 'confirmar_exclusao.html', {'condominio': condominio})
