from django.shortcuts import render, get_object_or_404, redirect
from .models import Condominios
from django.contrib.auth.models import User, Group
from .models import AuthUser, AuthGroup, AuthPermission, AuthUserGroups, AuthUserUserPermissions, AuthGroupPermissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
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


def manage_groups(request):
    # Verifica se o método é POST para adicionar ou remover grupo
    if request.method == 'POST':
        if 'group_name' in request.POST:
            # Adiciona novo grupo
            group_name = request.POST.get('group_name').strip()
            if AuthGroup.objects.filter(name=group_name).exists():
                messages.error(request, f"Grupo '{group_name}' já existe.")
            else:
                AuthGroup.objects.create(name=group_name)
                messages.success(request, f"Grupo '{group_name}' foi criado com sucesso.")
        elif 'group_id' in request.POST and request.POST.get('action') == 'delete':
            # Remove grupo
            group_id = request.POST.get('group_id')
            try:
                group = AuthGroup.objects.get(id=group_id)
                group.delete()
                messages.success(request, f"Grupo '{group.name}' foi removido.")
            except AuthGroup.DoesNotExist:
                messages.error(request, "Grupo não encontrado.")

        return redirect('manage_groups')

    # Obter todos os grupos existentes
    groups = AuthGroup.objects.all()

    return render(request, 'grupos.html', {
        'groups': groups,
    })


# Mapeamento de permissões para Português
PERMISSION_TRANSLATIONS = {
    'can_add_user': 'Pode adicionar utilizador',
    'can_delete_user': 'Pode remover utilizador',
    'can_change_user': 'Pode modificar utilizador',
    'can_view_user': 'Pode ver utilizador',
    # Adiciona outras permissões conforme necessário
}

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
