from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models import (EmpresasServicosEmpresas, EmpresasServicos, Empresas, Condominios,
                        PrestadoresAcessos, Funcionarios,CondominiosFuncionarios)
from django.http import JsonResponse


def lista_prestadores(request):
    # Certificando-se de que as relações estão sendo acessadas corretamente.
    prestadores = PrestadoresAcessos.objects.select_related(
        'condominio',  # Relaciona o Condomínio
        'empresas_servicos_empresa',  # Relaciona a Empresa
        'empresas_servicos_empresa__empresas_servico',  # Relaciona o Serviço
        'funcionario'  # Relaciona o Funcionário
    ).all()

    return render(request, 'lista_prestadores.html', {
        'prestadores': prestadores,
    })


def adicionar_prestador(request):
    """Adiciona um novo prestador."""
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        servico_id = request.POST.get('servico')
        condominio_id = request.POST.get('condominio')

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not empresa_id or not servico_id or not condominio_id:
            messages.error(request, "Todos os campos devem ser preenchidos.")
            return redirect('adicionar_prestador')

        try:
            # Tenta obter os objetos correspondentes
            empresa = get_object_or_404(Empresas, pk=empresa_id)
            servico = get_object_or_404(EmpresasServicos, pk=servico_id)
            condominio = get_object_or_404(Condominios, pk=condominio_id)

            # Imprime para depuração
            print(f"Empresa: {empresa}, Serviço: {servico}, Condomínio: {condominio}")

        except Exception as e:
            # Caso ocorra algum erro ao buscar os dados
            messages.error(request, f"Ocorreu um erro ao buscar os dados: {e}")
            return redirect('adicionar_prestador')

        try:
            # Cria o prestador e tenta salvar
            prestador = EmpresasServicosEmpresas(
                empresa=empresa,
                empresas_servico=servico,
                status=1  # Ativo por padrão
            )
            prestador.save()

            # Imprime para depuração
            print(f"Prestador {prestador} criado com sucesso!")

            messages.success(request, "Prestador adicionado com sucesso!")

        except Exception as e:
            # Caso ocorra algum erro ao salvar
            messages.error(request, f"Ocorreu um erro ao salvar o prestador: {e}")
            return redirect('adicionar_prestador')

        # Imprime para depuração
        print("Redirecionando para a lista de prestadores.")

        return redirect('lista_prestadores')  # Redireciona para a lista de prestadores

    # Preenche as opções de empresas, serviços e condomínios para o formulário
    empresas = Empresas.objects.filter(status=1)
    servicos = EmpresasServicos.objects.filter(status=1)
    condominios = Condominios.objects.filter(status=1)

    return render(request, 'adicionar_prestador.html', {
        'empresas': empresas,
        'servicos': servicos,
        'condominios': condominios
    })

def carregar_empresas_por_servico(request):
    """Carrega as empresas relacionadas a um serviço selecionado."""
    servico_id = request.GET.get('servico_id')

    # Filtrando as empresas relacionadas ao serviço selecionado através da tabela intermediária
    empresas = Empresas.objects.filter(empresasservicosempresas__empresas_servico__id=servico_id, status=1)

    # Criando a lista de empresas para retornar no JsonResponse
    empresa_list = [{'id': empresa.id, 'nome_fantasia': empresa.nome_fantasia} for empresa in empresas]

    return JsonResponse({'empresas': empresa_list})

def carregar_funcionarios_por_empresa(request):
    """Carrega os funcionários relacionados a uma empresa selecionada."""
    empresa_id = request.GET.get('empresa_id')
    funcionarios = Funcionarios.objects.filter(empresa_id=empresa_id, status=1)
    funcionario_list = [{'id': funcionario.id, 'nome_funcionario': funcionario.nome_funcionario} for funcionario in funcionarios]
    return JsonResponse({'funcionarios': funcionario_list})


def editar_prestador(request, pk):
    """Edita os dados de um prestador."""
    prestador = get_object_or_404(EmpresasServicosEmpresas, pk=pk)

    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        servico_id = request.POST.get('servico')
        condominio_id = request.POST.get('condominio')

        prestador.empresa = get_object_or_404(Empresas, pk=empresa_id)
        prestador.empresas_servico = get_object_or_404(EmpresasServicos, pk=servico_id)
        prestador.save()

        messages.success(request, "Prestador atualizado com sucesso!")
        return redirect('lista_prestadores')

    empresas = Empresas.objects.filter(status=1)
    servicos = EmpresasServicos.objects.filter(status=1)
    condominios = Condominios.objects.filter(status=1)
    return render(request, 'editar_prestador.html',
                  {'prestador': prestador, 'empresas': empresas, 'servicos': servicos, 'condominios': condominios})


def deletar_prestador(request, pk):
    """Deleta um prestador."""
    prestador = get_object_or_404(EmpresasServicosEmpresas, pk=pk)
    try:
        prestador.delete()
        messages.success(request, "Prestador deletado com sucesso!")
    except ProtectedError:
        messages.error(request, "Não é possível deletar este prestador pois ele está vinculado a outras entidades.")
    return redirect('lista_prestadores')
