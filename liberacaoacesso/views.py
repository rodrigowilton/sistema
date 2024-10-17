from django.shortcuts import render, redirect
from app.models import LiberacoesAcessos, Condominios, Apartamentos, Pessoas, TatticaFuncionarios
from django.utils import timezone
from django.http import JsonResponse

def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')
    return JsonResponse({'apartamentos': list(apartamentos)})

def get_pessoas_por_apartamento(request):
    apartamento_id = request.GET.get('apartamento_id')
    # Retorna todas as pessoas vinculadas ao apartamento, sem filtro de status
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id).values('id', 'nome_pessoa')  # Use 'nome_pessoa'
    return JsonResponse({'pessoas': list(pessoas)})

def criar_liberacao_acesso(request):
    if request.method == "POST":
        condominio_id = request.POST.get("condominio")
        apartamento_id = request.POST.get("apartamento")
        pessoa_id = request.POST.get("pessoa")
        tattica_funcionario_id = request.POST.get("tattica_funcionario")
        nome_acesso = request.POST.get("nome_acesso")
        descricao = request.POST.get("descricao")
        rg = request.POST.get("rg")
        cpf = request.POST.get("cpf")
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")

        # Cria uma nova liberação de acesso
        liberacao = LiberacoesAcessos(
            condominio_id=condominio_id,
            apartamento_id=apartamento_id,
            pessoa_id=pessoa_id,
            tattica_funcionario_id=tattica_funcionario_id,
            nome_acesso=nome_acesso,
            descricao=descricao,
            rg=rg,
            cpf=cpf,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=1,  # Definindo status como 1
            created=timezone.now(),
            modified=timezone.now(),
        )
        liberacao.save()  # Salva a liberação no banco de dados

        # Exibe uma mensagem de sucesso e redireciona
        return redirect('criar_liberacao_acesso')  # Aqui você pode redirecionar para uma página de sucesso, se necessário

    # Se não for um POST, renderiza o formulário
    condominios = Condominios.objects.all()
    apartamentos = []
    pessoas = []

    # Verifica se há um condomínio e um apartamento selecionados
    condominio_id = request.GET.get("condominio")
    apartamento_id = request.GET.get("apartamento")

    if condominio_id:
        apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)

    if apartamento_id:
        pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)  # Sem filtro de status

    funcionarios = TatticaFuncionarios.objects.all()

    return render(request, 'criar_liberacao_acesso.html', {
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
        'funcionarios': funcionarios,
    })
