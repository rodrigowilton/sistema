from django import forms
from app.models import Sindicos

class SindicoForm(forms.ModelForm):
    class Meta:
        model = Sindicos
        fields = ['condominio', 'pessoa', 'tipos_sindico', 'email_sindico', 'data_inicio', 'data_fim', 'descricao', 'email_permissao', 'status']
