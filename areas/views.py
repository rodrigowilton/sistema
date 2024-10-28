from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Areas, Condominios

def criar_area(request):
    # Filtra apenas condomínios com status 1
    condominios = Condominios.objects.filter(status=1)

    # Define as opções de tipos de reserva predefinidas
    tipos_reserva_opcoes = [
        {"id": 1, "nome": "Reserva única por Dia"},
        {"id": 2, "nome": "Horários Livres"},
        {"id": 3, "nome": "Horários Fixos"},
    ]

    if request.method == 'POST':
        # Captura os dados do formulário para criação de uma nova área
        condominio_id = request.POST.get('condominio')
        nome_area = request.POST.get('nome_area')
        andar = request.POST.get('andar')
        limite_pessoas = request.POST.get('limite_pessoas')
        valor = request.POST.get('valor')
        normas = request.POST.get('normas')
        info = request.POST.get('info')
        cor = request.POST.get('cor')
        tipo_reserva = request.POST.get('tipo_reserva')

        # Cria a nova área
        Areas.objects.create(
            condominio_id=condominio_id,
            nome_area=nome_area,
            andar=andar,
            limite_pessoas=limite_pessoas,
            valor=valor,
            normas=normas,
            info=info,
            cor=cor,
            tipo_reserva=tipo_reserva,
            status=1,  # Define o status como ativo
        )

        messages.success(request, 'Área criada com sucesso.')
        return redirect('url_destino')  # Redireciona para uma página de destino após a criação

    # Renderiza o formulário de criação de área
    return render(request, 'criar_areas.html', {
        'condominios': condominios,
        'tipos_reserva_opcoes': tipos_reserva_opcoes,
    })
