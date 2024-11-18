from django import forms
from app.models import CondominiosFuncionarios, TiposCondominiosFuncionarios

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = CondominiosFuncionarios
        fields = [
            'condominio', 'tipos_condominios_funcionario', 'nome_condominios_funcionario',
            'telefone1', 'telefone2', 'email', 'hora_inicio', 'hora_fim',
            'hora_inicio_sab', 'hora_fim_sab', 'observacao', 'status'
        ]
        labels = {
            'condominio': 'Condomínio',
            'tipos_condominios_funcionario': 'Tipo de Funcionário',
            'nome_condominios_funcionario': 'Nome',
            'telefone1': 'Telefone 1',
            'telefone2': 'Telefone 2',
            'email': 'E-mail',
            'hora_inicio': 'Hora Início (Seg-Sex)',
            'hora_fim': 'Hora Fim (Seg-Sex)',
            'hora_inicio_sab': 'Hora Início (Sábado)',
            'hora_fim_sab': 'Hora Fim (Sábado)',
            'observacao': 'Observação'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Oculta e define o valor padrão para o campo status
        self.fields['status'].initial = 1
        self.fields['status'].widget = forms.HiddenInput()
        # Filtra apenas os tipos ativos
        self.fields['tipos_condominios_funcionario'].queryset = TiposCondominiosFuncionarios.objects.filter(status=1)
