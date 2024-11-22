from django import forms
from django.utils import timezone
from app.models import ControlesAcessos, Apartamentos, Pessoas

class ControleAcessoForm(forms.ModelForm):
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
        super(ControleAcessoForm, self).__init__(*args, **kwargs)

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
