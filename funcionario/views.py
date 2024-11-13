from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from app.models import Funcionarios, CondominiosFuncionarios, Condominios
from .forms import FuncionarioForm

@login_required
def lista_funcionarios(request):
    funcionarios = CondominiosFuncionarios.objects.select_related('tipos_condominios_funcionario', 'condominio').all()
    return render(request, 'lista_funcionarios.html', {'funcionarios': funcionarios})

@login_required
def verificar_condominio_existe(request):
    if request.method == 'GET':
        nome_condominio = request.GET.get('nome_condominio', '').strip()
        existe = Condominios.objects.filter(nome_condominio__iexact=nome_condominio).exists()
        return JsonResponse({'existe': existe})


@login_required
def adicionar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários após adicionar
    else:
        form = FuncionarioForm()
    
    return render(request, 'adicionar_funcionario.html', {'form': form})


@login_required
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionarios, id=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'editar_funcionario.html', {'form': form, 'funcionario': funcionario})

@login_required
def deletar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionarios, id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('lista_funcionarios')
    return render(request, 'deletar_funcionario.html', {'funcionario': funcionario})
