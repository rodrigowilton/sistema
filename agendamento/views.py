# Em views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import AgendamentoForm
from django.core.paginator import Paginator
from django.db.models import Q
from app.models import Agendamentos, Condominios, Apartamentos
from datetime import datetime

def lista_agendamento(request):
    # Filtros obtidos da requisição GET
    filtros = {
        'condominio': request.GET.get('condominio', 'Todos'),  # Ajuste para o campo condominio
        'apartamento': request.GET.get('apartamento', 'Todos'),
        'adm': request.GET.get('adm', 'Todos'),
        'mudanca': request.GET.get('mudanca', 'Todos'),
        'zelador': request.GET.get('zelador', 'Todos'),
        'status': request.GET.get('status', 'Todos'),
        'data_inicio': request.GET.get('data_inicio', ''),
        'data_fim': request.GET.get('data_fim', ''),
    }

    # Lista de condomínios com status ativo
    condominios = Condominios.objects.filter(status=1)

    # Filtra apartamentos baseados no condomínio selecionado (se aplicável)
    if filtros['condominio'] != 'Todos':
        apartamentos = Apartamentos.objects.filter(condominio_id=filtros['condominio'])
    else:
        apartamentos = Apartamentos.objects.all()

    # Aplica os filtros nos agendamentos
    agendamentos = Agendamentos.objects.all()
    if filtros['condominio'] != 'Todos':
        agendamentos = agendamentos.filter(condominio_id=filtros['condominio'])
    if filtros['apartamento'] != 'Todos':
        agendamentos = agendamentos.filter(apartamento_id=filtros['apartamento'])
    if filtros['adm'] != 'Todos':
        agendamentos = agendamentos.filter(adm=filtros['adm'])
    if filtros['mudanca'] != 'Todos':
        agendamentos = agendamentos.filter(mudanca=filtros['mudanca'])
    if filtros['zelador'] != 'Todos':
        agendamentos = agendamentos.filter(zelador=filtros['zelador'])
    if filtros['status'] != 'Todos':
        agendamentos = agendamentos.filter(status=filtros['status'])
    if filtros['data_inicio']:
        agendamentos = agendamentos.filter(data_inicio__gte=filtros['data_inicio'])
    if filtros['data_fim']:
        agendamentos = agendamentos.filter(data_fim__lte=filtros['data_fim'])

    # Paginação
    paginator = Paginator(agendamentos, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderiza o template com os dados e filtros aplicados
    return render(request, 'lista_agendamento.html', {
        'page_obj': page_obj,
        'filtros': filtros,
        'condominios': condominios,
        'apartamentos': apartamentos
    })


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
