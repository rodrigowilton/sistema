from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Pessoas, Apartamentos, Condominios

from .forms import PessoasForm  # Certifique-se de criar um formulário para o modelo Pessoas
from django.http import JsonResponse

def get_condominio(request, apartamento_id):
    apartamento = Apartamentos.objects.get(id=apartamento_id)
    return JsonResponse({'condominio': str(apartamento.condominio)})
class ListPessoasView(View):
    def get(self, request):
        pessoas = Pessoas.objects.all()
        return render(request, 'list_pessoas.html', {'pessoas': pessoas})




# View para criar uma nova pessoa
def criar_pessoa(request):
    if request.method == 'POST':
        # Aqui você processa os dados do formulário e cria a pessoa
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_pessoas')
    else:
        form = PessoasForm()

    # Pegamos todos os condomínios ativos (ajuste de status conforme sua lógica de status)
    condominios = Condominios.objects.filter(status=1)  # Considerando '1' como ativo

    return render(request, 'criar_pessoas.html', {
        'form': form,
        'condominios': condominios
    })


# View para retornar os apartamentos de um condomínio via AJAX
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1)  # '1' como ativo

    apartamentos_data = [
        {'id': apartamento.id, 'nome_apartamento': apartamento.nome_apartamento}
        for apartamento in apartamentos
    ]

    return JsonResponse({'apartamentos': apartamentos_data})

class DeletarPessoasView(View):
    def get(self, request, pk):
        pessoa = get_object_or_404(Pessoas, pk=pk)
        return render(request, 'deletar_pessoas.html', {'pessoa': pessoa})

    def post(self, request, pk):
        pessoa = get_object_or_404(Pessoas, pk=pk)
        pessoa.delete()
        return redirect('list_pessoas')