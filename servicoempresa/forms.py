from django import forms
from app.models import EmpresasServicos

class EmpresasServicosForm(forms.ModelForm):
    class Meta:
        model = EmpresasServicos
        fields = ['nome_tipos_empresa', 'cor', 'status']
        widgets = {
            'nome_tipos_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=[(1, 'Ativo'), (0, 'Inativo')], attrs={'class': 'form-control'}),
        }
