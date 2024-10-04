from django.shortcuts import render, get_object_or_404, redirect
from .models import Condominios
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import AuthUser, AuthGroup, AuthPermission, AuthUserGroups, AuthUserUserPermissions, AuthGroupPermissions
from django.contrib.auth.decorators import login_required

from django.utils.translation import gettext as _

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validação das senhas
        if password != confirm_password:
            messages.error(request, _("As senhas não coincidem."))
            return redirect('register')

        # Verifica se o nome de usuário já está em uso
        if User.objects.filter(username=username).exists():
            messages.error(request, _("O nome de usuário já está em uso."))
            return redirect('register')

        # Verifica se o email já está em uso
        if User.objects.filter(email=email).exists():
            messages.error(request, _("O email já está em uso."))
            return redirect('register')

        try:
            # Cria o usuário
            user = User.objects.create_user(username=username, email=email, password=password)

            # Adiciona o usuário ao grupo, se necessário (opcional)
            # user_group = request.POST.get('user_group')  # Caso você tenha um campo para grupos
            # if user_group:
            #     group = Group.objects.get(name=user_group)
            #     user.groups.add(group)

            messages.success(request, _("Cadastro realizado com sucesso. Você pode fazer login agora."))
            return redirect('configuracao')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('register')

    return render(request, 'register.html')



# views.py

from django.shortcuts import render, redirect
from .models import AuthUser, AuthPermission, AuthUserUserPermissions
from django.contrib import messages

def lista_autenticacao(request):
    users = AuthUser.objects.all()
    permissions = AuthPermission.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        permission_id = request.POST.get('permission_id')
        action = request.POST.get('action')

        user = AuthUser.objects.get(id=user_id)
        permission = AuthPermission.objects.get(id=permission_id)

        if action == 'add':
            # Adiciona a permissão ao usuário se não existir
            user_perm, created = AuthUserUserPermissions.objects.get_or_create(user=user, permission=permission)
            if created:
                messages.success(request, f"Permissão '{permission.name}' adicionada ao usuário '{user.username}'.")
            else:
                messages.warning(request, f"O usuário '{user.username}' já possui a permissão '{permission.name}'.")

        elif action == 'remove':
            # Remove a permissão do usuário se existir
            deleted, _ = AuthUserUserPermissions.objects.filter(user=user, permission=permission).delete()
            if deleted:
                messages.success(request, f"Permissão '{permission.name}' removida do usuário '{user.username}'.")
            else:
                messages.warning(request, f"O usuário '{user.username}' não possui a permissão '{permission.name}'.")

        return redirect('lista_autenticacao')  # Redireciona após a ação

    # Captura as permissões atribuídas aos usuários
    user_permissions = AuthUserUserPermissions.objects.select_related('permission').all()

    return render(request, 'lista_autenticacao.html', {
        'users': users,
        'permissions': permissions,
        'user_permissions': user_permissions,
    })

@login_required
def home(request):
    # Verifica se o usuário tem a permissão 'severus.can_change_condominios'
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
        return render(request, 'home.html', context)
    else:
        return render(request, 'sem_permissao.html')  # Renderiza uma página de erro de permissão


def configuracao(request):
    return render(request, 'configuracao.html')

def editar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para editar o condomínio aqui
    return render(request, 'editar_condominio.html', {'condominio': condominio})

def consultar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para consultar o condomínio aqui
    return render(request, 'consultar_condominio.html', {'condominio': condominio})

def excluir_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)

    if request.method == 'POST':
        condominio.delete()
        messages.success(request, 'Condomínio excluído com sucesso!')
        return redirect('home')  # Redireciona para a página inicial após a exclusão

    return render(request, 'confirmar_exclusao.html', {'condominio': condominio})
