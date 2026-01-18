from django.db import models

class TipoCliente(models.TextChoices):
    PESSOA_FISICA = 'PF', 'Pessoa Física'
    PESSOA_JURIDICA = 'PJ', 'Pessoa Jurídica'

class Cliente(models.Model):
    nome = models.CharField(
        max_length=100,
        help_text='Nome do cliente ou razão social'
    )

    tipo = models.CharField(
        max_length=2,
        choices=TipoCliente.choices,
        default=TipoCliente.PESSOA_FISICA,
        help_text='Defina se o cliente é pessoa física ou jurídica'
    )

    documento = models.CharField(
        max_length=18,
        unique=True,
        help_text='CPF ou CNPJ do cliente'
    )

    telefone = models.CharField(
        max_length=20,
        help_text='Telefone principal para contato'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    def __str__(self) -> str:
        return f'Cliente: {self.nome} ({self.get_tipo_display()})'