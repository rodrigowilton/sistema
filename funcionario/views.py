from django.shortcuts import render, get_object_or_404, redirect
from app.models import Funcionarios
from django.core.paginator import Paginator
from .forms import FuncionarioForm


def list_funcionarios(request):
	funcionarios = Funcionarios.objects.filter(status=1).select_related('empresa', 'tipos_funcionario')
	
	paginator = Paginator(funcionarios, 20)  # Exibe 20 funcionários por página
	page_number = request.GET.get('page')  # Pega o número da página atual
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'lista_funcionarios.html', {'page_obj': page_obj})

from .forms import FuncionarioForm  # Supondo que você tenha um formulário para o modelo Funcionarios

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