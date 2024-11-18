from django import forms
from app.models import Empresas

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'telefone', 'celular',
            'email', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade',
            'uf', 'cep', 'status', 'website'
        ]
        widgets = {
            'status': forms.Select(choices=[(1, 'Ativo'), (0, 'Inativo')]),
        }
