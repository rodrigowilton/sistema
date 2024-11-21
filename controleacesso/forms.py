from django import forms
from app.models import ControlesAcessos

class ControleAcessoForm(forms.ModelForm):
    class Meta:
        model = ControlesAcessos
        fields = [
            'condominio', 'tipos_controles_acesso', 'tattica_funcionario', 'apartamento',
            'pessoa', 'condominios_funcionario', 'sindico', 'entregador', 'realizador',
            'solicitante', 'execucao', 'pedido', 'quantidade', 'valor', 'descricao',
            'identificador', 'agendado', 'promo_status', 'data_prazo', 'data_entrega',
            'data_final', 'data_pagamento', 'comprador_nome', 'comprador_email',
            'comprador_cpf', 'comprador_telefone', 'metodo_pagamento', 'link_boleto',
            'codigo_pagseguro', 'status_pagseguro', 'status', 'created', 'modified'
        ]
