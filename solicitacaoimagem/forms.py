from django import forms
from django.utils import timezone
from app.models import (ControlesAcessos, Apartamentos, Pessoas, Sindicos,Imagemcameras,
                        TatticaFuncionarios, Condominios,TiposControlesAcessos,CondominiosFuncionarios)


class SolicitacaoImagemMoradorForm(forms.ModelForm):
    class Meta:
        model = Imagemcameras
        fields = [
            'condominio', 'tattica_funcionario_id', 'apartamento_id', 'pessoa_id',
            'sindico_id', 'condominios_funcionario', 'solicitante', 'cameras',
            'periodo', 'descricao', 'link', 'tipo_gravacao', 'execucao',
            'aprovacao', 'area_sindico', 'status', 'created', 'modified'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrando os campos para exibir apenas os itens ativos, caso aplicável
        self.fields['apartamento_id'].queryset = Apartamentos.objects.filter(status=1)  # Apenas apartamentos ativos
        self.fields['pessoa_id'].queryset = Pessoas.objects.filter(status=1)  # Apenas pessoas ativas

    def clean_apartamento_id(self):
        apartamento_id = self.cleaned_data.get('apartamento_id')
        if not apartamento_id:
            raise forms.ValidationError("O campo 'Apartamento' é obrigatório.")
        return apartamento_id

    def clean_pessoa_id(self):
        pessoa_id = self.cleaned_data.get('pessoa_id')
        if not pessoa_id:
            raise forms.ValidationError("O campo 'Pessoa' é obrigatório.")
        return pessoa_id

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)

        # Garantir que os campos 'created' e 'modified' sejam definidos corretamente
        if not instance.created:
            instance.created = timezone.now()
        instance.modified = timezone.now()

        # Personalizar o campo 'solicitante'
        if instance.apartamento_id and instance.pessoa_id:
            instance.solicitante = f'Apto: {instance.apartamento_id} - Pessoa: {instance.pessoa_id}'

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
        print("ID do síndico enviado:", instance.sindico.id)

        if condominio and sindico:
            # Acessar o nome do síndico
            nome_sindico = None
            if sindico.pessoa:
                # Buscar o nome da pessoa relacionada ao síndico
                nome_sindico = sindico.pessoa.nome_pessoa
                tipos_sindico = sindico.tipos_sindico
            if nome_sindico:
                # Definir 'solicitante' como a combinação do nome do condomínio e nome do síndico
                instance.solicitante = f'{tipos_sindico} - {nome_sindico}'
            else:
                # Caso o síndico não tenha uma pessoa associada
                instance.solicitante = f'{condominio.nome_condominio} - Síndico não encontrado'

        if commit:
            instance.save()

        return instance


class ControleAcessoFuncionarioForms(forms.ModelForm):
    class Meta:
        model = ControlesAcessos
        fields = [
            'condominio', 'tipos_controles_acesso', 'tattica_funcionario',
            'condominios_funcionario', 'execucao', 'pedido', 'quantidade', 'valor', 'descricao',
            'identificador', 'data_prazo', 'metodo_pagamento', 'status', 'solicitante'
        ]
        # Campos criados e modificados não são incluídos porque são gerados automaticamente

    def __init__(self, *args, **kwargs):
        super(ControleAcessoFuncionarioForms, self).__init__(*args, **kwargs)

        # Filtra somente condomínios ativos
        self.fields['condominio'].queryset = Condominios.objects.filter(status=1)

        # Filtra somente funcionários ativos
        self.fields['condominios_funcionario'].queryset = CondominiosFuncionarios.objects.filter(status=1)

        # Configuração do queryset de tipos de controle de acesso
        self.fields['tipos_controles_acesso'].queryset = TiposControlesAcessos.objects.all()

        # Adicionando classes CSS para estilização dos campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_condominio(self):
        """Valida se o campo condomínio foi preenchido."""
        condominio = self.cleaned_data.get('condominio')
        if not condominio:
            raise forms.ValidationError("O campo 'Condomínio' é obrigatório.")
        return condominio

    def clean_condominios_funcionario(self):
        """Valida se um funcionário válido foi selecionado."""
        funcionario = self.cleaned_data.get('condominios_funcionario')
        if not funcionario:
            raise forms.ValidationError("O campo 'Funcionário' é obrigatório.")
        return funcionario

    def save(self, commit=True, *args, **kwargs):
        """Sobrescreve o método save para adicionar lógica personalizada."""
        instance = super().save(commit=False, *args, **kwargs)

        # Define ou atualiza os campos de data
        if not instance.created:
            instance.created = timezone.now()  # Define a data de criação apenas se estiver vazia
        instance.modified = timezone.now()  # Atualiza a data de modificação

        # Configura lógica personalizada (por exemplo, dados do solicitante)
        instance.solicitante = f"Condomínio: {instance.condominio}, Funcionário: {instance.condominios_funcionario}"

        if commit:
            instance.save()
        return instance

class ControleAcessoOutroForms(forms.ModelForm):
    class Meta:
        model = ControlesAcessos
        fields = [
            'condominio', 'tipos_controles_acesso', 'execucao', 'pedido', 'quantidade', 'valor', 'descricao',
            'identificador', 'data_prazo', 'metodo_pagamento', 'status', 'solicitante'
        ]
        # Campos criados e modificados não são incluídos porque são gerados automaticamente

    def __init__(self, *args, **kwargs):
        super(ControleAcessoOutroForms, self).__init__(*args, **kwargs)

        # Filtra somente condomínios ativos
        self.fields['condominio'].queryset = Condominios.objects.filter(status=1)

        # Configuração do queryset de tipos de controle de acesso
        self.fields['tipos_controles_acesso'].queryset = TiposControlesAcessos.objects.all()

        # Adicionando classes CSS para estilização dos campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_condominio(self):
        """Valida se o campo condomínio foi preenchido."""
        condominio = self.cleaned_data.get('condominio')
        if not condominio:
            raise forms.ValidationError("O campo 'Condomínio' é obrigatório.")
        return condominio

    def save(self, commit=True, *args, **kwargs):
        """Sobrescreve o método save para adicionar lógica personalizada."""
        instance = super().save(commit=False, *args, **kwargs)

        # Define ou atualiza os campos de data
        if not instance.created:
            instance.created = timezone.now()  # Define a data de criação apenas se estiver vazia
        instance.modified = timezone.now()  # Atualiza a data de modificação

        # Configura lógica personalizada (por exemplo, dados do solicitante)
        instance.solicitante = f"Condomínio: {instance.condominio}"

        if commit:
            instance.save()
        return instance