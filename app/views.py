from django.shortcuts import render, get_object_or_404, redirect
from .models import Condominios
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .models import AuthUser, AuthGroup, AuthPermission, AuthUserGroups, AuthUserUserPermissions, AuthGroupPermissions
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Atualize o caminho conforme necessário

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Verifica se o usuário pertence ao grupo "Administrativo"
        if user.groups.filter(name='Administrativo').exists():
            return redirect('menu_adm')  # Redireciona para o menu de administração
        elif user.groups.filter(name='Supervisor T.I').exists():
            return redirect('home')  # Redireciona para a página inicial ou outra página desejada
        elif user.groups.filter(name='Diretoria').exists():
            return redirect('home')  # Redireciona para a página inicial ou outra página desejada

        # Adiciona uma mensagem de erro se o usuário não pertencer a nenhum dos grupos
        messages.error(self.request, "Você não tem acesso à área administrativa.")
        return redirect('/accounts/login/')  # Redireciona para a página de login


@login_required
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


@login_required
def manage_groups(request):
    if request.method == 'POST':
        # Ações para adicionar ou editar grupo
        if 'group_name' in request.POST:
            group_name = request.POST['group_name']
            permissions_ids = request.POST.getlist('permissions')

            # Adicionar ou atualizar o grupo
            group, created = AuthGroup.objects.get_or_create(name=group_name)
            group.save()
            group.authgrouppermissions_set.set(permissions_ids)  # Associar permissões ao grupo
            messages.success(request, f'Grupo "{group_name}" {"criado" if created else "atualizado"} com sucesso!')

        elif 'action' in request.POST and request.POST['action'] == 'delete':
            group_id = request.POST['group_id']
            group = get_object_or_404(AuthGroup, id=group_id)
            group.delete()
            messages.success(request, f'Grupo "{group.name}" removido com sucesso!')

        return redirect('manage_groups')

    # Exibir grupos e permissões
    groups = AuthGroup.objects.all().prefetch_related('authgrouppermissions_set')
    permissions = AuthPermission.objects.all()
    return render(request, 'manage_groups.html', {
        'groups': groups,
        'permissions': permissions,
    })


@login_required
def edit_group_permissions(request, group_id):
    group = get_object_or_404(AuthGroup, id=group_id)
    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')

        # Converter os IDs para instâncias de AuthGroupPermissions
        permissions = AuthGroupPermissions.objects.filter(id__in=permission_ids)

        # Atualizar permissões do grupo
        group.authgrouppermissions_set.set(permissions)

        messages.success(request, 'Permissões atualizadas com sucesso!')
        return redirect('manage_groups')


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(AuthGroup, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Grupo removido com sucesso!')

    return redirect('manage_groups')


@login_required
def manage_users_groups_permissions(request):
    users = User.objects.all()
    groups = Group.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        action = request.POST.get('action')

        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=group_id)

            if action == 'add_group':
                user.groups.add(group)
                messages.success(request, f'{user.username} foi adicionado ao grupo {group.name}.')

            elif action == 'remove_group':
                user.groups.remove(group)
                messages.success(request, f'{user.username} foi removido do grupo {group.name}.')

        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        except Group.DoesNotExist:
            messages.error(request, 'Grupo não encontrado.')

    return render(request, 'gerenciar_usuarios.html', {
        'users': users,
        'groups': groups,
    })


@login_required
def lista_autenticacao(request):
    users = AuthUser.objects.all()
    permissions = AuthPermission.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        permission_id = request.POST.get('permission_id')
        action = request.POST.get('action')

        user = AuthUser.objects.get(id=user_id)
        permission = AuthPermission.objects.get(id=permission_id)

        # Aplicar as traduções ao nome da permissão
        permission_name = PERMISSION_TRANSLATIONS.get(permission.codename, permission.name)

        if action == 'add':
            # Adiciona a permissão ao utilizador se não existir
            user_perm, created = AuthUserUserPermissions.objects.get_or_create(user=user, permission=permission)
            if created:
                messages.success(request, f"Permissão '{permission_name}' adicionada ao utilizador '{user.username}'.")
            else:
                messages.warning(request, f"O utilizador '{user.username}' já possui a permissão '{permission_name}'.")

        elif action == 'remove':
            # Remove a permissão do utilizador se existir
            deleted, _ = AuthUserUserPermissions.objects.filter(user=user, permission=permission).delete()
            if deleted:
                messages.success(request, f"Permissão '{permission_name}' removida do utilizador '{user.username}'.")
            else:
                messages.warning(request, f"O utilizador '{user.username}' não possui a permissão '{permission_name}'.")

        return redirect('lista_autenticacao')  # Redireciona após a ação

    # Captura as permissões atribuídas aos utilizadores
    user_permissions = AuthUserUserPermissions.objects.select_related('permission').all()

    # Aplica a tradução às permissões que são renderizadas
    permissions_traduzidas = []
    for permission in permissions:
        permissions_traduzidas.append({
            'id': permission.id,
            'name': PERMISSION_TRANSLATIONS.get(permission.codename, permission.name),
        })

    return render(request, 'lista_autenticacao.html', {
        'users': users,
        'permissions': permissions_traduzidas,
        'user_permissions': user_permissions,
    })


@login_required
def home(request):
    # Verifica se o usuário tem a permissão 'app.change_condominios'
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
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('configuracao')


@login_required
def configuracao(request):
    return render(request, 'configuracao.html')


@login_required
def editar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para editar o condomínio aqui
    return render(request, 'editar_condominio.html', {'condominio': condominio})


@login_required
def consultar_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)
    # Lógica para consultar o condomínio aqui
    return render(request, 'consultar_condominio.html', {'condominio': condominio})


@login_required
def excluir_condominio(request, id):
    condominio = get_object_or_404(Condominios, id=id)

    if request.method == 'POST':
        condominio.delete()
        messages.success(request, 'Condomínio excluído com sucesso!')
        return redirect('home')  # Redireciona para a página inicial após a exclusão

    return render(request, 'confirmar_exclusao.html', {'condominio': condominio})
