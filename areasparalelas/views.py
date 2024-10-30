from django.views import View  # Importando a classe View
from django.shortcuts import render, get_object_or_404, redirect
from app.models import AreasParalelas  # Importando o modelo
from .forms import AreasParalelasForm  # Certifique-se de que você tenha um formulário para as áreas paralelas

class AreasParalelasView(View):
    def get(self, request):
        areas_paralelas = AreasParalelas.objects.all()  # Obtém todas as áreas paralelas
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
            form.save()
            return redirect('areas_paralelas')  # Redireciona para a lista de áreas paralelas
        return render(request, 'editar_area_paralela.html', {'form': form})

class DeleteAreaParalelaView(View):
    def get(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        return render(request, 'confirm_delete_area_paralela.html', {'area_paralela': area_paralela})

    def post(self, request, pk):
        area_paralela = get_object_or_404(AreasParalelas, pk=pk)
        area_paralela.delete()  # Deleta a área paralela
        return redirect('areas_paralelas')  # Redireciona para a lista de áreas paralelas
