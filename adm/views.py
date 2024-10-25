from .forms import CondominiosForm
from app.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def verificar_condominio_existe(request):
    if request.method == 'GET':
        nome_condominio = request.GET.get('nome_condominio', '').strip()
        existe = Condominios.objects.filter(nome_condominio__iexact=nome_condominio).exists()
        return JsonResponse({'existe': existe})


# CREATE
@login_required
def criar_condominio(request):
    if request.method == 'POST':
        form = CondominiosForm(request.POST)
        if form.is_valid():
            print("Formulário válido!")
            condominio = form.save()  # Salva imediatamente, pois o status já é definido no formulário
            messages.success(request, 'Cadastro criado com sucesso!')

            return redirect('menu_adm')  # Redireciona para a página desejada após o salvamento
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = CondominiosForm()

    return render(request, 'create_condominio.html', {'form': form})


# READ (List and Detail)
@login_required
def list_condominios(request):
    condominios = Condominios.objects.filter(status=1)  # Filtra apenas os condomínios com status=1
    #condominios = Condominios.objects.all()
    return render(request, 'list_condominios.html', {'condominios': condominios})


@login_required
def editar_condominio(request, id):
    condominio = get_object_or_404(Condominios, pk=id)  # Obtém o condomínio pelo ID

    if request.method == 'POST':
        form = CondominiosForm(request.POST, instance=condominio)  # Passa a instância existente
        if form.is_valid():
            form.save()  # Salva as alterações
            return redirect('menu_adm')  # Redireciona após o salvamento
    else:
        form = CondominiosForm(instance=condominio)  # Carrega o formulário com os dados existentes

    return render(request, 'editar_condominio.html', {'form': form})  # Verifique o caminho aqui

# UPDATE

@login_required
def delete_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)

    if request.method == 'POST':
        condominio.status = 0  # Alterar o status para 0 (inativo)
        condominio.save()  # Salvar as alterações no banco de dados
        messages.success(request, 'Condomínio desativado com sucesso!')
        return redirect('home')  # Redireciona para a lista de condomínios

    return render(request, 'delete_condominio.html', {'condominio': condominio})


@login_required
def redirect_based_on_group(request):
    # Verifica se o usuário pertence ao grupo "Diretoria"
    if request.user.groups.filter(name='Diretoria').exists():
        return redirect('home')  # Redireciona para home
    else:
        return redirect('menu_adm')  # Redireciona para menu_adm

@login_required
def consulta_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    return render(request, 'consultacondominio.html', {'condominio': condominio})

@login_required
def menu_adm(request):
    if request.user.has_perm('app.change_condominios'):
        try:
            condominios = Condominios.objects.filter(status=1)  # Filtra apenas os condomínios com status=1
            #condominios = Condominios.objects.all()
        except Exception as e:
            print(f"Erro ao buscar condomínios: {e}")
            condominios = []

        # Captura os usuários e permissões para o template
        users = AuthUser.objects.all()
        permissions = AuthPermission.objects.all()

        # Captura as permissões atribuídas aos usuários
        user_permissions = []

        for user in users:
            user_perms = user.authuseruserpermissions_set.all()
            for user_perm in user_perms:
                user_permissions.append(user_perm)

        context = {
            'condominios': condominios,
            'users': users,
            'permissions': permissions,
            'user_permissions': user_permissions,
        }
        return render(request, 'menu_adm.html', context)
    else:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('configuracao')


@login_required
def menu_add(request):
    if request.user.has_perm('app.change_condominios'):
        try:
            condominios = Condominios.objects.filter(status=1)  # Filtra apenas os condomínios com status=1
            #condominios = Condominios.objects.all()  # Captura todos os condomínios
        except Exception as e:
            print(f"Erro ao buscar condomínios: {e}")
            condominios = []  # Em caso de erro, define condomínios como uma lista vazia

        # Captura os usuários e permissões para o template
        users = AuthUser.objects.all()
        permissions = AuthPermission.objects.all()

        # Captura as permissões atribuídas aos usuários
        user_permissions = []
        for user in users:
            user_perms = user.authuseruserpermissions_set.all()
            user_permissions.extend(user_perms)  # Usando extend para simplificar

        # Define o contexto a ser passado para o template
        context = {
            'condominios': condominios,
            'users': users,
            'permissions': permissions,
            'user_permissions': user_permissions,
        }
        return render(request, 'menu_add.html', context)  # Passando o contexto
    else:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('menu_adm')


@login_required
def menu_ctr(request):
    return render(request, 'menu_ctr.html')


@login_required
def menu_agd(request):
    return render(request, 'menu_agd.html')


@login_required
def menu_srv(request):
    return render(request, 'menu_srv.html')

@login_required
def menu_slc(request):
    return render(request, 'menu_slc.html')


@login_required
def menu_ocr(request):
    return render(request, 'menu_ocr.html')

@login_required
def menu_tel(request):
    return render(request, 'menu_tel.html')

@login_required
def menu_inf(request):
    return render(request, 'menu_inf.html')
