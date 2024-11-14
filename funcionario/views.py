from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from app.models import Funcionarios, CondominiosFuncionarios, Condominios, TiposFuncionarios
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
    # Filtra todos os condomínios com status = 1
    condominios = Condominios.objects.filter(status=1)
    tipos_funcionario = TiposFuncionarios.objects.all()

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()  # Salva os dados do formulário
            return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários
    else:
        form = FuncionarioForm()  # Cria um formulário vazio para GET

    # Passa os condomínios, tipos de funcionários e o formulário para o template
    return render(request, 'adicionar_funcionario.html', {'form': form, 'condominios': condominios, 'tipos_funcionario': tipos_funcionario})


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
