from django import forms
from app.models import AgendamentoHorarios, Agendamentos

class AgendamentoHorariosForm(forms.ModelForm):
    class Meta:
        model = AgendamentoHorarios
        fields = ['condominio', 'area', 'horario_inicio', 'horario_fim', 'status']

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = AgendamentoHorarios
        fields = ['condominio', 'area', 'horario_inicio', 'horario_fim', 'status']  # Incluindo os campos necessários

    def __init__(self, *args, **kwargs):
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        self.fields['horario_inicio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Horário de Início'})
        self.fields['horario_fim'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Horário de Fim'})
        self.fields['condominio'].widget.attrs.update({'class': 'form-control'})
        self.fields['area'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})