from django import forms
from django.utils import timezone

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
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        # Garantir que status seja 1 (oculto e sempre 1)
        self.fields['status'].initial = 1
        self.fields['status'].widget = forms.HiddenInput()
        # Garanta que o queryset seja de TiposCondominiosFuncionarios com status=1
        self.fields['tipos_condominios_funcionario'].queryset = TiposCondominiosFuncionarios.objects.filter(status=1)

    def save(self, commit=True):
        # Sobrescreve o método save() para garantir que 'created' seja preenchido
        instance = super(FuncionarioForm, self).save(commit=False)
        if not instance.created:
            instance.created = timezone.now()  # Define a data/hora atual
        if commit:
            instance.save()
        return instance

    def clean_tipos_condominios_funcionario(self):
        tipos_condominios_funcionario = self.cleaned_data.get('tipos_condominios_funcionario')
        if not tipos_condominios_funcionario:
            raise forms.ValidationError('O tipo de funcionário é obrigatório.')
        return tipos_condominios_funcionario
