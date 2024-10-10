from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from app.models import *

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
