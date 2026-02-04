from django.db import models

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