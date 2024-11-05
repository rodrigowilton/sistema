from django.shortcuts import render, get_object_or_404, redirect
from app.models import AgendamentoHorarios, Areas, Condominios, Agendamentos
from .forms import AgendamentoHorariosForm, AgendamentoForm
from django.db.models import Q

def adicionar_horario_agendamento(request):
    # Obtém os condomínios ativos
    condominios = Condominios.objects.filter(status=1)
    areas = []  # Inicializa a lista de áreas vazia

    # Verifica se um condomínio foi selecionado
    condominio_id = request.POST.get('condominio') or request.GET.get('condominio_id')
    if condominio_id:
        areas = Areas.objects.filter(condominio_id=condominio_id)  # Filtra áreas pelo condomínio selecionado

    if request.method == 'POST':
        form = AgendamentoHorariosForm(request.POST)
        if form.is_valid():
            # Cria o agendamento com commit=False para definir o status manualmente
            agendamento = form.save(commit=False)
            agendamento.status = 1  # Define o status como 1
            agendamento.save()  # Salva o agendamento no banco
            return redirect('listar_agendamento_horarios')
        else:
            print("Formulário inválido:", form.errors)  # Log de erro para depuração
    else:
        form = AgendamentoHorariosForm()

    # Renderiza o template com o formulário e dados do condomínio/área
    return render(request, 'adicionar_horario_agendamento.html', {
        'form': form,
        'condominios': condominios,
        'areas': areas,
        'selected_condominio': condominio_id,  # Passa o condomínio selecionado para o template
    })


def editar_horario_agendamento(request, id):
    agendamento = get_object_or_404(AgendamentoHorarios, id=id)
    condominios = Condominios.objects.filter(status=1)  # Filtra os condomínios ativos
    areas = Areas.objects.filter(condominio=agendamento.condominio)  # Filtra áreas pelo condomínio do agendamento

    if request.method == 'POST':
        form = AgendamentoHorariosForm(request.POST)

        # Atribui a área recebida do formulário ao agendamento
        area_id = request.POST.get('area')
        agendamento.area = get_object_or_404(Areas, id=area_id)  # Obtém a área com base no ID recebido

        if form.is_valid():
            agendamento.horario_inicio = form.cleaned_data['horario_inicio']
            agendamento.horario_fim = form.cleaned_data['horario_fim']
            agendamento.status = 1  # Define o status como 1
            agendamento.save()  # Salva o agendamento com a área e horários atualizados

            return redirect('listar_agendamento_horarios')  # Redireciona após salvar
    else:
        form = AgendamentoHorariosForm(instance=agendamento)

    return render(request, 'editar_horario_agendamento.html', {
        'form': form,
        'condominios': condominios,
        'areas': areas,
        'agendamento': agendamento,  # Passa o agendamento para o template
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
            Q(area__nome_area__icontains=search_query) |  # Filtra pelo nome da área
            Q(condominio__nome_condominio__icontains=search_query)  # Filtra pelo nome do condomínio
        )

    context = {
        'agendamentos': agendamentos,
        'search_query': search_query  # Passa o termo de busca para o template
    }
    return render(request, 'horarioagendamento.html', context)
