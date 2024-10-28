from django import forms
from app.models import Areas

class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = [
            'condominio', 'nome_area', 'andar', 'limite_pessoas', 'valor',
            'hora_min', 'hora_max', 'antecedencia_min', 'antecedencia_max',
            'tipo_reserva', 'intervalo_entre_reservas', 'max_abertos',
            'hora_inicio_permitido', 'hora_fim_permitido', 'necessita_aprovacao',
            'status'
        ]

class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = '__all__'  # ou especifique campos
