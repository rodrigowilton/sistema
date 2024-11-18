from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Empresas
from .forms import EmpresaForm

def lista_empresas(request):
    empresas = Empresas.objects.all()
    return render(request, 'lista_empresas.html', {'empresas': empresas})

def adicionar_empresas(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa adicionada com sucesso!')
            return redirect('lista_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'adicionar_empresas.html', {'form': form})

def editar_empresas(request, pk):
    empresa = get_object_or_404(Empresas, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('lista_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'editar_empresas.html', {'form': form})

def deletar_empresas(request, pk):
    empresa = get_object_or_404(Empresas, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa deletada com sucesso!')
        return redirect('lista_empresas')
    return render(request, 'deletar_empresas.html', {'empresa': empresa})
