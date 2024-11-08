# Em forms.py
from django import forms
from app.models import Agendamentos

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamentos
        fields = [
            'condominio', 'area', 'apartamento', 'tattica_funcionario', 'pessoa',
            'data_inicio', 'data_fim', 'hora_inicio', 'hora_fim', 'mudanca',
            'outrostext', 'adm', 'zelador', 'status'
        ]
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'outrostext': forms.Textarea(attrs={'rows': 3}),
        }
