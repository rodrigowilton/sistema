from django.shortcuts import render, redirect, get_object_or_404
from app.models import Feriados, Condominios, CondominiosFeriados
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from .forms import FeriadoForm
from django.contrib import messages



# View para adicionar feriados
@require_http_methods(["GET", "POST"])
def adicionar_feriados(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        sinc_acessos = request.POST.get('sinc_acessos', 0)  # Default to 0 if not provided
        status = request.POST.get('status', 1)  # Default to 1 (active)

        Feriados.objects.create(
            nome=nome,
            data=data,
            sinc_acessos=sinc_acessos,
            status=status,
            created=timezone.now(),
            modified=timezone.now()
        )
        return redirect('listar_feriados')  # Redireciona para a lista de feriados

    return render(request, 'adicionar_feriados.html')


def editar_feriados(request, feriado_id):
    feriado = get_object_or_404(Feriados, pk=feriado_id)

    if request.method == 'POST':
        # Formulário para o feriado
        form = FeriadoForm(request.POST, instance=feriado)

        # Recupera os IDs dos condomínios bloqueados como uma lista de inteiros
        bloqueados_ids = request.POST.get('bloqueados_ids', '')
        bloqueados_ids = [int(id.strip()) for id in bloqueados_ids.split(',') if id.strip().isdigit()]

        if form.is_valid():
            form.save()

            # Limpa os registros antigos de bloqueio para evitar duplicação
            CondominiosFeriados.objects.filter(feriado=feriado).delete()

            # Cria novos registros de condomínios bloqueados
            for condominio_id in bloqueados_ids:
                CondominiosFeriados.objects.create(
                    condominio_id=condominio_id,
                    feriado=feriado,
                    status=1  # Status 1 para bloqueado
                )

            messages.success(request, "Feriado atualizado com sucesso!")
            return redirect('listar_feriados')

    else:
        form = FeriadoForm(instance=feriado)

        # IDs dos condomínios bloqueados
        bloqueados_ids = list(
            CondominiosFeriados.objects.filter(feriado=feriado).values_list('condominio_id', flat=True)
        )

    # Carrega os condomínios liberados e bloqueados
    condominios_liberados = Condominios.objects.exclude(id__in=bloqueados_ids)
    condominios_bloqueados = Condominios.objects.filter(id__in=bloqueados_ids)

    # Passa os dados para o template
    context = {
        'form': form,
        'condominios_liberados': condominios_liberados,
        'condominios_bloqueados': condominios_bloqueados,
        'bloqueados_ids': bloqueados_ids,
    }
    return render(request, 'editar_feriados.html', context)

# View para deletar feriados
@require_http_methods(["GET", "POST"])
def deletar_feriados(request, feriado_id):
    feriado = get_object_or_404(Feriados, id=feriado_id)

    if request.method == "POST":
        feriado.delete()
        return redirect('listar_feriados')

    return render(request, 'deletar_feriados.html', {'feriado': feriado})

# View para listar feriados com pesquisa
def listar_feriados(request):
    search_query = request.GET.get('search', '')  # Obtém o termo de busca
    feriados = Feriados.objects.all()  # Obtém todos os feriados do banco de dados

    if search_query:
        # Filtra pelo nome ou data do feriado
        feriados = feriados.filter(
            Q(nome__icontains=search_query) |  # Filtra pelo nome do feriado
            Q(data__icontains=search_query)    # Filtra pela data do feriado
        )

    context = {
        'feriados': feriados,
        'search_query': search_query  # Passa o termo de busca para o template
    }
    return render(request, 'listar_feriados.html', context)
