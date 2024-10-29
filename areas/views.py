from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Condominios, Areas
from django.http import JsonResponse
from .forms import AreaForm
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
        limite_pessoas = request.POST.get('limite_pessoas') or None  # Define None se estiver vazio
        valor = request.POST.get('valor')
        normas = request.POST.get('normas')
        info = request.POST.get('info')
        cor = request.POST.get('cor')
        tipo_reserva = request.POST.get('tipo_reserva')

        # Captura os novos campos do formulário
        hora_min = request.POST.get('hora_min')
        hora_max = request.POST.get('hora_max')
        antecedencia_min = request.POST.get('antecedencia_min')
        antecedencia_max = request.POST.get('antecedencia_max')
        intervalo_entre_reservas = request.POST.get('intervalo_entre_reservas')
        max_abertos = request.POST.get('max_abertos')
        tempo_entre_reservas = request.POST.get('tempo_entre_reservas')
        hora_inicio_permitido = request.POST.get('hora_inicio_permitido')
        hora_fim_permitido = request.POST.get('hora_fim_permitido')
        hora_inicio_permitido_fds = request.POST.get('hora_inicio_permitido_fds')
        hora_fim_permitido_fds = request.POST.get('hora_fim_permitido_fds')
        permite_convidados = request.POST.get('permite_convidados')
        necessita_aprovacao = request.POST.get('necessita_aprovacao')
        dias_permitidos = {
            'segunda': 'segunda' in request.POST,
            'terca': 'terca' in request.POST,
            'quarta': 'quarta' in request.POST,
            'quinta': 'quinta' in request.POST,
            'sexta': 'sexta' in request.POST,
            'sabado': 'sabado' in request.POST,
            'domingo': 'domingo' in request.POST,
        }
        tem_feriados = request.POST.get('tem_feriados')

        # Cria a nova área
        Areas.objects.create(
            condominio_id=condominio_id,
            nome_area=nome_area,
            andar=andar,
            limite_pessoas=limite_pessoas if limite_pessoas is not None else None,  # Lógica para limite_pessoas
            valor=valor,
            normas=normas,
            info=info,
            cor=cor,
            tipo_reserva=tipo_reserva,
            hora_min=hora_min,
            hora_max=hora_max,
            antecedencia_min=antecedencia_min,
            antecedencia_max=antecedencia_max,
            intervalo_entre_reservas=intervalo_entre_reservas,
            max_abertos=max_abertos,
            tempo_entre_reservas=tempo_entre_reservas,
            hora_inicio_permitido=hora_inicio_permitido,
            hora_fim_permitido=hora_fim_permitido,
            hora_inicio_permitido_fds=hora_inicio_permitido_fds,
            hora_fim_permitido_fds=hora_fim_permitido_fds,
            permite_convidados=permite_convidados,
            necessita_aprovacao=necessita_aprovacao,
            tem_feriados=tem_feriados,
            **dias_permitidos,  # Adiciona os dias permitidos como campos da nova área
            status=1,  # Define o status como ativo
        )

        messages.success(request, 'Área criada com sucesso.')
        return redirect('menu_agd')  # Redireciona para uma página de destino após a criação

    # Renderiza o formulário de criação de área
    return render(request, 'criar_areas.html', {
        'condominios': condominios,
        'tipos_reserva_opcoes': tipos_reserva_opcoes,
    })


def consulta_area(request):
    pesquisar = request.GET.get('pesquisar', '')  # Obtém o termo de pesquisa
    areas = Areas.objects.all()  # Obtém todas as áreas inicialmente

    if pesquisar:
        # Filtra as áreas com base no nome da área
        areas = areas.filter(nome_area__icontains=pesquisar)

    context = {
        'areas': areas,
    }
    return render(request, 'consulta_area.html', context)

def editar_area(request, area_id):
    area = get_object_or_404(Areas, id=area_id)  # Busca a área pelo ID

    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)  # Preenche o formulário com os dados da área
        if form.is_valid():
            form.save()  # Salva as alterações
            return redirect('consulta_are')  # Redireciona para a página de consulta após salvar
    else:
        form = AreaForm(instance=area)  # Cria um formulário com os dados da área

    return render(request, 'editar_area.html', {'form': form, 'area': area})




def deletar_area(request, area_id):
    area = get_object_or_404(Areas, id=area_id)  # Busca a área pelo ID

    if request.method == 'POST':
        area.delete()  # Deleta a área
        return redirect('consulta_are')  # Redireciona para a página de consulta após a deleção

    return render(request, 'deletar_area.html', {'area': area})  # Renderiza a página de confirmação