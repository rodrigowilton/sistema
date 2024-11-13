from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from app.models import Sindicos, Apartamentos, Condominios, TiposSindicos, Pessoas  # Importe o modelo Condominios aqui
from .forms import SindicoForm
from django.http import JsonResponse
from django.views import View  # Adicione esta linha para importar a classe View

@login_required
def lista_sindicos(request):
    sindicos = Sindicos.objects.filter(status=1, condominio__status=1).order_by('condominio__nome_condominio')
    return render(request, 'lista_sindicos.html', {'sindicos': sindicos})


def criar_sindico(request):
	if request.method == 'POST':
		form = SindicoForm(request.POST)
		
		# Filtra os tipos de síndico ativos (status=1)
		tipos_sindico = TiposSindicos.objects.filter(status=1)
		
		# Atualiza o queryset de apartamentos com base no condomínio selecionado
		condominio_id = request.POST.get('condominio')
		if condominio_id:
			form.fields['apartamento'].queryset = Apartamentos.objects.filter(condominio_id=condominio_id, status=1)
		
		if form.is_valid():
			form.save()
			messages.success(request, 'Síndico criado com sucesso.')
			return redirect('lista_sindicos')
		else:
			messages.error(request, 'Houve um erro no cadastro. Verifique os dados e tente novamente.')
	
	else:
		form = SindicoForm()
	
	# Filtra os condomínios ativos
	condominios = Condominios.objects.filter(status=1)
	
	# Filtra os tipos de síndico ativos (status=1)
	tipos_sindico = TiposSindicos.objects.filter(status=1)
	
	return render(request, 'criar_sindico.html', {
		'form': form,
		'condominios': condominios,
		'tipos_sindico': tipos_sindico  # Adiciona tipos_sindico no contexto
	})


# Endpoint para buscar apartamentos pelo condomínio selecionado
def get_apartamentos_por_condominio(request, condominio_id):
    apartamentos = Apartamentos.objects.filter(condominio_id=condominio_id).values('id', 'nome_apartamento')
    return JsonResponse(list(apartamentos), safe=False)

def get_pessoas_por_apartamento(request, apartamento_id):
    pessoas = Pessoas.objects.filter(apartamento_id=apartamento_id).values('id', 'nome_pessoa')
    return JsonResponse(list(pessoas), safe=False)

def editar_sindico(request, sindico_id):
    sindico = get_object_or_404(Sindicos, id=sindico_id)

    # Obter apartamentos associados ao condomínio do síndico
    apartamentos = Apartamentos.objects.filter(condominio=sindico.condominio, status=1)
    pessoas = Pessoas.objects.none()

    # Se o síndico já tem uma pessoa associada, filtrar as pessoas associadas ao apartamento
    if sindico.pessoa:
        pessoas = Pessoas.objects.filter(apartamento=sindico.pessoa.apartamento)

    tipos_sindico = TiposSindicos.objects.all()

    if request.method == 'POST':
        form = SindicoForm(request.POST, instance=sindico)

        # Verificando a validade do formulário
        if form.is_valid():
            print(f"Formulário válido! Email Permissão: {form.cleaned_data['email_permissao']}")

            # Atribuindo o id do condomínio do formulário
            condominio_id = form.cleaned_data.get('condominio_id')  # Agora acessamos depois de is_valid()
            if condominio_id:
                try:
                    # Atribuindo o valor do condomínio
                    sindico.condominio = Condominios.objects.get(id=condominio_id)
                    print(f"Condomínio ID atribuído corretamente: {condominio_id}")
                except Condominios.DoesNotExist:
                    form.add_error('condominio', 'Condomínio não encontrado.')

            apartamento_id = request.POST.get('apartamento_id')
            if apartamento_id:
                try:
                    apartamento = Apartamentos.objects.get(id=apartamento_id)
                    sindico.apartamento = apartamento
                except Apartamentos.DoesNotExist:
                    form.add_error('apartamento', 'Apartamento não encontrado.')

            # Processando o campo 'email_permissao'
            email_permissao = request.POST.get('email_permissao')
            if email_permissao:
                sindico.email_permissao = int(email_permissao)

            # Salvando as alterações
            try:
                form.save()
                messages.success(request, 'Síndico atualizado com sucesso.')
                return redirect('lista_sindicos')
            except IntegrityError as e:
                print(f"Erro de integridade: {e}")
                form.add_error(None, "Erro ao salvar. Verifique se todos os campos obrigatórios estão preenchidos.")
        else:
            print(f"Erro ao salvar: {form.errors}")

    else:
        # Quando o método for GET, criamos o formulário a partir do objeto 'sindico'
        form = SindicoForm(instance=sindico)
        form.fields['apartamento'].queryset = apartamentos

        # Se o síndico já tiver uma pessoa e um apartamento, preenchemos o campo do apartamento
        if sindico.pessoa and sindico.pessoa.apartamento:
            form.fields['apartamento'].initial = sindico.pessoa.apartamento.id

        # Passando o id do condomínio para o campo oculto no formulário
        form.fields['condominio_id'].initial = sindico.condominio.id
        print(f"Condomínio ID no formulário ao renderizar: {form.fields['condominio_id'].initial}")

    return render(request, 'editar_sindico.html', {
        'form': form,
        'sindico': sindico,
        'apartamentos': apartamentos,
        'pessoas': pessoas,
        'tipos_sindico': tipos_sindico,
    })


def consultar_sindico(request, sindico_id):
	# Obtém o objeto "sindico" com base no id
	sindico = get_object_or_404(Sindicos, id=sindico_id)
	
	# Obtém todas as pessoas e tipos de síndico para preencher os campos do formulário
	pessoas = Pessoas.objects.all()  # Modifique para filtrar conforme necessário
	tipos_sindico = TiposSindicos.objects.all()  # Modifique conforme o modelo
	
	if request.method == 'POST':
		# Caso o formulário tenha sido enviado, atualize os dados
		sindico.pessoa = get_object_or_404(Pessoas, id=request.POST.get('pessoa'))
		sindico.tipos_sindico = get_object_or_404(TiposSindicos, id=request.POST.get('tipos_sindico'))
		sindico.email_sindico = request.POST.get('email_sindico')
		sindico.data_inicio = request.POST.get('data_inicio')
		sindico.data_fim = request.POST.get('data_fim')
		sindico.descricao = request.POST.get('descricao')
		sindico.email_permissao = request.POST.get('email_permissao')
		sindico.save()
	
	# Redirecionar ou exibir uma mensagem de sucesso
	# Exemplo: return redirect('success_page') ou exibir uma mensagem de sucesso
	
	return render(request, 'consultar_sindico.html', {
		'sindico': sindico,
		'pessoas': pessoas,
		'tipos_sindico': tipos_sindico,
	})


class DeletarSindico(View):
    def get(self, request, pk):
        # Corrija para usar 'pk' em vez de 'sindico_id'
        sindico = get_object_or_404(Sindicos, pk=pk)  # Buscar o síndico pelo pk
        return render(request, 'deletar_sindico.html', {'sindico': sindico})

    def post(self, request, pk):
        sindico = get_object_or_404(Sindicos, pk=pk)  # Buscar o síndico novamente
        sindico.status = 2  # Mudar o status para 2 (por exemplo, "desativado")
        sindico.save()
        return redirect('lista_sindicos')  # Redireciona para a lista de síndicos