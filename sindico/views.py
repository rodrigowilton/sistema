from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Sindicos
from .forms import SindicoForm


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
    if request.method == 'POST':
        form = SindicoForm(request.POST, instance=sindico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico atualizado com sucesso.')
            return redirect('lista_sindicos')
    else:
        form = SindicoForm(instance=sindico)
    return render(request, 'editar_sindico.html', {'form': form, 'sindico': sindico})

def deletar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)
    sindico.delete()
    messages.success(request, 'Síndico deletado com sucesso.')
    return redirect('lista_sindicos')
from django.shortcuts import render

# Create your views here.
