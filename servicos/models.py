from django.db import models
from ordens.models import OrdemServico

class ServicoExecutado(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='servicos_executados'
    )

    descricao = models.TextField(
        help_text='Descrição do serviço realizado'
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Valor referente a esse serviço'
    )

    created_at = models.DateTimeField(
        auto_now_add=True               
    )

    class Meta:
        verbose_name = 'Serviço Executado'
        verbose_name_plural = 'Serviços Executados'

    def __str__(self):
        return f' OS {self.ordem_servico.numero_os} - R${self.valor}'