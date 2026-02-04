from django.db import models
from ordens.models import OrdemServico

class Servico(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        help_text='Nome do serviço. Ex: Rebbaling'
    )

    descricao = models.TextField(
        blank=True,
        help_text='Descrição detalhada do serviço' 
    )

    preco_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Preço padrão do serviço'
    )

    ativo = models.BooleanField(
        default=True,
        help_text='Defina se o serviço está disponível'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True   
    )

    class Meta:
        ordering = ['nome']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f'Serviço: {self.nome}'
    
class ServicoExecutado(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='servicos_executados'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name='execucoes'
    )

    quantidade = models.PositiveIntegerField(
        default=1 
    )

    valor_cobrado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Valor cobrado por este serviço'
    )

    observacoes = models.TextField(
        blank=True 
    )

    created_at = models.DateTimeField(
        auto_now_add=True               
    )

    class Meta:
        verbose_name = 'Serviço Executado'
        verbose_name_plural = 'Serviços Executados'

    def __str__(self):
        return f'{self.servico.nome} - {self.ordem_servico.numero_os}'