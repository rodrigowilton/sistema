from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ApartamentoForm
from django.contrib import messages
from app.models import Condominios, Apartamentos
from django.http import JsonResponse
from django.db.models import F, IntegerField
from django.db.models.functions import Substr, Cast


@login_required
def criar_apartamentos(request):
    condominios = Condominios.objects.filter(status=1)
    apartamentos = None
    condominio_selecionado = None
    andares = None
    apartamentos_por_andar = None
    prefixo_apartamento = None
    numero_inicial = None
    apartamentos_existentes = []

    if request.method == 'POST':
        condominio_id = request.POST.get('condominio')
        andares = int(request.POST.get('andares'))
        apartamentos_por_andar = int(request.POST.get('apartamentos_por_andar'))
        prefixo_apartamento = request.POST.get('prefixo_apartamento')  # Obtém o prefixo alfanumérico
        numero_inicial = int(request.POST.get('numero_inicial'))  # Obtém o número inicial (ex: 1000)

        # Obtenha o condomínio selecionado
        condominio = Condominios.objects.get(id=condominio_id)
        condominio_selecionado = condominio  # Mantém o condomínio selecionado na tela

        # Obtenha todos os apartamentos existentes no condomínio
        apartamentos_existentes_db = Apartamentos.objects.filter(condominio=condominio).values_list('nome_apartamento',
                                                                                                    flat=True)

        novos_apartamentos = []  # Lista para armazenar novos apartamentos a serem criados
        for andar in range(andares):
            # O número inicial será o andar * número_inicial + 1 (para começar o primeiro apto do andar com 01)
            numero_atual = (andar + 1) * numero_inicial + 1

            for apartamento in range(apartamentos_por_andar):
                nome_apartamento = f"{prefixo_apartamento} {numero_atual}"  # Usa o prefixo alfanumérico

                # Verificar se o apartamento já existe no condomínio (normalizamos espaços e caixa alta/baixa para evitar erros)
                if nome_apartamento.strip().lower() not in [apt.strip().lower() for apt in apartamentos_existentes_db]:
                    # Adiciona o novo apartamento à lista de novos apartamentos
                    novos_apartamentos.append(
                        Apartamentos(
                            condominio=condominio,
                            nome_apartamento=nome_apartamento,
                            status=1  # Defina o status como 1
                        )
                    )
                else:
                    # Se o apartamento já existir, armazena o nome do apartamento na lista de existentes
                    apartamentos_existentes.append(nome_apartamento)

                numero_atual += 1  # Incrementa o número do apartamento dentro do andar

        # Cria todos os apartamentos novos de uma vez
        if novos_apartamentos:
            Apartamentos.objects.bulk_create(novos_apartamentos)

        # Verifica se houve apartamentos que já existiam
        if apartamentos_existentes:
            # Exibe um alerta com os nomes dos apartamentos que já existiam
            messages.warning(request, f"Os seguintes apartamentos já existiam: {', '.join(apartamentos_existentes)}")

        if novos_apartamentos:
            # Caso tenha criado apartamentos novos, exibe uma mensagem de sucesso
            messages.success(request, f"{len(novos_apartamentos)} apartamentos foram criados com sucesso.")

        # Após criar, redirecione para a página que chamou a função
        return redirect('criar_apartamentos')  # Substitua pelo nome da view ou URL correta

    elif request.GET.get('condominio_id'):  # Para manter os apartamentos ao recarregar
        condominio_id = request.GET.get('condominio_id')
        condominio_selecionado = Condominios.objects.get(id=condominio_id)

        # Ajuste de ordenação usando `annotate` para ordenar corretamente pelo número do apartamento
        apartamentos = Apartamentos.objects.filter(condominio=condominio_selecionado).annotate(
            # Extrai a parte numérica do nome do apartamento (assumindo que há um espaço entre prefixo e número)
            numero_apartamento=Cast(Substr('nome_apartamento', 5), IntegerField())  # Ajuste conforme o formato do nome
        ).order_by('numero_apartamento')

        # Retorna os apartamentos em formato JSON
        apartamentos_data = [
            {
                'id': apartamento.id,
                'nome': apartamento.nome_apartamento,
                'condominio_nome': apartamento.condominio.nome_condominio  # Inclua o nome do condomínio
            }
            for apartamento in apartamentos
        ]
        return JsonResponse({'apartamentos': apartamentos_data})

    return render(request, 'criar_apartamentos.html', {
        'condominios': condominios,
        'apartamentos': apartamentos,
        'condominio_selecionado': condominio_selecionado
    })


# View para deletar apartamento
@login_required
def deletar_apartamento(request, apartamento_id):
    apartamento = get_object_or_404(Apartamentos, id=apartamento_id)
    if request.method == 'POST':  # Verifique se a requisição é um POST
        apartamento.delete()  # Deletar o apartamento
        return redirect('criar_apartamentos')  # Redirecionar após a exclusão
    return render(request, 'deletar_apartamento.html', {'apartamento': apartamento})


@login_required
def editar_apartamento(request, apartamento_id):
    apartamento = get_object_or_404(Apartamentos, id=apartamento_id)

    if request.method == 'POST':
        form = ApartamentoForm(request.POST, instance=apartamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apartamento editado com sucesso!')
            return redirect('criar_apartamentos')  # Redirecione para a página que lista apartamentos
    else:
        form = ApartamentoForm(instance=apartamento)

    return render(request, 'editar_apartamentos.html', {'form': form, 'apartamento': apartamento})

