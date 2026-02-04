from django.core.exceptions import ValidationError
from django.db import models, transaction
from clientes.models import Cliente
from django.utils import timezone

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

    nome_equipamento = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Ex: Playstation 5, Xbox Series X'
    )

    modelo_equipamento = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Modelo ou versão do equipamento'
    )

    numero_serie = models.CharField(
        max_length=100,
        null=True,
        blank=True,
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

    valor_orcamento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
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

    def clean(self):
        if self.status == StatusOrdemServico.FINALIZADO and not self.valor_orcamento:
            raise ValidationError('Não é possível finalizar a OS sem definir o valor do orçamento.')
        
        if self.status == StatusOrdemServico.ENTREGUE and self.data_finalizacao is None:
            raise ValidationError('Não é possível entregar a OS sem finalizá-la.')

    def save(self, *args, **kwargs):
        self.full_clean()

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

        if (self.status == StatusOrdemServico.FINALIZADO and self.data_finalizacao is None):
            self.data_finalizacao = timezone.now()

        if (self.status == StatusOrdemServico.ENTREGUE and self.data_entrega is None):
            self.data_entrega = timezone.now()            

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'OS {self.numero_os} - {self.cliente.nome}'