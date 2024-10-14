from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Apartamentos
from .forms import ApartamentoForm
from django.contrib import messages
from app.models import Condominios, Apartamentos

# Listar apartamentos
def listar_apartamentos(request):
    apartamentos = Apartamentos.objects.all()
    return render(request, 'listar_apartamentos.html', {'apartamentos': apartamentos})



def list_apartamentos(request):
    apartamentos = Apartamentos.objects.all()
    return render(request, 'list.html', {'apartamentos': apartamentos})

# gerar aptos
def criar_apartamentos(request):
    condominios = Condominios.objects.all()
    apartamentos = None
    condominio_selecionado = None

    if request.method == 'POST':
        condominio_id = request.POST.get('condominio')
        andares = int(request.POST.get('andares'))
        apartamentos_por_andar = int(request.POST.get('apartamentos_por_andar'))

        # Obtenha o condomínio selecionado
        condominio = Condominios.objects.get(id=condominio_id)
        condominio_selecionado = condominio  # Mantém o condomínio selecionado na tela

        # Inicialize o número inicial de apartamentos
        for andar in range(andares):
            numero_inicial = 101 + (andar * 100)  # Ajusta o número inicial com base no andar
            for apartamento in range(apartamentos_por_andar):
                nome_apartamento = f"Apt {numero_inicial}"

                # Crie o apartamento com status 1
                Apartamentos.objects.create(
                    condominio=condominio,
                    nome_apartamento=nome_apartamento,
                    status=1  # Defina o status como 1
                )
                numero_inicial += 1  # Incrementa o número do apartamento

        # Após criar, mostre os apartamentos criados
        apartamentos = Apartamentos.objects.filter(condominio=condominio)

    elif request.GET.get('condominio_id'):  # Para manter os apartamentos ao recarregar
        condominio_id = request.GET.get('condominio_id')
        condominio_selecionado = Condominios.objects.get(id=condominio_id)
        apartamentos = Apartamentos.objects.filter(condominio=condominio_selecionado)

    return render(request, 'criar_apartamentos.html', {
        'condominios': condominios,
        'apartamentos': apartamentos,
        'condominio_selecionado': condominio_selecionado
    })


def editar_apartamento(request, id):
    apartamento = get_object_or_404(Apartamentos, id=id)
    if request.method == 'POST':
        apartamento.nome_apartamento = request.POST.get('nome_apartamento')
        apartamento.save()
        return redirect('listar_apartamentos')

    return render(request, 'editar_apartamento.html', {'apartamento': apartamento})


# Adicionar apartamento
def add_apartamento(request):
    if request.method == 'POST':
        form = ApartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apartamento adicionado com sucesso!')
            return redirect('list_apartamentos')
    else:
        form = ApartamentoForm()
    return render(request, 'form.html', {'form': form})

# Editar apartamento
def edit_apartamento(request, id):
    apartamento = get_object_or_404(Apartamentos, id=id)
    if request.method == 'POST':
        form = ApartamentoForm(request.POST, instance=apartamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Apartamento editado com sucesso!')
            return redirect('list_apartamentos')
    else:
        form = ApartamentoForm(instance=apartamento)
    return render(request, 'apartamentos/form.html', {'form': form})

# Deletar apartamento
def delete_apartamento(request, id):
    apartamento = get_object_or_404(Apartamentos, id=id)
    if request.method == 'POST':
        apartamento.delete()
        messages.success(request, 'Apartamento removido com sucesso!')
        return redirect('list_apartamentos')
    return render(request, 'apartamentos/delete.html', {'apartamento': apartamento})
