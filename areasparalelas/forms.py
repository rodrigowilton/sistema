from django import forms
from app.models import AreasParalelas

class AreasParalelasForm(forms.ModelForm):
    class Meta:
        model = AreasParalelas
        fields = ['area', 'area2', 'tipo']  # Ajuste conforme necessário

    tipo = forms.ChoiceField(choices=[
        (1, 'Concorrente'),
        (2, 'Conjunta')
    ])
