from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Veiculos, Apartamentos, TiposVeiculos, Condominios
from django.http import JsonResponse


def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)

    apartamentos_data = [{'id': apartamento.id, 'nome_apartamento': apartamento.nome_apartamento} for apartamento in apartamentos]

    return JsonResponse({'apartamentos': apartamentos_data})



def listar_pessoas(request):
    veiculos = Veiculos.objects.all()  # Lista todos os veículos
    return render(request, 'listar_pessoas.html', {'veiculos': veiculos})

def editar_veiculos(request, veiculo_id):
    veiculo = get_object_or_404(Veiculos, id=veiculo_id)

    if request.method == 'POST':
        # Coletando dados do formulário
        apartamento_id = request.POST.get('apartamento')
        tipos_veiculo_id = request.POST.get('tipos_veiculo')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        cor = request.POST.get('cor')
        placa = request.POST.get('placa')
        status = request.POST.get('status')

        # Atualizando o veículo
        veiculo.apartamento_id = apartamento_id
        veiculo.tipos_veiculo_id = tipos_veiculo_id
        veiculo.marca = marca
        veiculo.modelo = modelo
        veiculo.cor = cor
        veiculo.placa = placa
        veiculo.status = status
        veiculo.save()

        messages.success(request, 'Veículo atualizado com sucesso!')
        return redirect('listar_pessoas')

    return render(request, 'editar_veiculos.html', {
        'veiculo': veiculo,
        'apartamentos': Apartamentos.objects.all(),
        'tipos_veiculos': TiposVeiculos.objects.all(),
    })

def criar_veiculos(request):
    if request.method == 'POST':
        # Coletando dados do formulário
        apartamento_id = request.POST.get('apartamento')
        tipos_veiculo_id = request.POST.get('tipos_veiculo')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        cor = request.POST.get('cor')
        placa = request.POST.get('placa')
        status = 1  # Definindo o status como 1

        # Criando o novo veículo
        try:
            novo_veiculo = Veiculos(
                apartamento_id=apartamento_id,
                tipos_veiculo_id=tipos_veiculo_id,
                marca=marca,
                modelo=modelo,
                cor=cor,
                placa=placa,
                status=status,
            )
            novo_veiculo.save()  # Salvando o novo veículo no banco de dados
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('criar_veiculos')  # Redireciona para a lista de veículos
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar veículo: {str(e)}')

    # Passando condomínios para o template
    condominios = Condominios.objects.all()
    return render(request, 'criar_veiculos.html', {
        'apartamentos': Apartamentos.objects.all(),  # Adicione conforme necessário
        'tipos_veiculos': TiposVeiculos.objects.all(),  # Adicione conforme necessário
        'condominios': condominios,  # Adicionando a lista de condomínios
    })