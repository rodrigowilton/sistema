from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.models import Condominios, Apartamentos, Pets, TiposRacas, Racas
from django.http import JsonResponse

@login_required
def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id)  # Filtra apartamentos pelo ID do condomínio
    data = {
        'apartamentos': [{'id': apartamento.id, 'nome_apartamento': apartamento.nome_apartamento} for apartamento in apartamentos]
    }
    return JsonResponse(data)


@login_required
def get_racas_por_tipo_raca(request):
    tipo_raca_id = request.GET.get('tipo_raca_id')

    # Ajuste: o nome correto do campo é tipos_raca_id
    racas = Racas.objects.filter(tipos_raca_id=tipo_raca_id)  # Filtra as raças pelo tipo de raça
    data = {
        'racas': [{'id': raca.id, 'nome_raca': raca.nome_raca} for raca in racas]
    }
    return JsonResponse(data)


@login_required
def criar_pets(request):
    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        raca_id = request.POST.get('raca')  # Raça selecionada
        nome_pet = request.POST.get('nome_pet')
        status = request.POST.get('status')

        # Obter a instância de Apartamentos e Racas
        apartamento = Apartamentos.objects.get(id=apartamento_id)
        raca = Racas.objects.get(id=raca_id)  # Certifique-se de pegar a instância correta de Racas

        # Criar o objeto Pet
        pet = Pets.objects.create(
            apartamento=apartamento,
            raca=raca,  # Aqui estamos passando uma instância de Racas
            nome_pet=nome_pet,
            status=1
        )

        return redirect('criar_pets')  # Redireciona após criar o pet

    # Carrega dados para exibição no template
    condominios = Condominios.objects.all()
    tipos_racas = TiposRacas.objects.all()  # Carregar tipos de raça

    return render(request, 'criar_pets.html', {
        'condominios': condominios,
        'tipos_racas': tipos_racas
    })