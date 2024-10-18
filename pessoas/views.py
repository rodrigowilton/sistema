from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Pessoas, Apartamentos, Condominios, Criticidades, TiposClassificacaos, TiposPessoas
from .forms import PessoasForm  # Certifique-se de criar um formulário para o modelo Pessoas
from django.http import JsonResponse

@login_required
def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    apartamento_id = request.GET.get('apartamento_id')

    # Verifica se o CPF já está cadastrado no apartamento
    existe = Pessoas.objects.filter(cpf=cpf, apartamento_id=apartamento_id).exists()

    return JsonResponse({'existe': existe})


@login_required
def get_condominio(request, apartamento_id):
    apartamento = Apartamentos.objects.get(id=apartamento_id)
    return JsonResponse({'condominio': str(apartamento.condominio)})
class ListPessoasView(View):
    def get(self, request):
        pessoas = Pessoas.objects.all()
        return render(request, 'list_pessoas.html', {'pessoas': pessoas})


@login_required
def criar_pessoa(request):
    condominios = Condominios.objects.filter(status=1)  # Condominios ativos
    criticidades = Criticidades.objects.all()  # Criticidades do banco
    classificacoes = TiposClassificacaos.objects.all()  # Classificações do banco

    if request.method == 'POST':
        # Coletando dados do formulário
        condominio_id = request.POST.get('condominio')
        apartamento_id = request.POST.get('apartamento')
        tipos_pessoa_value = request.POST.get('tipos_pessoa')  # Alterado para 'tipos_pessoa'
        responsavel = request.POST.get('responsavel')
        nome_pessoa = request.POST.get('nome_pessoa')
        parentesco = request.POST.get('parentesco')
        data_aniversario = request.POST.get('data_aniversario')
        sexo = request.POST.get('sexo')
        celular = request.POST.get('celular')
        celular_2 = request.POST.get('celular_2')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        profissao = request.POST.get('profissao')
        criticidade_id = request.POST.get('criticidade')
        tipos_classificacao_id = request.POST.get('tipos_classificacao')
        observacao = request.POST.get('observacoes')  # Alterado para 'observacao'

        # Verificando se o CPF já existe no apartamento
        cpf_existe = Pessoas.objects.filter(apartamento_id=apartamento_id, cpf=cpf).exists()
        if cpf_existe:
            messages.warning(request, 'Já existe uma pessoa cadastrada com este CPF neste apartamento.')
            return redirect('criar_pessoas')  # Redireciona para a página atual

        # Buscando o objeto TiposPessoas usando o campo correto
        tipos_pessoa = TiposPessoas.objects.get(nome_tipos_pessoa=tipos_pessoa_value)  # Use 'nome_tipos_pessoa'

        # Criando a nova pessoa
        try:
            nova_pessoa = Pessoas(
                apartamento_id=apartamento_id,
                tipos_pessoa=tipos_pessoa,
                responsavel=responsavel,
                nome_pessoa=nome_pessoa,
                parentesco=parentesco,
                data_aniversario=data_aniversario,
                sexo=sexo,
                celular=celular,
                celular_2=celular_2,
                email=email,
                cpf=cpf,
                rg=rg,
                profissao=profissao,
                criticidade_id=criticidade_id,
                tipos_classificacao_id=tipos_classificacao_id,
                observacao=observacao,  # Alterado para 'observacao'
                status=1  # Definindo o status como 1
            )
            nova_pessoa.save()  # Salvando a nova pessoa no banco de dados
            messages.success(request, 'Pessoa cadastrada com sucesso!')
            return redirect('criar_pessoas')  # Redireciona para a página inicial ou onde preferir
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar pessoa: {str(e)}')

    return render(request, 'criar_pessoas.html', {
        'condominios': condominios,
        'criticidades': criticidades,
        'tipos_classificacaos': classificacoes,
        'tipos_pessoas': TiposPessoas.objects.all(),  # Tipos de pessoa (Proprietário, Inquilino, etc)
    })


@login_required
def listar_pessoas(request):
    pessoas = Pessoas.objects.all()  # Obtém todas as pessoas do banco de dados
    return render(request, 'list_pessoas.html', {'pessoas': pessoas})

@login_required
def editar_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoas, id=pessoa_id)

    if request.method == 'POST':
        # Coletando dados do formulário
        pessoa.nome_pessoa = request.POST.get('nome_pessoa')
        pessoa.cpf = request.POST.get('cpf')
        pessoa.celular = request.POST.get('celular')
        pessoa.email = request.POST.get('email')
        # Atualize outros campos conforme necessário

        try:
            pessoa.save()  # Salvando as alterações no banco de dados
            messages.success(request, 'Pessoa editada com sucesso!')
            return redirect('list_pessoas')  # Redireciona para a lista de pessoas
        except Exception as e:
            messages.error(request, f'Erro ao editar pessoa: {str(e)}')

    return render(request, 'editar_pessoas.html', {'pessoa': pessoa})
# View para carregar apartamentos dinamicamente

@login_required
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