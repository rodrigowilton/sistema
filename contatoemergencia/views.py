from django.shortcuts import render, redirect
from app.models import ContatoEmergencias, Condominios, Apartamentos
from django.http import JsonResponse
from django.contrib import messages

def get_apartamentos_por_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')
    return JsonResponse({'apartamentos': list(apartamentos)})

def criar_contato_emergencia(request):
    condominios = Condominios.objects.all()

    if request.method == 'POST':
        apartamento = Apartamentos.objects.get(id=request.POST['apartamento'])
        nome = request.POST['nome']
        celular = request.POST['celular']
        celular_2 = request.POST.get('celular_2', '')
        parentesco = request.POST.get('parentesco', '')
        obs = request.POST.get('obs', '')

        ContatoEmergencias.objects.create(
            apartamento=apartamento,
            nome=nome,
            celular=celular,
            celular_2=celular_2,
            parentesco=parentesco,
            obs=obs,
            status=1  # Define o status como 1 automaticamente
        )
        messages.success(request, 'Contato Cadastrado com sucesso!')
        return redirect('criar_contato_emergencia')  # redireciona após criação

    return render(request, 'criar_contato_emergencia.html', {
        'condominios': condominios,
    })
