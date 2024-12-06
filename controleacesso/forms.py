from django import forms
from django.utils import timezone
from app.models import ControlesAcessos, Apartamentos, Pessoas, Sindicos, TatticaFuncionarios, Condominios,TiposControlesAcessos


class ControleAcessoMoradorForm(forms.ModelForm):
    class Meta:
        model = ControlesAcessos
        fields = [
            'condominio', 'tipos_controles_acesso', 'tattica_funcionario', 'apartamento',
            'pessoa', 'condominios_funcionario', 'sindico', 'entregador', 'realizador',
            'solicitante', 'execucao', 'pedido', 'quantidade', 'valor', 'descricao',
            'identificador', 'agendado', 'promo_status', 'data_prazo', 'data_entrega',
            'data_final', 'data_pagamento', 'comprador_nome', 'comprador_email',
            'comprador_cpf', 'comprador_telefone', 'metodo_pagamento', 'link_boleto',
            'codigo_pagseguro', 'status_pagseguro', 'status', 'created', 'modified'
        ]

    def __init__(self, *args, **kwargs):
        super(ControleAcessoMoradorForm, self).__init__(*args, **kwargs)

        # Filtrando os campos de Apartamento e Pessoa para exibir apenas os ativos
        self.fields['apartamento'].queryset = Apartamentos.objects.filter(status=1)  # Apenas apartamentos ativos
        self.fields['pessoa'].queryset = Pessoas.objects.filter(status=1)  # Apenas pessoas ativas

    # Validação adicional para garantir que 'apartamento' e 'pessoa' não sejam deixados em branco
    def clean_apartamento(self):
        apartamento = self.cleaned_data.get('apartamento')
        if not apartamento:
            raise forms.ValidationError("O campo 'Apartamento' é obrigatório.")
        return apartamento

    def clean_pessoa(self):
        pessoa = self.cleaned_data.get('pessoa')
        if not pessoa:
            raise forms.ValidationError("O campo 'Pessoa' é obrigatório.")
        return pessoa


    # Sobrescrevendo o método 'save' para garantir que as datas 'created' e 'modified' sejam preenchidas corretamente
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)

        # Garantir que os campos 'created' e 'modified' sejam definidos como a data atual
        if not instance.created:
            instance.created = timezone.now()  # Define 'created' com a data atual, se não estiver preenchido
        instance.modified = timezone.now()  # Sempre atualiza 'modified' com a data atual

        # Definir o 'solicitante' como uma combinação do apartamento e pessoa
        apartamento = instance.apartamento
        pessoa = instance.pessoa

        if apartamento and pessoa:
            # Exemplo de como definir 'solicitante' com base no apartamento e pessoa
            instance.solicitante = f'{apartamento.nome_apartamento} - {pessoa.nome_pessoa}'

        if commit:
            instance.save()

        return instance


class ControleAcessoSindicoForms(forms.ModelForm):
    class Meta:
        model = ControlesAcessos
        fields = [
            'condominio', 'tipos_controles_acesso', 'tattica_funcionario',
            'sindico', 'execucao', 'pedido', 'quantidade', 'valor', 'descricao',
            'identificador', 'data_prazo', 'metodo_pagamento', 'status', 'solicitante'
        ]
        # Não incluímos 'created' e 'modified' nos fields, pois serão manipulados no método save()

    def __init__(self, *args, **kwargs):
        super(ControleAcessoSindicoForms, self).__init__(*args, **kwargs)

        # Filtrando os campos para mostrar apenas síndicos ativos
        self.fields['tattica_funcionario'].queryset = Sindicos.objects.filter(status=1)  # Apenas colaboradores ativos
        self.fields['tipos_controles_acesso'].queryset = TiposControlesAcessos.objects.all()
        self.fields['condominio'].queryset = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
        self.fields['sindico'].queryset = Sindicos.objects.filter(status=1)  # Apenas síndicos ativos

    # Validação adicional para garantir que os campos 'condominio' e 'sindico' não sejam deixados em branco
    def clean_condominio(self):
        condominio = self.cleaned_data.get('condominio')
        if not condominio:
            raise forms.ValidationError("O campo 'Condomínio' é obrigatório.")
        return condominio

    def clean_sindico(self):
        sindico = self.cleaned_data.get('sindico')
        if not sindico or not Sindicos.objects.filter(id=sindico.id).exists():
            raise forms.ValidationError("Selecione um síndico válido.")
        return sindico

    # Sobrescrevendo o método 'save' para garantir que as datas 'created' e 'modified' sejam preenchidas corretamente
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)

        # Depuração: Imprimir os dados do formulário para verificação
        print("Dados do formulário antes de salvar:")
        print(f"Condomínio: {instance.condominio}")
        print(f"Síndico: {instance.sindico}")
        print(f"Data de criação: {instance.created}")
        print(f"Data de modificação: {instance.modified}")

        # Garantir que os campos 'created' e 'modified' sejam definidos como a data atual
        if not instance.created:
            instance.created = timezone.now()  # Define 'created' com a data atual, se não estiver preenchido
        instance.modified = timezone.now()  # Sempre atualiza 'modified' com a data atual

        # Definir o 'solicitante' como uma combinação do condomínio e síndico
        condominio = instance.condominio
        sindico = instance.sindico

        if condominio and sindico:
            # Acessar o nome do síndico
            nome_sindico = None
            if sindico.pessoa:
                # Buscar o nome da pessoa relacionada ao síndico
                nome_sindico = sindico.pessoa.nome_pessoa

            if nome_sindico:
                # Definir 'solicitante' como a combinação do nome do condomínio e nome do síndico
                instance.solicitante = f'{condominio.nome_condominio} - {nome_sindico}'
            else:
                # Caso o síndico não tenha uma pessoa associada
                instance.solicitante = f'{condominio.nome_condominio} - Síndico não encontrado'

        if commit:
            instance.save()

        return instance