# Em views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import AgendamentoForm
from django.core.paginator import Paginator
from django.db.models import Q
from app.models import Agendamentos, Condominios, Apartamentos
from datetime import datetime


def lista_agendamento(request):
    # Coleta os valores dos filtros do formulário
    condominio_id = request.GET.get('condominio')
    apartamento_id = request.GET.get('apartamento')
    adm = request.GET.get('adm')
    zelador = request.GET.get('zelador')
    status = request.GET.get('status')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    mudanca = request.GET.get('mudanca')

    # Dicionário para mapear os valores do status
    STATUS_CHOICES = {
        1: 'Agendado',
        2: 'Concluído',
        3: 'Cancelado',
        4: 'Pendente',
    }

    # Obtém o mês e ano atuais
    hoje = datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month

    # Inicializa a queryset com todos os agendamentos
    agendamentos = Agendamentos.objects.all()

    # Aplica o filtro para mostrar apenas os agendamentos do mês atual
    agendamentos = agendamentos.filter(data_inicio__year=ano_atual, data_inicio__month=mes_atual)

    # Aplica filtros adicionais de acordo com os parâmetros preenchidos
    if condominio_id and condominio_id != "Todos":
        agendamentos = agendamentos.filter(condominio_id=condominio_id)
    if apartamento_id and apartamento_id != "Todos":
        agendamentos = agendamentos.filter(apartamento_id=apartamento_id)
    if adm and adm != "Todos":
        agendamentos = agendamentos.filter(adm=adm)
    if zelador and zelador != "Todos":
        agendamentos = agendamentos.filter(zelador=zelador)
    if status and status != "Todos":
        agendamentos = agendamentos.filter(status=status)
    if data_inicio:
        agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_fim__lte=data_fim)
    if mudanca and mudanca != "Todos":
        agendamentos = agendamentos.filter(mudanca=mudanca)

    # Ordena os agendamentos por data de criação
    agendamentos = agendamentos.order_by('created')

    # Aplica a conversão do status para o nome legível
    for agendamento in agendamentos:
        agendamento.status_display = STATUS_CHOICES.get(agendamento.status, 'Desconhecido')

    # Paginação com 10 agendamentos por página
    paginator = Paginator(agendamentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dados para os campos de filtro (exibidos no dropdown)
    condominios = Condominios.objects.all()
    apartamentos = Apartamentos.objects.all()

    context = {
        'page_obj': page_obj,
        'total_agendamentos': agendamentos.count(),
        'condominios': condominios,
        'apartamentos': apartamentos,
        'filters': {
            'condominio_id': condominio_id,
            'apartamento_id': apartamento_id,
            'adm': adm,
            'zelador': zelador,
            'status': status,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'mudanca': mudanca
        }
    }
    return render(request, 'lista_agendamento.html', context)

def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_agendamento')
    else:
        form = AgendamentoForm()
    return render(request, 'criar_agendamento.html', {'form': form})

def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamentos, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('lista_agendamento')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'criar_agendamento.html', {'form': form})

def deletar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamentos, pk=pk)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('lista_agendamento')
    return render(request, 'deletar_agendamento.html', {'agendamento': agendamento})
