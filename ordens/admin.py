from django.contrib import admin
from ordens.models import OrdemServico

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'cliente', 'status', 'data_inicio', 'data_finalizacao')
    search_fields = (
        'numero_os',
        'cliente__nome',
        'cliente__telefone',
        'cliente__documento',
    )
    list_filter = ('status', 'data_inicio', 'data_entrega',)
    ordering = ('-data_inicio',)
    readonly_fields = ('numero_os', 'data_inicio', 'created_at', 'updated_at',)
