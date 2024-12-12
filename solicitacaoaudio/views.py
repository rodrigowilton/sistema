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


import logging

from solicitacaoaudio.forms import SolicitacaoAudioMoradorForm, SolicitacaoAudioSindicoForms, \
    SolicitacaoAudioFuncionarioForms, SolicitacaoAudioOutroForms

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível mínimo para capturar mensagens
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@login_required
def adicionar_solicitacaoaudio(request):
    return render(request, 'adicionar_solicitacaoaudio.html')

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
def adicionar_solicitacaoaudio_morador(request):
    condominios = Condominios.objects.filter(status=1)  # Condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores
    apartamentos = []
    pessoas = []

    if request.method == 'POST':
        print(request.POST)
        form = SolicitacaoAudioMoradorForm(request.POST)
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
                return render(request, 'adicionar_solicitacao_audio_morador.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'condominios': condominios,
                    'apartamentos': apartamentos,
                    'pessoas': pessoas,
                })

            # Salva a solicitação
            try:
                controle.save()
                messages.success(request, "Solicitação de áudio adicionada com sucesso!")
                return redirect('lista_solicitacaoaudio_pendente')  # Redireciona para a lista de controle de acesso
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
        form = SolicitacaoAudioMoradorForm()

    return render(request, 'adicionar_solicitacao_audio_morador.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
    })


@login_required
def adicionar_solicitacaoaudio_sindico(request):
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
        form = SolicitacaoAudioSindicoForms(request.POST)
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
                messages.success(request, 'Solicitação de áudio adicionado com sucesso!')
                return redirect('lista_solicitacaoaudio_pendente')
            except Exception as e:
                print(f"Erro ao salvar solicitação de áudio: {str(e)}")
                messages.error(request, f'Erro ao salvar Solicitação de áudio: {str(e)}')
        else:
            print("Formulário inválido. Erros:", form.errors)
            if form.errors.get('sindico'):
                messages.error(request, f"Erro no campo Síndico: {form.errors['sindico']}")
            if form.errors.get('condominio'):
                messages.error(request, f"Erro no campo Condomínio: {form.errors['condominio']}")
    else:
        form = SolicitacaoAudioSindicoForms()

    return render(request, 'adicionar_solicitacao_audio_sindico.html', {
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
def adicionar_solicitacaoaudio_funcionario_condominio(request):
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

        form = SolicitacaoAudioFuncionarioForms(request.POST)
        if form.is_valid():
            try:
                controle = form.save(commit=False)
                controle.created = timezone.now()  # Define a data de criação
                controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
                print(f"Data Prazo definida como: {controle.data_prazo}")

                # Salva o controle de acesso no banco
                controle.save()
                messages.success(request, 'Solicitação de áudio adicionado com sucesso!')
                return redirect('lista_solicitacaoaudio_pendente')  # Redireciona para a lista de controles de acesso
            except Exception as e:
                print(f"Erro ao salvar Solicitação de áudio: {e}")
                messages.error(request, "Erro ao salvar Solicitação de áudio.")
        else:
            print("Erros no formulário:", form.errors)
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = SolicitacaoAudioFuncionarioForms()

    return render(request, 'adicionar_solicitacao_audio_funcionario_condominio.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
        'funcionarios': funcionarios,  # Passa os funcionários filtrados para o template
    })


@login_required
def adicionar_solicitacaoaudio_outros(request):
    # Filtra os dados necessários
    condominios = Condominios.objects.filter(status=1)  # Filtra condomínios ativos
    colaboradores = TatticaFuncionarios.objects.all()  # Todos os colaboradores

    if request.method == 'POST':
        print("Dados recebidos via POST:", request.POST)  # Log de depuração
        form = SolicitacaoAudioOutroForms(request.POST)

        if form.is_valid():
            print("Formulário válido.")
            area_sindico = form.cleaned_data.get('area_sindico', 0)


            try:
                controle = form.save(commit=False)
                controle.created = timezone.now()  # Define a data de criação
                controle.data_prazo = adicionar_dias_uteis(controle.created, 3)
                print(f"Data Prazo definida como: {controle.data_prazo}")

                # Valida o campo 'outros' como solicitante
                solicitante = request.POST.get('outros', '').strip()
                if solicitante:
                    controle.solicitante = solicitante
                else:
                    messages.error(request, "O campo 'Outros' é obrigatório quando não há funcionário associado.")
                    return render(request, 'adicionar_solicitacao_audio_outros.html', {
                        'form': form,
                        'colaboradores': colaboradores,
                        'condominios': condominios,
                    })

                # Salva o objeto no banco de dados
                controle.save()
                messages.success(request, 'Solicitação de áudio adicionada com sucesso!')
                return redirect('lista_solicitacaoaudio_pendente')  # Ajuste conforme sua URL correta

            except Exception as e:
                print(f"Erro ao salvar no banco de dados: {e}")
                messages.error(request, "Ocorreu um erro ao salvar a solicitação. Tente novamente.")
                return render(request, 'adicionar_solicitacao_audio_outros.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'condominios': condominios,
                })
        else:
            print("Formulário inválido. Erros:", form.errors)
            messages.error(request, "Existem erros no formulário. Por favor, corrija-os.")

    else:
        form = SolicitacaoAudioOutroForms()
        print("Formulário inicializado para GET.")

    return render(request, 'adicionar_solicitacao_audio_outros.html', {
        'form': form,
        'colaboradores': colaboradores,
        'condominios': condominios,
    })

@login_required
def lista_solicitacaoaudio(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    pedido = request.GET.get('pedido')
    status = request.GET.get('status')  # O campo status será crucial aqui
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os dados com base nos filtros selecionados
    controles = Imagemcameras.objects.filter(tipo_gravacao=2)

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipo_gravacao=2)
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
    tipo_gravacao = Imagemcameras.objects.filter(tipo_gravacao=2)

    # Renderiza os dados no template
    context = {
        'pendencias_existentes': pendencias_existentes,
        'controles': controles,
        'condominios': condominios,
        'tipo_gravacao': tipo_gravacao,
    }
    return render(request, 'lista_solicitacaoaudio.html', context)

@login_required
def lista_solicitacaoaudio_pendente(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')  # Filtro de status
    aprovacao = request.GET.get('aprovacao')  # Filtro de aprovação

    # Filtra os dados com base nos filtros selecionados
    controles = Imagemcameras.objects.filter(tipo_gravacao=2)

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipo_gravacao=2)
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
    tipo_gravacao = Imagemcameras.objects.filter(tipo_gravacao=2)

    messages.warning(request, "Atenção! Existem pendências que precisam ser resolvidas.")

    # Renderiza os dados no template
    context = {
        'controles': controles,
        'condominios': condominios,
        'tipo_gravacao': tipo_gravacao,
    }
    return render(request, 'lista_solicitacaoaudio.html', context)

