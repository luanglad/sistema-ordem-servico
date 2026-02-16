from django.contrib import admin
from ordens.models import OrdemServico, Equipamento
from servicos.admin import ServicoExecutadoInline

class OrdemServicoInline(admin.TabularInline):
    model = OrdemServico
    extra = 0
    readonly_fields = ('numero_os', 'status', 'data_inicio')
    show_change_link = True

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('numero_os', 'cliente', 'equipamento', 'status', 'valor_orcamento_formatado', 'valor_total_formatado', 'data_inicio', 'data_finalizacao')
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
    inlines = [ServicoExecutadoInline]

    @admin.display(description='Orçamento')
    def valor_orcamento_formatado(self, obj):
        if obj.valor_orcamento:
            return f'R$ {obj.valor_orcamento:.2f}'
        return 'R$ 0,00'

    @admin.display(description='Total Serviços')
    def valor_total_formatado(self, obj):
        return f'R$ {obj.valor_total:.2f}'


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero_serie', 'cliente', 'quantidade_os', 'ultima_os')
    search_fields = (
        'nome', 
        'numero_serie', 
        'cliente__nome',
    )
    inlines = [OrdemServicoInline]

    @admin.display(description='Qtd OS')
    def quantidade_os(self, obj):
        return obj.ordens_servico.count()
    
    @admin.display(description='Última OS')
    def ultima_os(self, obj):
        ultima = obj.ordens_servico.order_by('-data_inicio').first()
        if ultima:
            return ultima.numero_os
        return '-'