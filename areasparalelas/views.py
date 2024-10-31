from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from app.models import Areas, AreasParalelas, Condominios
from .forms import AreasParalelasForm

class AreasParalelasView(View):
    def get(self, request):
        # Lógica para mostrar áreas paralelas
        return render(request, 'areas_paralelas.html', {})

def get_areas(request, condominio_id):
    areas = Areas.objects.filter(condominio_id=condominio_id, status=1).values('id', 'nome')  # Ajuste conforme os campos disponíveis
    return JsonResponse({'areas': list(areas)})

def fetch_areas(request, condominio_id):
    areas = Areas.objects.filter(condominio_id=condominio_id)
    areas_list = [{'id': area.id, 'nome_area': area.nome_area} for area in areas]
    return JsonResponse(areas_list, safe=False)



# View para listar áreas paralelas
def adicionar_area_paralela(request):
    condominios = Condominios.objects.all()
    areas1 = []
    areas2 = []
    selected_condominio = None  # Para armazenar o condomínio selecionado

    if request.method == 'POST':
        selected_condominio = request.POST.get('condominio')  # Obtenha o condomínio selecionado
        area1_id = request.POST.get('area')
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
        areas1 = Areas.objects.filter(condominio_id=selected_condominio)
        areas2 = Areas.objects.filter(condominio_id=selected_condominio)

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
