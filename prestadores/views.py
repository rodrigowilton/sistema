from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models import (EmpresasServicosEmpresas, EmpresasServicos, Empresas, Condominios,
                        PrestadoresAcessos, Funcionarios,CondominiosFuncionarios)

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

        empresa = get_object_or_404(Empresas, pk=empresa_id)
        servico = get_object_or_404(EmpresasServicos, pk=servico_id)
        condominio = get_object_or_404(Condominios, pk=condominio_id)

        prestador = EmpresasServicosEmpresas(
            empresa=empresa,
            empresas_servico=servico,
            status=1  # Ativo por padrão
        )
        prestador.save()
        messages.success(request, "Prestador adicionado com sucesso!")
        return redirect('lista_prestadores')

    empresas = Empresas.objects.filter(status=1)
    servicos = EmpresasServicos.objects.filter(status=1)
    condominios = Condominios.objects.filter(status=1)
    return render(request, 'adicionar_prestador.html',
                  {'empresas': empresas, 'servicos': servicos, 'condominios': condominios})


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
