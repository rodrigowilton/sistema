from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models import (EmpresasServicosEmpresas, EmpresasServicos, Empresas, Condominios,
                        PrestadoresAcessos, Funcionarios,CondominiosFuncionarios)
from django.http import JsonResponse
import logging


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


logger = logging.getLogger(__name__)


def adicionar_prestador(request):
    if request.method == 'POST':
        try:
            condominio_id = request.POST.get('condominio')
            servico_id = request.POST.get('servico')
            empresa_id = request.POST.get('empresa')
            funcionario_id = request.POST.get('funcionario')

            if not (condominio_id and servico_id and empresa_id and funcionario_id):
                raise ValueError("Todos os campos são obrigatórios!")

            # Recuperando os objetos necessários
            condominio = get_object_or_404(Condominios, pk=condominio_id)
            servico = get_object_or_404(EmpresasServicos, pk=servico_id)
            empresa = get_object_or_404(Empresas, pk=empresa_id)
            funcionario = get_object_or_404(Funcionarios, pk=funcionario_id)

            # Selecionar o primeiro registro encontrado, sem validações adicionais
            empresas_servicos_empresa = EmpresasServicosEmpresas.objects.filter(
                empresa=empresa,
                empresas_servico=servico
            ).first()

            # Criar o registro de prestador
            prestador_acesso = PrestadoresAcessos.objects.create(
                condominio=condominio,
                empresas_servicos_empresa=empresas_servicos_empresa,
                funcionario=funcionario,
                status=1  # Define o status padrão como ativo
            )

            messages.success(request, "Prestador adicionado com sucesso!")
            return redirect('lista_prestadores')

        except Exception as e:
            messages.error(request, f"Erro ao adicionar prestador: {e}")
            return redirect('adicionar_prestador')

    # Renderizando o formulário de adição
    condominios = Condominios.objects.filter(status=1)
    servicos = EmpresasServicos.objects.filter(status=1)
    empresas = Empresas.objects.filter(status=1)
    funcionarios = Funcionarios.objects.filter(status=1)

    return render(request, 'adicionar_prestador.html', {
        'condominios': condominios,
        'servicos': servicos,
        'empresas': empresas,
        'funcionarios': funcionarios,
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
    prestador = get_object_or_404(PrestadoresAcessos, pk=pk)

    if request.method == 'POST':
        try:
            # Recuperando os dados do formulário
            condominio_id = request.POST.get('condominio')
            empresa_id = request.POST.get('empresa')
            servico_id = request.POST.get('servico')
            funcionario_id = request.POST.get('funcionario')

            # Validando se todos os campos foram preenchidos
            if not (condominio_id and empresa_id and servico_id and funcionario_id):
                raise ValueError("Todos os campos são obrigatórios!")

            # Atualizando os relacionamentos
            prestador.condominio = get_object_or_404(Condominios, pk=condominio_id)

            # Busca a empresa vinculada ao serviço
            empresas_servicos_empresa = EmpresasServicosEmpresas.objects.filter(
                empresa_id=empresa_id,
                empresas_servico_id=servico_id
            ).first()

            if not empresas_servicos_empresa:
                raise ValueError("Não foi possível encontrar a relação entre empresa e serviço selecionados!")

            prestador.empresas_servicos_empresa = empresas_servicos_empresa
            prestador.funcionario = get_object_or_404(Funcionarios, pk=funcionario_id)

            # Salvando as alterações no prestador
            prestador.save()

            messages.success(request, "Prestador atualizado com sucesso!")
            return redirect('lista_prestadores')

        except Exception as e:
            messages.error(request, f"Erro ao atualizar prestador: {e}")
            return redirect('editar_prestador', pk=pk)

    # Carregando dados para o formulário de edição
    condominios = Condominios.objects.filter(status=1)
    empresas = Empresas.objects.filter(status=1)
    servicos = EmpresasServicos.objects.filter(status=1)
    funcionarios = Funcionarios.objects.filter(status=1)

    # Passando os dados de prestador para o template
    return render(request, 'editar_prestador.html', {
        'prestador': prestador,
        'condominios': condominios,
        'empresas': empresas,
        'servicos': servicos,
        'funcionarios': funcionarios,
    })


def deletar_prestador(request, pk):
    """Deleta um prestador."""
    prestador = get_object_or_404(EmpresasServicosEmpresas, pk=pk)
    try:
        prestador.delete()
        messages.success(request, "Prestador deletado com sucesso!")
    except ProtectedError:
        messages.error(request, "Não é possível deletar este prestador pois ele está vinculado a outras entidades.")
    return redirect('lista_prestadores')
