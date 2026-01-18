from django.db import models, transaction
from clientes.models import Cliente

class StatusOrdemServico(models.TextChoices):
    AGUARDANDO_ORCAMENTO = 'AG_ORC', 'Aguardando orçamento'
    AGUARDANDO_APROVACAO = 'AG_APR', 'Aguardando aprovação'
    AGUARDANDO_CONSERTO = 'AG_CON', 'Aguardando conserto'
    FINALIZADO = 'FINAL', 'Finalizado'
    ENTREGUE = 'ENTREG', 'Entregue'

class OrdemServico(models.Model):
    numero_os = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text='Número identificador da Ordem de Serviço'
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ordens_servico'
    )

    defeito = models.TextField(
        help_text='Defeito informado pelo cliente'
    )

    observacoes = models.TextField(
        blank=True,
        help_text='Observações técnicas do serviço'
    )

    status = models.CharField(
        max_length=6,
        choices=StatusOrdemServico.choices,
        default=StatusOrdemServico.AGUARDANDO_ORCAMENTO
    )

    data_inicio = models.DateTimeField(
        auto_now_add=True
    )

    data_finalizacao = models.DateTimeField(
        null=True,
        blank=True
    )

    data_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.numero_os:
            with transaction.atomic():
                ultimo = (
                    OrdemServico.objects
                    .select_for_update()
                    .order_by("-id")
                    .first()
                )

                proximo_numero = 1 if not ultimo else ultimo.id + 1
                self.numero_os = f"OS-{proximo_numero:06d}"

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'OS {self.numero_os} - {self.cliente.nome}'