from django import forms
from app.models import Funcionarios

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionarios
        fields = ['empresa', 'tipos_funcionario', 'nome_funcionario', 'cargo', 'cpf', 'rg', 'telefone', 'celular', 'email', 'imagem_prestador', 'status']
