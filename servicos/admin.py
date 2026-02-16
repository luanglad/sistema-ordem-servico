import nested_admin
from django.contrib import admin
from .models import ServicoExecutado, FotoServico

class FotoServicoInline(nested_admin.NestedTabularInline):
    model = FotoServico
    extra = 1

class ServicoExecutadoInline(nested_admin.NestedTabularInline):
    model = ServicoExecutado
    extra = 1
    inlines = [FotoServicoInline]