from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CondominiumForm
from app.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# CREATE
@login_required
def criar_condominio(request):
    if request.method == 'POST':
        form = CondominiumForm(request.POST)
        if form.is_valid():
            # Aqui você pode salvar os dados ou fazer algo com eles
            return redirect('create_condominio')  # Redirecione para a página desejada após o salvamento
    else:
        form = CondominiumForm()

    return render(request, 'create_condominio.html', {'form': form})


# READ (List and Detail)
@login_required
def list_condominios(request):
    condominios = Condominios.objects.all()
    return render(request, 'list_condominios.html', {'condominios': condominios})


@login_required
def detail_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    return render(request, 'detail_condominio.html', {'condominio': condominio})


# UPDATE
@login_required
def update_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    if request.method == 'POST':
        form = CondominioForm(request.POST, instance=condominio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Condomínio atualizado com sucesso!')
            return redirect('list_condominios')
    else:
        form = CondominioForm(instance=condominio)

    return render(request, 'update_condominio.html', {'form': form})


# DELETE
@login_required
def delete_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    if request.method == 'POST':
        condominio.delete()
        messages.success(request, 'Condomínio excluído com sucesso!')
        return redirect('list_condominios')
    return render(request, 'delete_condominio.html', {'condominio': condominio})


@login_required
def redirect_based_on_group(request):
    # Verifica se o usuário pertence ao grupo "Diretoria"
    if request.user.groups.filter(name='Diretoria').exists():
        return redirect('home')  # Redireciona para home
    else:
        return redirect('menu_adm')  # Redireciona para menu_adm


@login_required
def menu_adm(request):
    if request.user.has_perm('app.change_condominios'):
        try:
            condominios = Condominios.objects.all()
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
    return render(request, 'menu_add.html')

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
