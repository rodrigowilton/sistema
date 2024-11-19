from django import forms
from app.models import EmpresasServicosEmpresas

class PrestadorForm(forms.ModelForm):
    class Meta:
        model = EmpresasServicosEmpresas
        fields = ["empresas_servico", "empresa", "status"]
