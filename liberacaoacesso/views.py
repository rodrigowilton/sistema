from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import LiberacoesAcessos, Condominios, Apartamentos, Pessoas, TatticaFuncionarios, TiposPessoas
from django.utils import timezone
from django.http import JsonResponse

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')
    return JsonResponse({'apartamentos': list(apartamentos)})

@login_required
def get_pessoas_por_apartamento(request):
    apartamento_id = request.GET.get('apartamento_id')
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)  # Sem filtro de status, conforme solicitado
    data = {
        'pessoas': [
            {
                'id': pessoa.id,
                'nome_pessoa': pessoa.nome_pessoa,
                'tipo_pessoa': pessoa.tipos_pessoa.nome_tipos_pessoa,  # Corrigido para 'tipos_pessoa'
                'is_proprietario': pessoa.tipos_pessoa.nome_tipos_pessoa == 'Proprietário'  # Verifica se é proprietário
            }
            for pessoa in pessoas
        ]
    }
    return JsonResponse(data)

@login_required
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

        # Verifica se já existe uma liberação de acesso para o CPF entre as datas
        existe_liberacao = LiberacoesAcessos.objects.filter(
            cpf=cpf,
            data_inicio__lte=data_fim,
            # A data de início da nova liberação deve ser antes ou igual à data final da liberação existente
            data_fim__gte=data_inicio
            # A data de fim da nova liberação deve ser depois ou igual à data inicial da liberação existente
        ).exists()

        if existe_liberacao:
            return render(request, 'criar_liberacao_acesso.html', {
                'condominios': Condominios.objects.all(),
                'apartamentos': Apartamentos.objects.filter(condominio_id=condominio_id) if condominio_id else [],
                'pessoas': Pessoas.objects.filter(apartamento_id=apartamento_id),  # Sem filtro de status
                'funcionarios': TatticaFuncionarios.objects.all(),
                'erro': 'Já existe uma liberação de acesso para este CPF entre as datas especificadas.'
            })

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
        messages.success(request, 'Cadastro criado com sucesso!')

        return redirect(
            'liberacaoacesso:criar_liberacao_acesso')  # Aqui você pode redirecionar para uma página de sucesso, se necessário

    # Se não for um POST, renderiza o formulário
    condominios = Condominios.objects.all()
    apartamentos = []
    pessoas = []

    # Verifica se há um condomínio selecionado e limpa os campos
    condominio_id = request.GET.get("condominio")
    apartamento_id = request.GET.get("apartamento")

    if condominio_id:
        apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
        pessoas = []  # Limpa a lista de pessoas ao mudar o condomínio
    else:
        apartamento_id = None  # Limpa o apartamento se não houver condomínio selecionado

    if apartamento_id:
        pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)  # Sem filtro de status

    funcionarios = TatticaFuncionarios.objects.all()

    return render(request, 'criar_liberacao_acesso.html', {
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
        'funcionarios': funcionarios,
        'erro': None  # Inicializa a variável de erro como None
    })

