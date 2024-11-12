from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SindicoForm
from app.models import Sindicos, Apartamentos, Pessoas, TiposSindicos
from django.contrib import messages

@login_required
def lista_sindicos(request):
    sindicos = Sindicos.objects.filter(status=1, condominio__status=1).order_by('condominio__nome_condominio')
    return render(request, 'lista_sindicos.html', {'sindicos': sindicos})

def criar_sindico(request):
    if request.method == 'POST':
        form = SindicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico criado com sucesso.')
            return redirect('lista_sindicos')
    else:
        form = SindicoForm()
    return render(request, 'criar_sindico.html', {'form': form})


def editar_sindico(request, sindico_id):
    # Obtendo o síndico pelo ID
    sindico = get_object_or_404(Sindicos, id=sindico_id)
    
    # Filtrando os apartamentos que pertencem ao mesmo condomínio e que têm moradores
    apartamentos = Apartamentos.objects.filter(
        condominio=sindico.condominio,
        status=1  # Garantir que estamos pegando apenas apartamentos ativos
    )
    
    # Inicializando uma lista de pessoas vazia
    pessoas = Pessoas.objects.none()
    
    # Verificando se o síndico tem um apartamento associado e, se sim, buscando as pessoas desse apartamento
    if sindico.pessoa:
        pessoas = Pessoas.objects.filter(apartamento=sindico.pessoa.apartamento)
    
    # Obtendo os tipos de síndico para o dropdown
    tipos_sindico = TiposSindicos.objects.all()
    
    # Verificando se o método da requisição é POST
    if request.method == 'POST':
        form = SindicoForm(request.POST, instance=sindico)
        apartamento_id = request.POST.get('apartamento_id')  # Pegando o apartamento_id do formulário
        
        if apartamento_id:
            apartamento = Apartamentos.objects.get(id=apartamento_id)
            sindico.apartamento = apartamento  # Atualizando o apartamento do síndico
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Síndico atualizado com sucesso.')
            return redirect('lista_sindicos')
    else:
        # No GET, assegure que o queryset de apartamentos está sendo passado corretamente
        form = SindicoForm(instance=sindico)
        form.fields['apartamento'].queryset = apartamentos  # Atualiza o queryset de apartamentos no formulário
        
        # Definir o valor inicial do campo 'apartamento' com o apartamento do síndico
        if sindico.pessoa and sindico.pessoa.apartamento:
            form.fields[
                'apartamento'].initial = sindico.pessoa.apartamento.id  # Definindo o ID do apartamento como inicial
    
    # Passando os dados para o template
    return render(request, 'editar_sindico.html', {
        'form': form,
        'sindico': sindico,
        'apartamentos': apartamentos,  # Apenas apartamentos povoados
        'pessoas': pessoas,  # Apenas moradores do apartamento do síndico
        'tipos_sindico': tipos_sindico,
    })


def deletar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)
    sindico.delete()
    messages.success(request, 'Síndico deletado com sucesso.')
    return redirect('lista_sindicos')
from django.shortcuts import render

# Create your views here.
