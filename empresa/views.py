from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EmpresaForm
from app.models import Empresas, EmpresasServicosEmpresas


@login_required
def lista_empresas(request):
    # Busca todas as empresas ativas e seus serviços associados
    empresas = Empresas.objects.filter(status=1).prefetch_related(
        'empresasservicosempresas_set__empresas_servico'
    )

    # Organiza as informações em um contexto
    empresas_context = []
    for empresa in empresas:
        # Lista de serviços associados à empresa
        servicos = empresa.empresasservicosempresas_set.all()
        nomes_servicos = ", ".join([s.empresas_servico.nome_tipos_empresa for s in servicos])

        empresas_context.append({
            'empresa': empresa,
            'servicos': nomes_servicos,
        })

    context = {
        'empresas_context': empresas_context,
    }
    return render(request, 'lista_empresas.html', context)


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
