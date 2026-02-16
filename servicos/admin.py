from django.contrib import admin
from servicos.models import ServicoExecutado

class ServicoExecutadoInline(admin.TabularInline):
    model = ServicoExecutado
    extra = 1
