from django import forms
from app.models import AreasParalelas

class AreasParalelasForm(forms.ModelForm):
    class Meta:
        model = AreasParalelas
        fields = ['area', 'area2', 'tipo', 'status']  # Especifique os campos que deseja incluir no formulário
        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'}),
            'area2': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'choices': [
                    (1, 'Concorrente'),
                    (2, 'Conjunto')
                ]
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
