from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from app.models import (ControlesAcessos, TatticaFuncionarios, TiposControlesAcessos, Condominios,
                        Apartamentos, Pessoas, Sindicos)
from django.http import JsonResponse
from controleacesso.forms import ControleAcessoForm
from django.utils.timezone import now  # Para exibir a data atual se necessário
from django.contrib import messages  # Para exibir mensagens ao usuário
from controleacesso.templatetags.custom_tags import adicionar_dias_uteis

@login_required
def adicionar_controleacesso(request):
    colaboradores = TatticaFuncionarios.objects.all()
    tipos_controles_acesso = TiposControlesAcessos.objects.all()
    condominios = Condominios.objects.all()

    if request.method == 'POST':
        form = ControleAcessoForm(request.POST)
        if form.is_valid():
            # Cria a instância sem salvar no banco
            instance = form.save(commit=False)

            # Define a data de criação se não preenchida
            if not instance.created:
                instance.created = now()
                print(f"Created preenchido com: {instance.created}")

            # Calcula a data de prazo (3 dias úteis após a criação)
            try:
                instance.data_prazo = adicionar_dias_uteis(instance.created, 3)
                print(f"Data Prazo definida como: {instance.data_prazo}")
            except Exception as e:
                print(f"Erro ao calcular data_prazo: {e}")
                messages.error(request, "Erro ao calcular a data limite.")
                return render(request, 'adicionar_controleacesso.html', {
                    'form': form,
                    'colaboradores': colaboradores,
                    'tipos_controles_acesso': tipos_controles_acesso,
                    'condominios': condominios,
                })

            # Salva o objeto no banco
            try:
                instance.save()
                print("Objeto salvo com sucesso!")
                messages.success(request, "Controle de acesso adicionado com sucesso!")
                return redirect('lista_controleacesso')  # Substitua pela URL correta
            except Exception as e:
                print(f"Erro ao salvar o objeto: {e}")
                messages.error(request, "Erro ao salvar controle de acesso.")
        else:
            # Debug para erros de formulário
            print(form.errors)
            messages.error(request, "Erro ao adicionar controle de acesso. Verifique os dados fornecidos.")
    else:
        form = ControleAcessoForm()

    return render(request, 'adicionar_controleacesso.html', {
        'form': form,
        'colaboradores': colaboradores,
        'tipos_controles_acesso': tipos_controles_acesso,
        'condominios': condominios,
    })

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_apartamento')

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

def carregar_apartamentos(request, condominio_id):
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    apartamentos_data = [{'id': ap.id, 'nome': ap.nome_apartamento} for ap in apartamentos]
    return JsonResponse({'apartamentos': apartamentos_data})

def carregar_pessoas(request, apartamento_id):
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
    pessoas_data = [{'id': p.id, 'nome': p.nome_pessoa} for p in pessoas]
    return JsonResponse({'pessoas': pessoas_data})

def carregar_sindicos(request, condominio_id):
    sindicos = Sindicos.objects.filter(condominio_id=condominio_id)
    sindicos_data = [{'id': s.id, 'nome': s.nome_sindico} for s in sindicos]
    return JsonResponse({'sindicos': sindicos_data})



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


