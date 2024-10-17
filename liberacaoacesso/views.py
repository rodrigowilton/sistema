# views.py

from django.shortcuts import render, redirect
from app.models import LiberacoesAcessos, Condominios, Apartamentos, Pessoas, TatticaFuncionarios
from django.utils import timezone

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
        return redirect('criar_liberacao_acesso')  # Redireciona para uma página de sucesso (ajuste conforme necessário)

    # Se não for um POST, renderiza o formulário
    condominios = Condominios.objects.all()
    apartamentos = Apartamentos.objects.all()
    pessoas = Pessoas.objects.all()
    funcionarios = TatticaFuncionarios.objects.all()

    return render(request, 'criar_liberacao_acesso.html', {
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
        'funcionarios': funcionarios,
    })
