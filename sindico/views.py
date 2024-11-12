from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SindicoForm
from app.models import Sindicos, Apartamentos, Pessoas, TiposSindicos
from django.contrib import messages

@login_required
def lista_sindicos(request):
    sindicos = Sindicos.objects.filter(status=1, condominio__status=1).order_by('condominio__nome_condominio')
    return render(request, 'lista_sindicos.html', {'sindicos': sindicos})

def criar_sindico(request):
    if request.method == 'POST':
        form = SindicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico criado com sucesso.')
            return redirect('lista_sindicos')
    else:
        form = SindicoForm()
    return render(request, 'criar_sindico.html', {'form': form})


def editar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)

    # Obtendo os dados necessários para os dropdowns
    apartamentos = Apartamentos.objects.filter(condominio=sindico.condominio)
    pessoas = Pessoas.objects.all()
    tipos_sindico = TiposSindicos.objects.all()

    if request.method == 'POST':
        form = SindicoForm(request.POST, instance=sindico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico atualizado com sucesso.')
            return redirect('lista_sindicos')
    else:
        form = SindicoForm(instance=sindico)

    # Passando os dados de apartamentos, pessoas e tipos de síndico para o template
    return render(request, 'editar_sindico.html', {
        'form': form,
        'sindico': sindico,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
        'tipos_sindico': tipos_sindico
    })

def deletar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)
    sindico.delete()
    messages.success(request, 'Síndico deletado com sucesso.')
    return redirect('lista_sindicos')
from django.shortcuts import render

# Create your views here.
