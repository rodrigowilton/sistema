from django import forms
from app.models import Feriados

class FeriadoForm(forms.ModelForm):
    class Meta:
        model = Feriados
        fields = ['nome', 'data']  # Adicione outros campos conforme necessário
