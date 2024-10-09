from django.shortcuts import render, get_object_or_404, redirect
from .models import Condominios
from django.contrib.auth.models import User, Group
from .models import AuthUser, AuthGroup, AuthPermission, AuthUserGroups, AuthUserUserPermissions, AuthGroupPermissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group as AuthGroup, Permission



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


def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        permission_ids = request.POST.getlist('permissions')

        # Criação do novo grupo
        if group_name:
            new_group = Group.objects.create(name=group_name)
            new_group.permissions.set(permission_ids)  # Define as permissões selecionadas
            messages.success(request, 'Grupo adicionado com sucesso!')
        else:
            messages.error(request, 'O nome do grupo não pode estar vazio.')

    return redirect('manage_groups')

def edit_group_permissions(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')
        group.permissions.set(permission_ids)
        messages.success(request, 'Permissões atualizadas com sucesso!')

    return redirect('manage_groups')

def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Grupo removido com sucesso!')

    return redirect('manage_groups')

def manage_groups(request):
    if request.method == 'POST':
        # Verificar se é uma ação de adicionar ou editar grupo
        if 'group_name' in request.POST:
            # Adicionar novo grupo
            group_name = request.POST['group_name']
            permissions_ids = request.POST.getlist('permissions')

            group, created = AuthGroup.objects.get_or_create(name=group_name)
            group.permissions.set(permissions_ids)  # Associar permissões ao grupo
            group.save()

            messages.success(request, f'Grupo "{group_name}" criado com sucesso!')

        elif 'permissions_group_id' in request.POST:
            # Editar grupo existente
            group_id = request.POST['permissions_group_id']
            group = get_object_or_404(AuthGroup, id=group_id)
            permissions_ids = request.POST.getlist('permissions')

            group.permissions.set(permissions_ids)  # Atualizar permissões do grupo
            group.save()

            messages.success(request, f'Permissões do grupo "{group.name}" atualizadas com sucesso!')

        elif 'action' in request.POST and request.POST['action'] == 'delete':
            # Remover grupo
            group_id = request.POST['group_id']
            group = get_object_or_404(AuthGroup, id=group_id)
            group.delete()
            messages.success(request, f'Grupo "{group.name}" removido com sucesso!')

        return redirect('manage_groups')

    # Exibir grupos e permissões
    groups = AuthGroup.objects.all().prefetch_related('permissions')
    permissions = AuthPermission.objects.all()
    return render(request, 'manage_groups.html', {
        'groups': groups,
        'permissions': permissions,
    })


def manage_users_groups_permissions(request):
    users = AuthUser.objects.all()
    groups = AuthGroup.objects.all()
    permissions = AuthPermission.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        permission_id = request.POST.get('permission_id')
        action = request.POST.get('action')

        try:
            user = AuthUser.objects.get(id=user_id)

            if action == 'add_permission':
                permission = AuthPermission.objects.get(id=permission_id)
                # Usa o modelo intermediário para adicionar a permissão
                user_perm, created = AuthUserUserPermissions.objects.get_or_create(user=user, permission=permission)
                if created:
                    messages.success(request, f"Permissão '{permission.name}' adicionada ao utilizador '{user.username}'.")
                else:
                    messages.warning(request, f"O utilizador '{user.username}' já possui a permissão '{permission.name}'.")

            elif action == 'remove_permission':
                permission = AuthPermission.objects.get(id=permission_id)
                # Remove a permissão através do modelo intermediário
                deleted, _ = AuthUserUserPermissions.objects.filter(user=user, permission=permission).delete()
                if deleted:
                    messages.success(request, f"Permissão '{permission.name}' removida do utilizador '{user.username}'.")
                else:
                    messages.warning(request, f"O utilizador '{user.username}' não possui a permissão '{permission.name}'.")

            elif action == 'add_group':
                group = AuthGroup.objects.get(id=group_id)
                # Usa o modelo intermediário para associar o utilizador ao grupo
                user_group, created = AuthUserGroups.objects.get_or_create(user=user, group=group)
                if created:
                    messages.success(request, f"Utilizador '{user.username}' foi adicionado ao grupo '{group.name}'.")
                else:
                    messages.warning(request, f"O utilizador '{user.username}' já está no grupo '{group.name}'.")

        except (AuthUser.DoesNotExist, AuthGroup.DoesNotExist, AuthPermission.DoesNotExist):
            messages.error(request, "Erro ao processar o pedido. Verifique se o utilizador, grupo ou permissão existe.")

        return redirect('manage_users_groups_permissions')

    # Obter permissões e grupos associados aos utilizadores de maneira segura
    user_permissions = AuthUserUserPermissions.objects.select_related('user', 'permission').all()
    user_groups = AuthUserGroups.objects.select_related('user', 'group').all()

    return render(request, 'gerenciar_usuarios.html', {
        'users': users,
        'groups': groups,
        'permissions': permissions,
        'user_permissions': user_permissions,
        'user_groups': user_groups,
    })
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
