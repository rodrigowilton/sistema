from django import template
from datetime import timedelta, date, datetime

register = template.Library()

# Função para calcular a data com dias úteis adicionados
def adicionar_dias_uteis(data_inicial, dias_uteis):
    dias_adicionados = 0
    while dias_adicionados < dias_uteis:
        data_inicial += timedelta(days=1)
        if data_inicial.weekday() < 5:  # Dias úteis: segunda a sexta
            dias_adicionados += 1
    return data_inicial

@register.filter
def dias_uteis_mais(data_criacao, limite_dias):
    if data_criacao:
        # Normaliza a data para garantir que seja do tipo `date`
        if isinstance(data_criacao, datetime):
            data_criacao = data_criacao.date()

        # Calcula a data limite com base nos dias úteis
        data_limite = adicionar_dias_uteis(data_criacao, limite_dias)

        # Verifica se o prazo foi ultrapassado
        return date.today() > data_limite
    return False

@register.filter
def is_vencido(controle):
    if controle.data_prazo and controle.created:
        return dias_uteis_mais(controle.created, 3)
    return False
