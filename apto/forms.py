from django import forms
from app.models import Apartamentos

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamentos
        fields = ['condominio', 'nome_apartamento']
        widgets = {
            'condominio': forms.Select(attrs={'class': 'form-control'}),
            'nome_apartamento': forms.TextInput(attrs={'class': 'form-control'}),
        }
