from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EmpresaForm
from app.models import Empresas, EmpresasServicosEmpresas, EmpresasServicos


@login_required
def lista_empresas(request):
    search_query = request.GET.get('searchbar', '').strip()

    if search_query:
        empresas = Empresas.objects.filter(status=1, nome_fantasia__icontains=search_query).prefetch_related(
            'empresasservicosempresas_set__empresas_servico'
        )
    else:
        empresas = Empresas.objects.filter(status=1).prefetch_related(
            'empresasservicosempresas_set__empresas_servico'
        )

    empresas_context = []
    for empresa in empresas:
        servicos = empresa.empresasservicosempresas_set.all()
        nomes_servicos = ", ".join([s.empresas_servico.nome_tipos_empresa for s in servicos])

        empresas_context.append({
            'empresa': empresa,
            'servicos': nomes_servicos,
        })

    # Verificação manual se a requisição é AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'empresas': empresas_context})

    context = {
        'empresas_context': empresas_context,
    }
    return render(request, 'lista_empresas.html', context)


def adicionar_empresa(request):
    empresas_servicos = EmpresasServicos.objects.filter(status=1)

    if request.method == 'POST':
        form = EmpresaForm(request.POST)

        # Depuração: Exibe os dados recebidos no POST
        print("Dados recebidos no POST:", request.POST)

        if form.is_valid():
            # Depuração: Verifica os dados do formulário antes de salvar
            print("Formulário válido, salvando dados...")
            empresa = form.save()

            # Depuração: Confirmação de que a empresa foi salva
            print("Empresa salva com sucesso:", empresa)

            messages.success(request, 'Empresa adicionada com sucesso!')
            return redirect('lista_empresas')
        else:
            # Depuração: Exibe os erros do formulário
            print("Erros no formulário:", form.errors)
    else:
        form = EmpresaForm()

    return render(request, 'adicionar_empresa.html', {'form': form, 'empresas_servicos': empresas_servicos})

@login_required
def editar_empresas(request, pk):
    # Buscar a empresa existente pelo pk fornecido
    empresa = get_object_or_404(Empresas, pk=pk)

    # Obter os serviços disponíveis para a empresa
    empresas_servicos = EmpresasServicos.objects.filter(status=1)

    # Preencher o formulário com os dados da empresa
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)  # Preenche o formulário com os dados da empresa

        # Depuração: Exibe os dados recebidos no POST
        print("Dados recebidos no POST:", request.POST)

        if form.is_valid():
            # Depuração: Verifica os dados do formulário antes de salvar
            print("Formulário válido, salvando dados...")

            # Salva os dados atualizados da empresa
            empresa = form.save()

            # Depuração: Confirmação de que a empresa foi salva
            print("Empresa salva com sucesso:", empresa)

            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('lista_empresas')
        else:
            # Depuração: Exibe os erros do formulário
            print("Erros no formulário:", form.errors)
    else:
        form = EmpresaForm(instance=empresa)  # Preenche o formulário com os dados existentes da empresa

    context = {
        'form': form,
        'empresa': empresa,  # Passa a empresa para o template
        'empresas_servicos': empresas_servicos  # Passa os serviços disponíveis para a empresa
    }

    return render(request, 'editar_empresas.html', context)



def deletar_empresas(request, pk):
    empresa = get_object_or_404(Empresas, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa deletada com sucesso!')
        return redirect('lista_empresas')
    return render(request, 'deletar_empresas.html', {'empresa': empresa})
