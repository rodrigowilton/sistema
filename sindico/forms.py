from django import forms
from app.models import Sindicos, Apartamentos

class SindicoForm(forms.ModelForm):
    class Meta:
        model = Sindicos
        fields = ['condominio', 'pessoa', 'tipos_sindico', 'email_sindico', 'data_inicio', 'data_fim', 'descricao', 'email_permissao', 'status', 'apartamento']

    apartamento = forms.ModelChoiceField(
        queryset=Apartamentos.objects.none(),  # Será atualizado na view
        empty_label="Selecione o Apartamento",
        required=False
    )
