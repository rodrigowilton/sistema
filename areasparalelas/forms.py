# app/forms.py

from django import forms
from app.models import AreasParalelas, Areas

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
        # Certifique-se de retornar apenas o nome da área
        return obj.nome_area  # Altere isso para o campo que deseja exibir


class EditAreaParalelaForm(forms.ModelForm):
    class Meta:
        model = AreasParalelas
        fields = ['area', 'area2', 'tipo']  # campos que você quer editar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preencher as opções dos campos 'area' e 'area2'
        self.fields['area'].queryset = Areas.objects.all()  # Pode filtrar conforme necessário
        self.fields['area2'].queryset = Areas.objects.all()  # Pode filtrar conforme necessário