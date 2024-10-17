from django.shortcuts import render, redirect
from app.models import Recados, Condominios, Apartamentos, Pessoas, TatticaFuncionarios
from django.http import JsonResponse

def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')

    return JsonResponse({'apartamentos': list(apartamentos)})

def criar_recados(request):
    condominios = Condominios.objects.all()
    pessoas = Pessoas.objects.all()
    funcionarios = TatticaFuncionarios.objects.all()

    if request.method == 'POST':
        condominio = Condominios.objects.get(id=request.POST['condominio'])
        apartamento = Apartamentos.objects.get(id=request.POST['apartamento'])
        pessoa = Pessoas.objects.get(id=request.POST['pessoa'])
        funcionario = TatticaFuncionarios.objects.get(id=request.POST['tattica_funcionario'])
        nome_recado = request.POST['nome_recado']
        descricao = request.POST.get('descricao', '')
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']
        status = request.POST['status']

        Recados.objects.create(
            condominio=condominio,
            apartamento=apartamento,
            pessoa=pessoa,
            tattica_funcionario=funcionario,
            nome_recado=nome_recado,
            descricao=descricao,
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('listar_recados')  # redireciona após a criação

    return render(request, 'criar_recados.html', {
        'condominios': condominios,
        'pessoas': pessoas,
        'funcionarios': funcionarios,
    })
