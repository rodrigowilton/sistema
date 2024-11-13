from django import forms
from app.models import CondominiosFuncionarios, Condominios, TiposFuncionarios


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = CondominiosFuncionarios
        fields = [
            'condominio', 'tipos_condominios_funcionario', 'nome_condominios_funcionario',
            'telefone1', 'telefone2', 'email', 'hora_inicio', 'hora_fim',
            'hora_inicio_sab', 'hora_fim_sab', 'observacao'
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
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['condominio'].queryset = Condominios.objects.filter(status=1)  # Apenas condomínios ativos
        self.fields['tipos_condominios_funcionario'].queryset = TiposFuncionarios.objects.filter(
            status=1)  # Tipos de funcionário ativos
