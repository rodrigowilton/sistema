from django import forms
from app.models import Sindicos, Apartamentos, Condominios

class SindicoForm(forms.ModelForm):
    condominio_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # Campo oculto para o id do condomínio

    class Meta:
        model = Sindicos
        fields = ['condominio', 'pessoa', 'tipos_sindico', 'email_sindico', 'data_inicio', 'data_fim', 'descricao',
                  'email_permissao', 'status', 'apartamento']

    apartamento = forms.ModelChoiceField(
        queryset=Apartamentos.objects.none(),  # Inicialmente vazio, será atualizado pela view
        empty_label="Selecione o Apartamento",
        required=False
    )

    email_permissao = forms.ChoiceField(
        choices=[(1, 'Sim'), (2, 'Não')],  # Define as opções como Sim/Não
        widget=forms.RadioSelect,  # Usando rádio para seleção
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Força o status para 1, sem precisar ser editado no formulário
        self.fields['status'].initial = 1
        self.fields['status'].widget = forms.HiddenInput()  # Oculta o campo status
        self.fields['condominio'].queryset = Condominios.objects.filter(status=1)  # Filtra condomínios ativos
        self.fields['apartamento'].queryset = Apartamentos.objects.none()  # Inicializa apartamento vazio