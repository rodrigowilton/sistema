from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import Recados, Condominios, Apartamentos, Pessoas, TatticaFuncionarios
from django.http import JsonResponse

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')

    return JsonResponse({'apartamentos': list(apartamentos)})


@login_required
def get_pessoas_por_apartamento(request):
    condominio_id = request.GET.get('condominio_id')
    apartamento_id = request.GET.get('apartamento_id')

    # Filtra as pessoas que estão vinculadas ao condomínio e apartamento
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id, apartamento__condominio_id=condominio_id).values(
        'id', 'nome_pessoa')

    return JsonResponse({'pessoas': list(pessoas)})

@login_required
def criar_recados(request):
    condominios = Condominios.objects.all()
    funcionarios = TatticaFuncionarios.objects.all()

    if request.method == 'POST':
        condominio = Condominios.objects.get(id=request.POST['condominio'])
        apartamento = Apartamentos.objects.get(id=request.POST['apartamento'])
        pessoa = Pessoas.objects.get(id=request.POST['pessoa'])
        funcionario = None

        if request.POST.get('tattica_funcionario'):
            funcionario = TatticaFuncionarios.objects.get(id=request.POST['tattica_funcionario'])

        nome_recado = request.POST['nome_recado']
        descricao = request.POST.get('descricao', '')
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']

        # Definir o status como 1 diretamente no backend
        status = 1

        Recados.objects.create(
            condominio=condominio,
            apartamento=apartamento,
            pessoa=pessoa,
            tattica_funcionario=funcionario,
            nome_recado=nome_recado,
            descricao=descricao,
            status=status,  # status fixo como 1
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        messages.success(request, 'Recado atualizado com sucesso!')

        return redirect('criar_recados')  # redireciona após a criação

    return render(request, 'criar_recados.html', {
        'condominios': condominios,
        'funcionarios': funcionarios,
    })
