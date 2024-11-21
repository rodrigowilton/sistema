from django import template
from datetime import date, timedelta
import datetime

register = template.Library()

# Função para calcular dias úteis
def calcular_dias_uteis(data_inicial, data_final):
    dias_uteis = 0
    current_day = data_inicial
    while current_day <= data_final:
        # Verifique se o dia não é sábado (5) ou domingo (6)
        if current_day.weekday() < 5:
            dias_uteis += 1
        current_day += timedelta(days=1)
    return dias_uteis

@register.filter
def dias_uteis_mais(data_criacao, limite_dias):
    hoje = datetime.date.today()  # Hoje como datetime.date
    if data_criacao:
        # Se data_criacao for datetime, converta para datetime.date
        if isinstance(data_criacao, datetime.datetime):
            data_criacao = data_criacao.date()

        # Calcula a data de X dias úteis a partir da data de criação
        data_limite = data_criacao
        dias_uteis = 0
        while dias_uteis < limite_dias:
            data_limite += timedelta(days=1)
            if data_limite.weekday() < 5:  # Se for um dia útil (segunda a sexta)
                dias_uteis += 1

        # Verifique se a data limite já passou
        if hoje > data_limite:
            return True
    return False

@register.filter
def is_vencido(controle):
    if controle.data_prazo and controle.created:
        limite_dias = 3  # Definir o limite de 3 dias úteis
        # Calcula a data de 3 dias úteis após a criação
        if dias_uteis_mais(controle.created, limite_dias):
            return True
    return False
