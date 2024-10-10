from django import forms
from app.models import Condominios

class CondominiumForm(forms.ModelForm):
    class Meta:
        model = Condominios
        fields = [
            'nome_condominio',
            'data_condominio',
            'cnpj',
            'logradouro',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'uf',
            'cep',
            'ramal_condominio',
            'ramal_interno',
            'telefone',
            'internet',
            'unidade',
            'suporteunidade',
            'entregadores_norma',
            'prestadores_norma',
            'reservas_norma',
            'mudancas_norma',
            'responsavel_tattica',
            'norma_observacao',
            'website',
            'website_agendamento',
            'financeiro_responsavel',
            'financeiro_email',
        ]
        widgets = {
            'data_condominio': forms.DateInput(attrs={'type': 'date'}),
            'norma_observacao': forms.Textarea(attrs={'rows': 4}),
            'website': forms.URLInput(attrs={'placeholder': 'http://exemplo.com'}),
            'website_agendamento': forms.URLInput(attrs={'placeholder': 'http://exemplo.com/agendamento'}),
        }

    def __init__(self, *args, **kwargs):
        super(CondominiumForm, self).__init__(*args, **kwargs)
        # Se precisar de opções dinâmicas para ForeignKeys
        # Exemplo: self.fields['internet'].queryset = Internets.objects.all()
