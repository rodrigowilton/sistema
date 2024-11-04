from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.models import Areas, AreasParalelas, Condominios
from .forms import AreasParalelasForm, EditarAreaParalelaForm

def get_areas(request):
    condominio_id = request.GET.get('condominio_id')
    areas = Areas.objects.filter(condominio_id=condominio_id).values('id', 'nome_area')
    areas_list = list(areas)

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
    selected_condominio = area_paralela.area.condominio  # Obtendo o objeto do condomínio

    if request.method == 'POST':
        form = EditarAreaParalelaForm(request.POST, instance=area_paralela, selected_condominio=selected_condominio.id)
        if form.is_valid():
            area_paralela = form.save(commit=False)  # Cria a instância sem salvar ainda
            area_paralela.status = 1  # Mantém o status como 1
            area_paralela.save()  # Salva a área paralela
            return redirect('areas_paralelas')  # Redireciona após salvar
    else:
        form = EditarAreaParalelaForm(instance=area_paralela, selected_condominio=selected_condominio.id)

    # Define a descrição do tipo com base no valor do tipo selecionado
    if area_paralela.tipo == 1:
        tipo_display = "Concorrente"
    else:
        tipo_display = "Conjunta"

    context = {
        'form': form,
        'area_paralela': area_paralela,
        'selected_condominio': selected_condominio,  # Passa o objeto do condomínio
        'tipo_display': tipo_display,  # Passa o tipo como texto
    }

    return render(request, 'editar_area_paralela.html', context)

# Função de view para listar e buscar áreas paralelas
def buscar_areas_paralelas(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        areas_paralelas = AreasParalelas.objects.filter(area__condominio__nome_condominio__icontains=search_query)
    else:
        areas_paralelas = AreasParalelas.objects.all()

    for area in areas_paralelas:
        if area.tipo == 1:
            area.tipo_display = 'Concorrente'
        elif area.tipo == 2:
            area.tipo_display = 'Conjunta'
        else:
            area.tipo_display = 'Desconhecido'

    context = {'areas_paralelas': areas_paralelas, 'search_query': search_query}
    return render(request, 'areas_paralelas.html', context)

class AreasParalelasView(View):
    def get(self, request):
        areas_paralelas = AreasParalelas.objects.all()

        for area in areas_paralelas:
            if area.tipo == 1:
                area.tipo_display = 'Concorrente'
            elif area.tipo == 2:
                area.tipo_display = 'Conjunta'
            else:
                area.tipo_display = 'Desconhecido'

        return render(request, 'areas_paralelas.html', {'areas_paralelas': areas_paralelas})

class EditarAreaParalelaView(View):
    def get(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        form = AreasParalelasForm(instance=area_paralela)
        return render(request, 'editar_area_paralela.html', {'form': form})

    def post(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        form = AreasParalelasForm(request.POST, instance=area_paralela)
        if form.is_valid():
            area_paralela = form.save(commit=False)  # Cria a instância sem salvar ainda
            area_paralela.status = 1  # Mantém o status como 1
            area_paralela.save()  # Salva a área paralela com o status definido
            return redirect('areas_paralelas')  # Redireciona após salvar
        return render(request, 'editar_area_paralela.html', {'form': form})

class DeleteAreaParalelaView(View):
    def get(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        return render(request, 'confirm_delete_area_paralela.html', {'area_paralela': area_paralela})

    def post(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        area_paralela.delete()
        return redirect('areas_paralelas')
