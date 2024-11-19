from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models import EmpresasServicos
from .forms import EmpresasServicosForm

# Listar os serviços
def lista_servicoempresa(request):
    servicos = EmpresasServicos.objects.all()
    return render(request, 'lista_servicoempresa.html', {'servicos': servicos})

# Criar um serviço
def criar_servicoempresa(request):
    if request.method == 'POST':
        form = EmpresasServicosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço criado com sucesso!')
            return redirect('lista_servicoempresa')
    else:
        form = EmpresasServicosForm()
    return render(request, 'criar_servicoempresa.html', {'form': form})

# Editar um serviço
def editar_servicoempresa(request, pk):
    servico = get_object_or_404(EmpresasServicos, pk=pk)
    if request.method == 'POST':
        form = EmpresasServicosForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('lista_servicoempresa')
    else:
        form = EmpresasServicosForm(instance=servico)
    return render(request, 'editar_servicoempresa.html', {'form': form, 'servico': servico})

# Deletar um serviço
def deletar_servicoempresa(request, pk):
    servico = get_object_or_404(EmpresasServicos, pk=pk)
    if request.method == 'POST':
        servico.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
        return redirect('lista_servicoempresa')
    return render(request, 'deletar_servicoempresa.html', {'servico': servico})
