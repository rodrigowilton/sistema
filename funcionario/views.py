from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from app.models import Funcionarios, CondominiosFuncionarios, Condominios, TiposFuncionarios
from .forms import FuncionarioForm
from django.http import HttpResponse
from django.utils.timezone import now


@login_required
def lista_funcionarios(request):
    try:
        funcionarios = CondominiosFuncionarios.objects.select_related('tipos_condominios_funcionario', 'condominio').all()
        return render(request, 'lista_funcionarios.html', {'funcionarios': funcionarios})
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao carregar a lista de funcionários: {str(e)}")
        return redirect('home')  # Redireciona para uma página de fallback

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
            funcionario = form.save(commit=False)  # Cria a instância, mas não salva ainda
            funcionario.created = now()  # Define o valor para o campo "created"
            form.save()  # Salva os dados do formulário
            messages.success(request, "Cadastro realizado com sucesso.")
            return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários
        else:
            messages.error(request, "Ocorreu um erro ao tentar cadastrar o funcionário. Verifique os campos.")

    else:
        form = FuncionarioForm()  # Cria um formulário vazio para GET

    # Passa os condomínios, tipos de funcionários e o formulário para o template
    return render(request, 'adicionar_funcionario.html',
                  {'form': form, 'condominios': condominios, 'tipos_funcionario': tipos_funcionario})


@login_required
def editar_funcionario(request, id):
    # Busca a instância do funcionário pelo ID
    funcionario = get_object_or_404(CondominiosFuncionarios, pk=id)
    print(f"Editando funcionário ID: {id}, Dados atuais: {funcionario}")  # Debug: Mostra informações do funcionário

    if request.method == "POST":
        print("POST Data:", request.POST)  # Debug: mostra os dados enviados no POST

        # Passa a instância do funcionário para o formulário
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            try:
                funcionario = form.save(commit=False)  # Cria a instância, mas não salva ainda
                funcionario.modified = now()  # Define a data e hora atual no campo "modified"
                funcionario.save()  # Salva as alterações no banco
                print("Funcionário atualizado com sucesso:", funcionario)  # Debug: Confirma o salvamento
                messages.success(request, "Funcionário atualizado com sucesso.")
                return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários
            except Exception as e:
                print("Erro ao salvar funcionário:", e)  # Debug: Mostra o erro no console
                messages.error(request, f"Erro ao salvar funcionário: {str(e)}")
                return redirect('editar_funcionario', id=id)
        else:
            print("Erros no formulário:", form.errors)  # Debug: Mostra os erros do formulário
            messages.error(request, "Erro no formulário. Verifique os campos preenchidos.")

    else:
        # Preenche o formulário com os dados do funcionário para GET
        form = FuncionarioForm(instance=funcionario)
        print("GET - Dados carregados no formulário:", form.initial)  # Debug: Mostra os dados carregados no form

    # Renderiza a página de edição com o formulário preenchido
    return render(request, 'editar_funcionario.html', {'form': form, 'funcionario': funcionario})


@login_required
def deletar_funcionario(request, id):
    funcionario = get_object_or_404(CondominiosFuncionarios, id=id)  # Aqui o id está correto

    if request.method == 'POST':
        funcionario.status = 0
        funcionario.save()
        messages.success(request, "Funcionário desativado com sucesso.")
        return redirect('lista_funcionarios')  # Redireciona para a lista de funcionários


    return render(request, 'deletar_funcionario.html', {'funcionario': funcionario})
