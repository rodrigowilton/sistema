from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import PermissaoAcessos, Condominios, Apartamentos, TiposAcessos, TiposFuncionarios, Funcionarios
from django.http import JsonResponse


def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_apartamento')

    return JsonResponse({'apartamentos': list(apartamentos)})


def criar_permissao_acesso(request):
    condominios = Condominios.objects.filter(status=1)
    tipos_acessos = TiposAcessos.objects.filter(status=1)
    tipos_funcionarios = TiposFuncionarios.objects.filter(status=1)

    if request.method == 'POST':
        condominio = get_object_or_404(Condominios, id=request.POST['condominio'], status=1)
        apartamento = get_object_or_404(Apartamentos, id=request.POST['apartamento'], status=1)
        tipo_acesso = get_object_or_404(TiposAcessos, id=request.POST['tipos_acesso'], status=1)
        tipo_funcionario = get_object_or_404(TiposFuncionarios, id=request.POST['tipos_funcionario'], status=1)

        funcionario_nome = request.POST['nome_funcionario']
        funcionario_cpf = request.POST['cpf']
        funcionario_rg = request.POST['rg']
        funcionario_celular = request.POST['celular']
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']

        # Convertendo 'on' para True e None para False
        domingo = True if request.POST.get('domingo') == 'on' else False
        segunda = True if request.POST.get('segunda') == 'on' else False
        terca = True if request.POST.get('terca') == 'on' else False
        quarta = True if request.POST.get('quarta') == 'on' else False
        quinta = True if request.POST.get('quinta') == 'on' else False
        sexta = True if request.POST.get('sexta') == 'on' else False
        sabado = True if request.POST.get('sabado') == 'on' else False

        acesso_livre = request.POST['acesso_livre']

        funcionario = Funcionarios.objects.create(
            nome_funcionario=funcionario_nome,
            cpf=funcionario_cpf,
            rg=funcionario_rg,
            celular=funcionario_celular,
            tipos_funcionario=tipo_funcionario,
            status=1  # Define status como ativo
        )

        permissao_acesso = PermissaoAcessos(
            condominio=condominio,
            apartamento=apartamento,
            tipos_acesso=tipo_acesso,
            funcionario=funcionario,
            data_inicio=data_inicio,
            data_fim=data_fim,
            domingo=domingo,
            segunda=segunda,
            terca=terca,
            quarta=quarta,
            quinta=quinta,
            sexta=sexta,
            sabado=sabado,
            acesso_livre=acesso_livre,
            status=1  # Define status como ativo
        )

        permissao_acesso.save()

        messages.success(request, 'Permissão de acesso criada com sucesso!')
        return redirect('criar_permissao_acesso')

    return render(request, 'criar_permissao_acesso.html', {
        'condominios': condominios,
        'tipos_acessos': tipos_acessos,
        'tipos_funcionarios': tipos_funcionarios,
    })
