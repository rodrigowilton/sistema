from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from app.models import ControlesAcessos, TatticaFuncionarios, TiposControlesAcessos, Condominios, Apartamentos, Pessoas, Sindicos
from django.http import JsonResponse
from controleacesso.forms import ControleAcessoForm


def adicionar_controleacesso(request):
    # Carregar os dados necessários para o formulário
    colaboradores = TatticaFuncionarios.objects.all()
    tipos_controles_acesso = TiposControlesAcessos.objects.all()
    condominios = Condominios.objects.all()

    if request.method == 'POST':
        form = ControleAcessoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Substitua 'success' pela URL que você deseja após a criação bem-sucedida
    else:
        form = ControleAcessoForm()

    return render(request, 'adicionar_controleacesso.html', {
        'form': form,
        'colaboradores': colaboradores,
        'tipos_controles_acesso': tipos_controles_acesso,
        'condominios': condominios,
    })

def carregar_apartamentos(request, condominio_id):
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)
    apartamentos_data = [{'id': ap.id, 'nome': ap.nome_apartamento} for ap in apartamentos]
    return JsonResponse({'apartamentos': apartamentos_data})

def carregar_pessoas(request, apartamento_id):
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id)
    pessoas_data = [{'id': p.id, 'nome': p.nome_pessoa} for p in pessoas]
    return JsonResponse({'pessoas': pessoas_data})

def carregar_sindicos(request, condominio_id):
    sindicos = Sindicos.objects.filter(condominio_id=condominio_id)
    sindicos_data = [{'id': s.id, 'nome': s.nome_sindico} for s in sindicos]
    return JsonResponse({'sindicos': sindicos_data})



@login_required
def lista_controleacesso(request):
    # Obtenha os filtros enviados pelo usuário
    condominio = request.GET.get('condominio')
    tipos = request.GET.get('tipos')
    execucao = request.GET.get('execucao')
    pedido = request.GET.get('pedido')
    status = request.GET.get('status')  # O campo status será crucial aqui
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os dados com base nos filtros selecionados
    controles = ControlesAcessos.objects.all()

    # Aplica os filtros baseados nos parâmetros recebidos
    if condominio:
        controles = controles.filter(condominio_id=condominio)
    if tipos:
        controles = controles.filter(tipos_controles_acesso_id=tipos)
    if execucao:
        controles = controles.filter(execucao=execucao)
    if pedido:
        controles = controles.filter(pedido=pedido)
    if data_inicio:
        controles = controles.filter(created__gte=data_inicio)
    if data_fim:
        controles = controles.filter(created__lte=data_fim)

    # Filtra status; padrão será mostrar apenas "pendentes" (status=1) caso não seja selecionado um status
    if status:
        controles = controles.filter(status=status)
    else:
        controles = controles.filter(status=1)  # Apenas pendentes por padrão

    # Verifica se há pendências
    pendencias_existentes = controles.filter(status=1).exists()

    # Para dropdowns de seleção
    condominios = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
    tipos_controles = TiposControlesAcessos.objects.filter(status=1)

    # Renderiza os dados no template
    context = {
        'pendencias_existentes': pendencias_existentes,
        'controles': controles,
        'condominios': condominios,
        'tipos_controles': tipos_controles,
    }
    return render(request, 'lista_controleacesso.html', context)


