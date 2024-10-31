
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Areas, AreasParalelas, Condominios
from .forms import AreasParalelasForm


# View para listar áreas paralelas
class AreasParalelasView(View):
    def get(self, request):
        # Lógica para mostrar áreas paralelas
        areas_paralelas = AreasParalelas.objects.all()
        return render(request, 'areas_paralelas.html', {'areas_paralelas': areas_paralelas})

def get_areas(request, condominio_id):
    areas = Areas.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome_area')  # Ajuste conforme os campos disponíveis
    return JsonResponse({'areas': list(areas)})

# View para adicionar área paralela
def adicionar_area_paralela(request):
    condominios = Condominios.objects.all()
    areas1 = []
    areas2 = []
    selected_condominio = None  # Para armazenar o condomínio selecionado

    if request.method == 'POST':
        selected_condominio = request.POST.get('condominio')  # Obtenha o condomínio selecionado
        area1_id = request.POST.get('area1')
        area2_id = request.POST.get('area2')

        # Adicione a lógica para criar a área paralela
        if area1_id and area2_id:
            AreasParalelas.objects.create(
                area_id=area1_id,
                area2_id=area2_id,
                tipo=1,  # ou 2, dependendo do que você deseja
                status=1,  # Defina o status conforme necessário
            )
            return redirect('areas_paralelas')  # Redirecione após a criação

    # Busque as áreas se um condomínio foi selecionado
    if selected_condominio:
        areas1 = Areas.objects.filter(condominio_id=selected_condominio, status=1)
        areas2 = Areas.objects.filter(condominio_id=selected_condominio, status=1)

    return render(request, 'adicionar_area_paralela.html', {
        'condominios': condominios,
        'areas1': areas1,
        'areas2': areas2,
        'selected_condominio': selected_condominio,  # Passar o condomínio selecionado
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
        area_paralela.delete()  # Deleta a área paralela
        return redirect('areas_paralelas')  # Redireciona para a lista de áreas paralelas
