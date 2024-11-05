from django import forms
from app.models import AgendamentoHorarios

class AgendamentoHorariosForm(forms.ModelForm):
    class Meta:
        model = AgendamentoHorarios
        fields = ['area', 'horario_inicio', 'horario_fim']  # Campos que o usuário pode editar
        widgets = {
            'condominio': forms.HiddenInput(),  # Campo oculto, se necessário
        }

    def __init__(self, *args, **kwargs):
        # Se o condomínio estiver sendo passado como argumento, adiciona ao formulário
        self.condominio = kwargs.pop('condominio', None)
        super().__init__(*args, **kwargs)
        if self.condominio:
            self.instance.condominio = self.condominio  # Define o condomínio no objeto da instância

    def save(self, commit=True):
        agendamento = super().save(commit=False)  # Não salva imediatamente
        if self.condominio:
            agendamento.condominio = self.condominio  # Atribui o condomínio ao agendamento
        if commit:
            agendamento.save()  # Salva o objeto se commit for True
        return agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = AgendamentoHorarios
        fields = ['condominio', 'area', 'horario_inicio', 'horario_fim']  # Removendo 'status' dos campos exibidos

    def __init__(self, *args, **kwargs):
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        self.fields['horario_inicio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Horário de Início'})
        self.fields['horario_fim'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Horário de Fim'})
        self.fields['condominio'].widget.attrs.update({'class': 'form-control'})
        self.fields['area'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super(AgendamentoForm, self).save(commit=False)
        instance.status = 1  # Define o status como 1
        if commit:
            instance.save()
        return instance
