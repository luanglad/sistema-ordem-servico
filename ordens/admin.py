from django.contrib import admin
from ordens.models import OrdemServico

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'cliente', 'equipamento', 'status', 'valor_orcamento', 'data_inicio', 'data_finalizacao')
    search_fields = (
        'numero_os',
        'cliente__nome',
        'cliente__telefone',
        'cliente__documento',
        'equipamento__nome',
        'equipamento__numero_serie',
        'equipamento__modelo',
    )
    list_filter = ('status', 'data_inicio', 'data_entrega',)
    ordering = ('-data_inicio',)
    readonly_fields = ('numero_os', 'data_inicio', 'data_finalizacao', 'data_entrega', 'created_at', 'updated_at',)
    fieldsets = (
        ('Ordem de Serviço', {
            'fields': ('numero_os', 'status')
        }),
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Equipamento', {
            'fields': ('equipamento',)
        }),
        ('Serviço', {
            'fields': ('defeito', 'observacoes')
        }),
        ('Orçamento', {
            'fields': ('valor_orcamento',)
        }),
        ('Datas', {
            'fields': (
                'data_inicio',
                'data_finalizacao',
                'data_entrega',
            )
        }),
    )

