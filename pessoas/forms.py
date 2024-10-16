from django import forms
from app.models import Pessoas, TiposPessoas


class PessoasForm(forms.ModelForm):
    tipos_pessoa = forms.ModelMultipleChoiceField(
        queryset=TiposPessoas.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Pessoas
        fields = '__all__'
