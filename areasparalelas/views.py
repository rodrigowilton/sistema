from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Areas, AreasParalelas, Condominios
from .forms import AreasParalelasForm, EditAreaParalelaForm


def get_areas(request):
    condominio_id = request.GET.get('condominio_id')
    areas = Areas.objects.filter(condominio_id=condominio_id).values('id', 'nome_area')  # Filtrar áreas pelo condomínio
    areas_list = list(areas)  # Converte o queryset para lista

    return JsonResponse({'areas': areas_list})

def adicionar_area_paralela(request):
    condominios = Condominios.objects.all()
    selected_condominio = None
    form = AreasParalelasForm()

    if request.method == 'POST':
        selected_condominio = request.POST.get('condominio')
        form = AreasParalelasForm(request.POST, selected_condominio=selected_condominio)

        if form.is_valid():
            area_paralela = form.save(commit=False)  # Cria a instância sem salvar ainda
            area_paralela.status = 1  # Define o status como 1
            area_paralela.save()  # Salva a nova área paralela com o status definido
            return redirect('areas_paralelas')  # Redireciona após a criação

    # Se um condomínio foi selecionado, busca as áreas
    if selected_condominio:
        form.fields['area'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)
        form.fields['area2'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)

    return render(request, 'adicionar_area_paralela.html', {
        'condominios': condominios,
        'form': form,
        'selected_condominio': selected_condominio,
    })


def editar_area_paralela(request, pk):
    area_paralela = get_object_or_404(AreasParalelas, id=pk)

    if request.method == 'POST':
        form = AreasParalelasForm(request.POST, instance=area_paralela)
        if form.is_valid():
            form.save()
            return redirect('areas_paralelas')
    else:
        form = AreasParalelasForm(instance=area_paralela)

    # Obter as áreas disponíveis para o condomínio da área paralela
    areas_disponiveis = Areas.objects.filter(condominio=area_paralela.area.condominio)  # Supondo que 'condominio' seja um campo no modelo Areas

    context = {
        'form': form,
        'area_paralela': area_paralela,
        'areas_disponiveis': areas_disponiveis,  # Adicionando as áreas disponíveis ao contexto
    }
    return render(request, 'editar_area_paralela.html', context)



# Função de view para listar e buscar áreas paralelas
def buscar_areas_paralelas(request):
    # Termo de pesquisa
    search_query = request.GET.get('search', '').strip()

    # Filtra as áreas paralelas com base no nome do condomínio
    if search_query:
        areas_paralelas = AreasParalelas.objects.filter(area__condominio__nome_condominio__icontains=search_query)
    else:
        areas_paralelas = AreasParalelas.objects.all()

    # Mapear o tipo de exibição
    for area in areas_paralelas:
        if area.tipo == 1:
            area.tipo_display = 'Concorrente'
        elif area.tipo == 2:
            area.tipo_display = 'Conjunta'
        else:
            area.tipo_display = 'Desconhecido'

    # Contexto para renderizar o template
    context = {'areas_paralelas': areas_paralelas, 'search_query': search_query}
    return render(request, 'areas_paralelas.html', context)


# View para listar áreas paralelas
class AreasParalelasView(View):
    def get(self, request):
        areas_paralelas = AreasParalelas.objects.all()

        # Mapeamento de tipos
        for area in areas_paralelas:
            if area.tipo == 1:
                area.tipo_display = 'Concorrente'
            elif area.tipo == 2:
                area.tipo_display = 'Conjunta'
            else:
                area.tipo_display = 'Desconhecido'

        return render(request, 'areas_paralelas.html', {'areas_paralelas': areas_paralelas})


# View para editar área paralela
class EditarAreaParalelaView(View):
    def get(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        form = AreasParalelasForm(instance=area_paralela)
        return render(request, 'editar_area_paralela.html', {'form': form})

    def post(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        form = AreasParalelasForm(request.POST, instance=area_paralela)
        if form.is_valid():
            form.save()
            return redirect('areas_paralelas')
        return render(request, 'editar_area_paralela.html', {'form': form})


# View para deletar área paralela
class DeleteAreaParalelaView(View):
    def get(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        return render(request, 'confirm_delete_area_paralela.html', {'area_paralela': area_paralela})

    def post(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        area_paralela.delete()
        return redirect('areas_paralelas')
