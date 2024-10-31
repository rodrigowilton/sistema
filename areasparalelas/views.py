from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Areas, AreasParalelas, Condominios
from .forms import AreasParalelasForm


# View de busca por condomínios
from django.shortcuts import render
from app.models import AreasParalelas

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


# View para buscar áreas de um condomínio específico
def get_areas(request, condominio_id):
    areas = Areas.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_area')
    return JsonResponse({'areas': list(areas)})


# View para adicionar área paralela
def adicionar_area_paralela(request):
    condominios = Condominios.objects.all()
    areas1, areas2 = [], []
    selected_condominio = None

    if request.method == 'POST':
        selected_condominio = request.POST.get('condominio')
        area1_id = request.POST.get('area1')
        area2_id = request.POST.get('area2')

        # Cria a área paralela, caso as áreas estejam definidas
        if area1_id and area2_id:
            AreasParalelas.objects.create(
                area_id=area1_id,
                area2_id=area2_id,
                tipo=1,  # ou 2, conforme necessário
                status=1,
            )
            return redirect('areas_paralelas')

    # Se um condomínio foi selecionado, busca as áreas
    if selected_condominio:
        areas1 = Areas.objects.filter(condominio_id=selected_condominio, status=1)
        areas2 = Areas.objects.filter(condominio_id=selected_condominio, status=1)

    return render(request, 'adicionar_area_paralela.html', {
        'condominios': condominios,
        'areas1': areas1,
        'areas2': areas2,
        'selected_condominio': selected_condominio,
    })


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
