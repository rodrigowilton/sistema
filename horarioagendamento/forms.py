from django import forms
from app.models import AgendamentoHorarios

class AgendamentoHorariosForm(forms.ModelForm):
    class Meta:
        model = AgendamentoHorarios
        fields = ['condominio', 'area', 'horario_inicio', 'horario_fim', 'status']
