from datetime import timedelta
from msilib.schema import ProgId

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET
from app.models import (ControlesAcessos, TatticaFuncionarios, TiposControlesAcessos, Condominios,
                        Apartamentos, Pessoas, Sindicos, CondominiosFuncionarios, Imagemcameras)
from django.http import JsonResponse
from django.utils.timezone import now  # Para exibir a data atual se necessário
from django.contrib import messages  # Para exibir mensagens ao usuário
from controleacesso.templatetags.custom_tags import adicionar_dias_uteis, dias_uteis_mais
from controleacesso.forms import (ControleAcessoMoradorForm, ControleAcessoSindicoForms,
                                  ControleAcessoFuncionarioForms, ControleAcessoOutroForms)

import logging

from solicitacaoimagem.forms import SolicitacaoImagemMoradorForm, SolicitacaoImagemSindicoForms, \
    SolicitacaoImagemFuncionarioForms

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível mínimo para capturar mensagens
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@login_required
def adicionar_solicitacaoimagem(request):
    return render(request, 'adicionar_solicitacaoimagem.html')

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_apartamento')

    return JsonResponse({'apartamentos': list(apartamentos)})

@login_required
@require_GET
def get_sindicos_por_condominio(request, condominio_id):
    if request.method == "GET":
        # Filtrar os síndicos pelo condomínio selecionado
        sindicos = Sindicos.objects.filter(condominio_id=condominio_id, status=1).select_related('pessoa', 'tipos_sindico')

        print(sindicos)

        # Retornar os dados como JSON
        data = [
            {
                "id": sindico.id,
                "nome_pessoa": sindico.pessoa.nome_pessoa,
                "tipo_sindico": sindico.tipos_sindico.nome_tipos_sindico,
            }
            for sindico in sindicos
        ]
        return JsonResponse(data, safe=False)

@login_required
def get_apartamentos(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    apartamentos_data = [{'id': apartamento.id, 'nome_apartamento': apartamento.nome_apartamento} for apartamento in apartamentos]
    return JsonResponse({'apartamentos': apartamentos_data})

@login_required
def get_pessoas(request):
    apartamento_id = request.GET.get('apartamento_id')
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
    pessoas_data = [{'id': pessoa.id, 'nome_pessoa': pessoa.nome_pessoa} for pessoa in pessoas]
    return JsonResponse({'pessoas': pessoas_data})


@login_required
def adicionar_solicitacaoimagem_morador(request):
    condominios = Condominios.objects.filter(status=1)  # Condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores
    apartamentos = []
    pessoas = []

    if request.method == 'POST':
        print(request.POST)
        form = SolicitacaoImagemMoradorForm(request.POST)
        print(form)
        if form.is_valid():
            controle = form.save(commit=False)
            controle.created = now()  # Define a data de criação como agora
            area_sindico = form.cleaned_data.get('area_sindico', 0)

            # Calcula a data limite de prazo
            try:
                controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
            except Exception as e:
                messages.error(request, f"Erro ao calcular a data limite: {e}")
                return render(request, 'adicionar_solicitacao_imagem_morador.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'condominios': condominios,
                    'apartamentos': apartamentos,
                    'pessoas': pessoas,
                })

            # Salva a solicitação
            try:
                controle.save()
                messages.success(request, "Solicitação de imagem adicionada com sucesso!")
                return redirect('lista_solicitacaoimagem_pendente')  # Redireciona para a lista de controle de acesso
            except Exception as e:
                messages.error(request, f"Erro ao salvar a solicitação: {e}")
        else:
            # Adiciona mensagens de erro específicas para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")

            messages.error(request, "Erro ao validar o formulário. Por favor, revise os dados.")

        # Filtra os apartamentos e pessoas para a exibição dinâmica
        condominio_id = request.POST.get('condominio')
        apartamento_id = request.POST.get('apartamento_id')

        if condominio_id:
            apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1)
            if apartamento_id:
                pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id, status=1)
    else:
        form = SolicitacaoImagemMoradorForm()

    return render(request, 'adicionar_solicitacao_imagem_morador.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
    })


@login_required
def adicionar_solicitacaoimagem_sindico(request):
    condominios = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores

    sindicos = Sindicos.objects.none()  # Default: nenhum síndico
    condominio_id = request.GET.get('condominio', None)

    if condominio_id:
        try:
            # Filtrar síndicos pelo condomínio
            sindicos = Sindicos.objects.filter(
                condominio_id=condominio_id,
                tipos_sindico_id__isnull=False,  # Síndicos com tipo definido
                pessoa_id__isnull=False  # Síndicos vinculados a uma pessoa
            ).select_related('pessoa')  # Otimização para reduzir consultas

            print(f"Síndicos filtrados para condomínio {condominio_id}:")
            for sindico in sindicos:
                print(f"ID: {sindico.id}, Nome: {sindico.pessoa.nome_pessoa}")

        except (ValueError, TypeError) as e:
            print(f"Erro ao filtrar síndicos: {str(e)}")
            messages.error(request, "ID de condomínio inválido.")

    if request.method == 'POST':
        form = SolicitacaoImagemSindicoForms(request.POST)
        sindico_id = request.POST.get('sindico')
        print("ID do síndico enviado no formulário:", sindico_id)

        if form.is_valid():
            print(form)
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
            try:
                print("Formulário válido. Dados do formulário:", form.cleaned_data)
                form.save()
                messages.success(request, 'Solicitação de imagem adicionado com sucesso!')
                return redirect('lista_solicitacaoimagem_pendente')
            except Exception as e:
                print(f"Erro ao salvar controle de acesso: {str(e)}")
                messages.error(request, f'Erro ao salvar Solicitação de imagem: {str(e)}')
        else:
            print("Formulário inválido. Erros:", form.errors)
            if form.errors.get('sindico'):
                messages.error(request, f"Erro no campo Síndico: {form.errors['sindico']}")
            if form.errors.get('condominio'):
                messages.error(request, f"Erro no campo Condomínio: {form.errors['condominio']}")
    else:
        form = SolicitacaoImagemSindicoForms()

    return render(request, 'adicionar_solicitacao_imagem_sindico.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'sindicos': sindicos,  # Passando os síndicos filtrados para o template
    })



@require_GET
def carregar_funcionarios(request):
    condominio_id = request.GET.get('condominio_id')
    try:
        # Ajuste esta consulta conforme a estrutura exata dos seus modelos
        funcionarios = TatticaFuncionarios.objects.filter(
            condominio_id=condominio_id
        ).values('id', 'nome_funcionario')

        return JsonResponse(list(funcionarios), safe=False)

    except Exception as e:
        # Log the error
        logger.error(f"Erro ao carregar funcionários: {e}")
        return JsonResponse([], safe=False)


@login_required
@require_GET
def carregar_funcionarios_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    try:
        funcionarios = CondominiosFuncionarios.objects.filter(
            condominio_id=condominio_id
        ).select_related('tipos_condominios_funcionario').values(
            'id',
            'nome_condominios_funcionario',
            'tipos_condominios_funcionario__nome_tipo_funcionario'  # Inclui o nome do tipo de funcionário
        )

        data = [
            {
                'id': funcionario['id'],
                'nome_funcionario': f"{funcionario['nome_condominios_funcionario']} ({funcionario['tipos_condominios_funcionario__nome_tipo_funcionario']})"
            }
            for funcionario in funcionarios
        ]

        return JsonResponse(data, safe=False)

    except Exception as e:
        logger.error(f"Erro ao carregar funcionários: {e}")
        return JsonResponse([], safe=False)



@login_required
def adicionar_solicitacaoimagem_funcionario_condominio(request):
    """View para adicionar controle de acesso vinculado a um funcionário e condomínio."""
    condominios = Condominios.objects.filter(status=1)  # Filtra condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores
    funcionarios = CondominiosFuncionarios.objects.none()  # Inicialmente nenhum funcionário é exibido

    # Verifica se um condomínio foi selecionado para filtrar funcionários
    condominio_id = request.GET.get('condominio', None)
    if condominio_id:
        try:
            # Filtra funcionários relacionados ao condomínio selecionado
            funcionarios = CondominiosFuncionarios.objects.filter(
                condominio_id=condominio_id,
                status=1  # Apenas funcionários ativos
            )
        except Exception as e:
            print(f"Erro ao filtrar funcionários: {e}")
            messages.error(request, "Erro ao carregar os funcionários deste condomínio.")

    # Processamento do formulário
    if request.method == 'POST':
        print("Dados enviados no POST:", request.POST)

        form = SolicitacaoImagemFuncionarioForms(request.POST)
        if form.is_valid():
            try:
                controle = form.save(commit=False)
                controle.created = timezone.now()  # Define a data de criação
                controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
                print(f"Data Prazo definida como: {controle.data_prazo}")

                # Salva o controle de acesso no banco
                controle.save()
                messages.success(request, 'Controle de acesso adicionado com sucesso!')
                return redirect('lista_solicitacaoimagem_pendente')  # Redireciona para a lista de controles de acesso
            except Exception as e:
                print(f"Erro ao salvar controle de acesso: {e}")
                messages.error(request, "Erro ao salvar o controle de acesso.")
        else:
            print("Erros no formulário:", form.errors)
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = SolicitacaoImagemFuncionarioForms()

    return render(request, 'adicionar_solicitacao_imagem_funcionario_condominio.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'funcionarios': funcionarios,  # Passa os funcionários filtrados para o template
    })


@login_required
def adicionar_controle_acesso_outros(request):
    condominios = Condominios.objects.filter(status=1)  # Filtra condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores
    tipos_controles_acesso = TiposControlesAcessos.objects.all()  # Todos os tipos de controle de acesso

    if request.method == 'POST':
        form = ControleAcessoOutroForms(request.POST)
        if form.is_valid():
            controle = form.save(commit=False)
            controle.created = timezone.now()  # Define a data de criação
            controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
            print(f"Data Prazo definida como: {controle.data_prazo}")
            tipo_gravacao = Imagemcameras.tipo_gravacao

            # Define o solicitante com o valor do campo manual
            solicitante = request.POST.get('outros', '').strip()
            if solicitante:
                controle.solicitante = solicitante
            else:
                messages.error(request, "O campo 'Outros' é obrigatório quando não há funcionário associado.")
                return render(request, 'controle_acesso_outros_form.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'condominios': condominios,
                    'tipo_gravacao': tipo_gravacao,
                })

            controle.save()
            messages.success(request, "Controle de acesso adicionado com sucesso!")
            return redirect('lista_controleacesso')  # Ajuste para sua URL correta
    else:
        form = ControleAcessoOutroForms()
        tipo_gravacao = Imagemcameras.tipo_gravacao

    return render(request, 'adicionar_controle_acesso_outros.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'tipo_gravacao': tipo_gravacao,
    })



@login_required
def lista_solicitacaoimagem(request):
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
        controles = controles.filter(tipo_gravacao=tipos)
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
    tipo_gravacao = Imagemcameras.objects.all()

    # Renderiza os dados no template
    context = {
        'pendencias_existentes': pendencias_existentes,
        'controles': controles,
        'condominios': condominios,
        'tipo_gravacao': tipo_gravacao,
    }
    return render(request, 'lista_solicitacaoimagem.html', context)

@login_required
def lista_solicitacaoimagem_pendente(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')  # Filtro de status
    aprovacao = request.GET.get('aprovacao')  # Filtro de aprovação

    # Filtra os dados com base nos filtros selecionados
    controles = Imagemcameras.objects.all()

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipo_gravacao=tipos)
    if execucao:
        controles = controles.filter(execucao=execucao)
    if data_inicio:
        controles = controles.filter(created__gte=data_inicio)
    if data_fim:
        controles = controles.filter(created__lte=data_fim)
    if status:
        controles = controles.filter(status=status)
    else:
        controles = controles.filter(status=1)
    if aprovacao:
        controles = controles.filter(aprovacao=aprovacao)
    else:
        controles = controles.filter(aprovacao=1)

    # Para dropdowns de seleção
    condominios = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
    tipo_gravacao = Imagemcameras.objects.all()

    messages.warning(request, "Atenção! Existem pendências que precisam ser resolvidas.")

    # Renderiza os dados no template
    context = {
        'controles': controles,
        'condominios': condominios,
        'tipo_gravacao': tipo_gravacao,
    }
    return render(request, 'lista_solicitacaoimagem.html', context)

