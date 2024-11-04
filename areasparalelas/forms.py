from django import forms
from app.models import AreasParalelas, Areas, Condominios


class AreasParalelasForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Areas.objects.none(), label='Área 1')
    area2 = forms.ModelChoiceField(queryset=Areas.objects.none(), label='Área 2')
    tipo = forms.ChoiceField(choices=[
        (1, 'Concorrente'),
        (2, 'Conjunta')
    ])

    class Meta:
        model = AreasParalelas
        fields = ['area', 'area2', 'tipo']

    def __init__(self, *args, **kwargs):
        selected_condominio = kwargs.pop('selected_condominio', None)
        super().__init__(*args, **kwargs)

        # Filtra as áreas com base no condomínio selecionado
        if selected_condominio:
            self.fields['area'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)
            self.fields['area2'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)

    def label_from_instance(self, obj):
        return obj.nome_area  # Exibe apenas o nome da área


class EditarAreaParalelaForm(forms.ModelForm):
    class Meta:
        model = AreasParalelas
        fields = ['area', 'area2', 'tipo']

    def __init__(self, *args, **kwargs):
        selected_condominio = kwargs.pop('selected_condominio', None)
        super().__init__(*args, **kwargs)

        # Filtra as áreas com base no condomínio selecionado
        if selected_condominio:
            self.fields['area'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)
            self.fields['area2'].queryset = Areas.objects.filter(condominio_id=selected_condominio, status=1)

    def label_from_instance(self, obj):
        return obj.nome_area  # Exibe o nome da área