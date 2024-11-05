from django.shortcuts import render, get_object_or_404, redirect
from app.models import AgendamentoHorarios, Areas, Condominios, Agendamentos
from .forms import AgendamentoHorariosForm, AgendamentoForm
from django.db.models import Q

def adicionar_horario_agendamento(request):
    condominios = Condominios.objects.filter(status=1)  # Obtém os condomínios ativos
    areas = []  # Inicializa a lista de áreas

    # Verifica se um condomínio foi selecionado
    condominio_id = request.POST.get('condominio') or request.GET.get('condominio_id')
    if condominio_id:
        areas = Areas.objects.filter(condominio_id=condominio_id)  # Filtra áreas pelo condomínio

    if request.method == 'POST':
        form = AgendamentoHorariosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamento_horarios')
    else:
        form = AgendamentoHorariosForm()

    return render(request, 'adicionar_horario_agendamento.html', {
        'form': form,
        'condominios': condominios,
        'areas': areas,
        'selected_condominio': condominio_id,  # Passa o condomínio selecionado para o template
    })


def editar_horario_agendamento(request, id):
    agendamento = get_object_or_404(Agendamentos, id=id)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamento_horarios')  # Redireciona após salvar
    else:
        form = AgendamentoForm(instance=agendamento)

    condominios = Condominios.objects.filter(status=1)  # Filtra os condomínios ativos
    areas = Areas.objects.all()  # Ajuste conforme sua lógica de áreas

    return render(request, 'editar_horario_agendamento.html', {
        'form': form,
        'condominios': condominios,
        'areas': areas,
    })


def deletar_horario_agendamento(request, id):
    agendamento = get_object_or_404(AgendamentoHorarios, id=id)

    if request.method == 'POST':
        agendamento.delete()
        return redirect('listar_agendamento_horarios')

    return render(request, 'deletar_horario_agendamento.html', {'agendamento': agendamento})


def listar_agendamento_horarios(request):
    search_query = request.GET.get('search', '')  # Captura o termo de busca do campo 'search'

    # Realiza o filtro apenas se o termo de busca for fornecido
    agendamentos = AgendamentoHorarios.objects.all()
    if search_query:
        agendamentos = agendamentos.filter(
            Q(condominio__nome_condominio__icontains=search_query) |  # Nome do condomínio
            Q(area__nome_area__icontains=search_query)  # Nome da área
        )

    context = {
        'agendamentos': agendamentos,
        'search_query': search_query  # Passa o termo de busca para o template
    }
    return render(request, 'horarioagendamento.html', context)
