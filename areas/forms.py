from django import forms
from app.models import Areas

class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = '__all__'  # ou especifique campos
