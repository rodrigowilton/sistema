from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app.models import (ControlesAcessos, TatticaFuncionarios, TiposControlesAcessos, Condominios,
                        Apartamentos, Pessoas, Sindicos, TiposSindicos)
from django.http import JsonResponse
from controleacesso.forms import ControleAcessoMoradorForm
from django.utils.timezone import now  # Para exibir a data atual se necessário
from django.contrib import messages  # Para exibir mensagens ao usuário
from controleacesso.templatetags.custom_tags import adicionar_dias_uteis, dias_uteis_mais


@login_required
def verificar_condominio_existe(request):
    if request.method == 'GET':
        nome_condominio = request.GET.get('nome_condominio', '').strip()
        existe = Condominios.objects.filter(nome_condominio__iexact=nome_condominio).exists()
        return JsonResponse({'existe': existe})

@login_required
def adicionar_controleacesso(request):
    return render(request, 'adicionar_controleacesso.html')

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_apartamento')

    return JsonResponse({'apartamentos': list(apartamentos)})


@login_required
def get_pessoas_por_apartamento(request):
    apartamento_id = request.GET.get('apartamento_id')

    if apartamento_id:
        # Filtra as pessoas associadas ao apartamento
        pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)

        # Prepara os dados a serem retornados no formato JSON
        data = {
            'pessoas': [
                {
                    'id': pessoa.id,
                    'nome_pessoa': pessoa.nome_pessoa,
                    'tipo_pessoa': pessoa.tipos_pessoa.nome_tipos_pessoa,  # Acesso correto ao tipo de pessoa
                    'is_proprietario': pessoa.tipos_pessoa.nome_tipos_pessoa == 'Proprietário'
                    # Verifica se é 'Proprietário'
                }
                for pessoa in pessoas
            ]
        }
        return JsonResponse(data)

    # Caso o apartamento_id não seja fornecido
    return JsonResponse({'pessoas': []}, status=400)

@login_required
def carregar_apartamentos(request, condominio_id):
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    apartamentos_data = [{'id': ap.id, 'nome': ap.nome_apartamento} for ap in apartamentos]
    return JsonResponse({'apartamentos': apartamentos_data})

@login_required
def carregar_pessoas(request, apartamento_id):
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
    pessoas_data = [{'id': p.id, 'nome': p.nome_pessoa} for p in pessoas]
    return JsonResponse({'pessoas': pessoas_data})



@login_required
def get_apartamento_sindico(request):
    condominio_id = request.GET.get('condominio_id')
    sindicos = Sindicos.objects.filter(condominio_id=condominio_id)

    sindico_data = []  # Lista que vai conter os dados dos síndicos

    for sindico in sindicos:
        apartamento = sindico.pessoa.apartamento
        apartamento_nome = None
        tiposindico_nome = None

        # Acessa o tipo de síndico através do relacionamento
        tiposindico = sindico.tipos_sindico  # Aqui você já tem a instância do tipo de síndico

        # Se o tipo de síndico existir, pega o nome
        if tiposindico:
            tiposindico_nome = tiposindico.nome_tipos_sindico

        # Acessa o objeto Pessoa diretamente
        pessoa = sindico.pessoa  # Acessa o objeto Pessoa completo
        pessoa_nome = pessoa.nome_pessoa  # Agora acessa corretamente o nome da pessoa

        if apartamento:
            apartamento_nome = apartamento.nome_apartamento  # Pega o nome do apartamento

        # Adiciona os dados do síndico à lista
        sindico_data.append({
            'apartamento_nome': apartamento_nome,  # Nome do apartamento
            'pessoa_nome': pessoa_nome,  # Nome da pessoa (síndico)
            'tiposindico_nome': tiposindico_nome  # Nome do tipo de síndico
        })

    print(sindico_data)  # Para verificar os dados retornados
    # Retorna a lista como resposta JSON
    return JsonResponse({'sindicos': sindico_data})





@login_required
def carregar_sindicos(request, condominio_id):
    try:
        # Buscar os síndicos associados ao condomínio
        sindicos = Sindicos.objects.filter(condominio_id=condominio_id, status=1)  # Filtra por status ativo

        if sindicos.exists():
            # Se houver síndicos, retorna as informações
            sindico_data = []
            for sindico in sindicos:
                sindico_data.append({
                    'id': sindico.pessoa.id,  # ID da pessoa associada ao síndico
                    'nome_pessoa': sindico.pessoa.nome_pessoa  # Nome da pessoa
                })
            return JsonResponse({'sindicos': sindico_data})
        else:
            # Se não houver síndico, retorna None
            return JsonResponse({'sindicos': None})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_apartamentos(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    apartamentos_data = [{'id': apartamento.id, 'nome_apartamento': apartamento.nome_apartamento} for apartamento in apartamentos]
    return JsonResponse({'apartamentos': apartamentos_data})

def get_pessoas(request):
    apartamento_id = request.GET.get('apartamento_id')
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
    pessoas_data = [{'id': pessoa.id, 'nome_pessoa': pessoa.nome_pessoa} for pessoa in pessoas]
    return JsonResponse({'pessoas': pessoas_data})


# aqui iniciei outro teste

@login_required
def adicionar_controle_acesso_morador(request):
    condominios = Condominios.objects.filter(status=1)
    colaboradores = TatticaFuncionarios.objects.all()
    tipos_controles_acesso = TiposControlesAcessos.objects.all()

    apartamentos = []
    pessoas = []

    form = ControleAcessoMoradorForm()

    if request.method == 'POST':
        form = ControleAcessoMoradorForm(request.POST)

        if form.is_valid():

            controle = form.save(commit=False)
            # Define a data de criação se não preenchida
            if not controle.created:
                controle.created = now()
                print(f"Created preenchido com: {controle.created}")

            try:
                controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
                print(f"Data Prazo definida como: {controle.data_prazo}")
            except Exception as e:
                print(f"Erro ao calcular data_prazo: {e}")
                messages.error(request, "Erro ao calcular a data limite.")
                return render(request, 'adicionar_controle_acesso_morador.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'tipos_controles_acesso': tipos_controles_acesso,
                    'condominios': condominios,
                })
                # Salva o objeto no banco
            try:
                controle.save()
                print("Objeto salvo com sucesso!")
                messages.success(request, "Controle de acesso adicionado com sucesso!")
                return redirect('lista_controleacesso')  # Substitua pela URL corret
            except Exception as e:
                print(f"Erro ao salvar o formulário: {e}")

        else:
            print(f"Formulário inválido. Erros de validação detectados: {form.errors}")

        # Lógica de preenchimento dos campos, como antes
        condominio_id = request.POST.get('condominio')
        apartamento_id = request.POST.get('apartamento')

        if condominio_id:
            apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
            print(f"Condomínio selecionado: {condominio_id}")

            if apartamento_id:
                pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
                print(f"Apartamento selecionado: {apartamento_id}")

    return render(request, 'adicionar_controle_acesso_morador.html', {
        'form': form,
        'colaboradores': colaboradores,
        'tipos_controles_acesso': tipos_controles_acesso,
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
    })



@login_required
def adicionar_controle_acesso_sindico(request):
    """
    View para renderizar o template de controle de acesso do síndico.
    """
    return render(request, 'adicionar_controle_acesso_sindico.html')

@login_required
def adicionar_controle_acesso_funcionario_condominio(request):
    """
    View para renderizar o template de controle de acesso dos funcionários do condomínio.
    """
    return render(request, 'adicionar_controle_acesso_funcionario_condominio.html')

@login_required
def adicionar_controle_acesso_outros(request):
    """
    View para renderizar o template de controle de acesso para outras pessoas.
    """
    return render(request, 'adicionar_controle_acesso_outro.html')




@login_required
def lista_controleacesso(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    pedido = request.GET.get('pedido')
    status = request.GET.get('status')  # O campo status será crucial aqui
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os dados com base nos filtros selecionados
    controles = ControlesAcessos.objects.all()

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipos_controles_acesso_id=tipos)
    if execucao:
        controles = controles.filter(execucao=execucao)
    if pedido:
        controles = controles.filter(pedido=pedido)
    if data_inicio:
        controles = controles.filter(created__gte=data_inicio)
    if data_fim:
        controles = controles.filter(created__lte=data_fim)

    # Filtra status; padrão será mostrar apenas "pendentes" (status=1) caso não seja selecionado um status
    if status:
        print(status)
        controles = controles.filter(status=status)
    else:
        controles = controles.filter(status=1)  # Apenas pendentes por padrão

    # Verifica se há pendências
    pendencias_existentes = controles.filter(status=1).exists()

    # Para dropdowns de seleção
    condominios = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
    tipos_controles = TiposControlesAcessos.objects.filter(status=1)

    # Renderiza os dados no template
    context = {
        'pendencias_existentes': pendencias_existentes,
        'controles': controles,
        'condominios': condominios,
        'tipos_controles': tipos_controles,
    }
    return render(request, 'lista_controleacesso.html', context)


@login_required
def lista_controleacesso_pendente(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    pedido = request.GET.get('pedido')
    status = request.GET.get('status')  # O campo status será crucial aqui
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os dados com base nos filtros selecionados
    controles = ControlesAcessos.objects.all()

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipos_controles_acesso_id=tipos)
    if execucao:
        controles = controles.filter(execucao=execucao)
    if pedido:
        controles = controles.filter(pedido=pedido)
    if data_inicio:
        controles = controles.filter(created__gte=data_inicio)
    if data_fim:
        controles = controles.filter(created__lte=data_fim)

    # Filtra status; padrão será mostrar apenas "pendentes" (status=1) caso não seja selecionado um status
    if status:
        print(status)
        controles = controles.filter(status=status)
    else:
        controles = controles.filter(status=1)

    # Para dropdowns de seleção
    condominios = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
    tipos_controles = TiposControlesAcessos.objects.filter(status=1)

    # Renderiza os dados no template
    context = {
        'controles': controles,
        'condominios': condominios,
        'tipos_controles': tipos_controles,
    }
    return render(request, 'lista_controleacesso.html', context)
