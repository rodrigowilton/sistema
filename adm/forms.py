from django import forms
from app.models import Condominios

class CondominiosForm(forms.ModelForm):
    class Meta:
        model = Condominios
        fields = '__all__'  # ou defina os campos que você deseja incluir
        widgets = {
            'nome_condominio': forms.TextInput(attrs={'class': 'form-control'}),
            'data_condominio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'ramal_condominio': forms.TextInput(attrs={'class': 'form-control'}),
            'ramal_interno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'internet': forms.Select(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-control'}),
            'suporteunidade': forms.Select(attrs={'class': 'form-control'}),
            'entregadores_norma': forms.Select(attrs={'class': 'form-control'}),
            'prestadores_norma': forms.Select(attrs={'class': 'form-control'}),
            'reservas_norma': forms.Select(attrs={'class': 'form-control'}),
            'mudancas_norma': forms.Select(attrs={'class': 'form-control'}),
            'responsavel_tattica': forms.Select(attrs={'class': 'form-control'}),
            'norma_observacao': forms.Textarea(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'website_agendamento': forms.TextInput(attrs={'class': 'form-control'}),
            'financeiro_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'financeiro_email': forms.EmailInput(attrs={'class': 'form-control'}),
            # Adicione mais campos conforme necessário
        }
