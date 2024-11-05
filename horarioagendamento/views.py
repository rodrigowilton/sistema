from django.shortcuts import render, get_object_or_404, redirect
from app.models import AgendamentoHorarios
from .forms import AgendamentoHorariosForm  # Supondo que um formulário tenha sido criado para este modelo


def adicionar_horario_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoHorariosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamento_horarios')
    else:
        form = AgendamentoHorariosForm()

    return render(request, 'adicionar_horario_agendamento.html', {'form': form})


def editar_horario_agendamento(request, id):
    agendamento = get_object_or_404(AgendamentoHorarios, id=id)

    if request.method == 'POST':
        form = AgendamentoHorariosForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamento_horarios')
    else:
        form = AgendamentoHorariosForm(instance=agendamento)

    return render(request, 'editar_horario_agendamento.html', {'form': form, 'agendamento': agendamento})


def deletar_horario_agendamento(request, id):
    agendamento = get_object_or_404(AgendamentoHorarios, id=id)

    if request.method == 'POST':
        agendamento.delete()
        return redirect('listar_agendamento_horarios')

    return render(request, 'deletar_horario_agendamento.html', {'agendamento': agendamento})


def listar_agendamento_horarios(request):
    agendamentos = AgendamentoHorarios.objects.all()
    return render(request, 'horarioagendamento.html', {'agendamentos': agendamentos})
