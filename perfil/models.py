from datetime import datetime
from django.db import models

# from PIL import Image


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valores

        valores = (
            Valores.objects.filter(categoria__id=self.id)
            .filter(data__month=datetime.now().month)
            .filter(tipo='S')
        )
        # print(valores)
        # return 11
        # return self.valor_planejamento

# Outra forma utilizando o aggregate()
#     def total_gasto(self):
#         from extrato.models import Valores
#         valores = Valores.objects.filter(
#             categoria__id=self.id).filter(
#                 data__month=datetime.now().month).aggregate(Sum('valor'))
#         return valores['valor__sum'] if valores['valor__sum'] else 0

        total_valor = 0
        for valor in valores:
            total_valor += valor.valor
        return total_valor

    # Desafio: transf linha 49/50/51/52 em uma unica linha func/utils

    def calcula_percentual_gasto_por_categoria(self):
        # return (self.total_gasto() * 100) / self.valor_planejamento

        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except ZeroDivisionError:
            return 0


class Conta(models.Model):
    banco_choices = (
        ("NU", "Nubank"),
        ("CE", "Caixa economica"),
        ("PS", "PagSeguro"),
        ("MP", "Mercado Pago"),
        ("BB", "Banco Brasil"),
        ("BI", "Banco Itau"),
    )

    tipo_choices = (
        ("pf", "Pessoa fisica"),
        ("pj", "Pessoa juridica"),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido
