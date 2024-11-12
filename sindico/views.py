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
    # Obtendo o síndico pelo ID
    sindico = get_object_or_404(Sindicos, id=sindico_id)

    # Filtrando os apartamentos que pertencem ao mesmo condomínio e que têm moradores
    apartamentos = Apartamentos.objects.filter(
        condominio=sindico.condominio,
        pessoas__isnull=False  # Filtra apartamentos que têm pelo menos uma pessoa
    ).distinct()

    # Filtrando as pessoas que moram no mesmo apartamento da pessoa associada ao síndico
    moradores_apartamento = Pessoas.objects.filter(apartamento=sindico.pessoa.apartamento) if sindico.pessoa else Pessoas.objects.none()

    # Obtendo os tipos de síndico para o dropdown
    tipos_sindico = TiposSindicos.objects.all()

    if request.method == 'POST':
        form = SindicoForm(request.POST, instance=sindico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico atualizado com sucesso.')
            return redirect('lista_sindicos')
    else:
        form = SindicoForm(instance=sindico)

    # Passando os dados para o template
    return render(request, 'editar_sindico.html', {
        'form': form,
        'sindico': sindico,
        'apartamentos': apartamentos,  # Apenas apartamentos povoados
        'pessoas': moradores_apartamento,  # Apenas moradores do apartamento do síndico
        'tipos_sindico': tipos_sindico,
    })


def deletar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)
    sindico.delete()
    messages.success(request, 'Síndico deletado com sucesso.')
    return redirect('lista_sindicos')
from django.shortcuts import render

# Create your views here.
