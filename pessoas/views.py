from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Pessoas, Apartamentos, Condominios, Criticidades, TiposClassificacaos, TiposPessoas
from .forms import PessoasForm  # Certifique-se de criar um formulário para o modelo Pessoas
from django.http import JsonResponse

def get_condominio(request, apartamento_id):
    apartamento = Apartamentos.objects.get(id=apartamento_id)
    return JsonResponse({'condominio': str(apartamento.condominio)})
class ListPessoasView(View):
    def get(self, request):
        pessoas = Pessoas.objects.all()
        return render(request, 'list_pessoas.html', {'pessoas': pessoas})



def criar_pessoa(request):
    condominios = Condominios.objects.filter(status=1)  # Condominios ativos
    criticidades = Criticidades.objects.all()  # Criticidades do banco
    classificacoes = TiposClassificacaos.objects.all()  # Classificações do banco

    if request.method == 'POST':
        # Tratamento de formulário POST e criação da pessoa
        pass

    return render(request, 'criar_pessoas.html', {
        'condominios': condominios,
        'criticidades': criticidades,
        'tipos_classificacaos': classificacoes,
        'tipos_pessoas': TiposPessoas.objects.all(),  # Tipos de pessoa (Proprietário, Inquilino, etc)
    })

# View para carregar apartamentos dinamicamente
from django.http import JsonResponse

def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    data = {
        'apartamentos': [{'id': apto.id, 'nome_apartamento': apto.nome_apartamento} for apto in apartamentos]
    }
    return JsonResponse(data)


class DeletarPessoasView(View):
    def get(self, request, pk):
        pessoa = get_object_or_404(Pessoas, pk=pk)
        return render(request, 'deletar_pessoas.html', {'pessoa': pessoa})

    def post(self, request, pk):
        pessoa = get_object_or_404(Pessoas, pk=pk)
        pessoa.delete()
        return redirect('list_pessoas')