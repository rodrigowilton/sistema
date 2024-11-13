from django.shortcuts import render, get_object_or_404, redirect
from app.models import Funcionarios, CondominiosFuncionarios
from .forms import FuncionarioForm

def lista_funcionarios(request):
    funcionarios = CondominiosFuncionarios.objects.select_related('tipos_condominios_funcionario', 'condominio').all()
    return render(request, 'lista_funcionarios.html', {'funcionarios': funcionarios})



def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionarios, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('lista_funcionarios')  # Redireciona de volta para a lista de funcionários
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'editar_funcionario.html', {'form': form, 'funcionario': funcionario})

def deletar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionarios, id=id)  # Busca o funcionário pelo ID

    if request.method == 'POST':
        funcionario.delete()  # Deleta o funcionário
        return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários

    return render(request, 'deletar_funcionario.html', {'funcionario': funcionario})