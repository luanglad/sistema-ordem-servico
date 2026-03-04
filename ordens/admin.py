from ordens.models import OrdemServico, StatusOrdemServico, Equipamento
from servicos.admin import ServicoExecutadoInline
from django.utils.html import format_html
from django.contrib import messages
from django.contrib import admin
from django.urls import reverse
import nested_admin

class OrdemServicoInline(admin.TabularInline):
    model = OrdemServico
    extra = 0
    readonly_fields = ('numero_os', 'status', 'data_inicio')
    show_change_link = True

@admin.register(OrdemServico)
class OrdemServicoAdmin(nested_admin.NestedModelAdmin):
    list_display = ('numero_os', 'cliente', 'equipamento', 'status', 'valor_orcamento_formatado', 'valor_total_formatado', 'data_inicio', 'data_finalizacao', 'botao_pdf',)
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
    
    @admin.display(description='PDF')
    def botao_pdf(self, obj):
        if obj.status in [StatusOrdemServico.ENTREGUE, StatusOrdemServico.FINALIZADO]:
            url = reverse('gerar_pdf_os', args=[obj.pk])
            return format_html(
                '<a target="_blank" '
                'style="padding:4px 8px;background:#0d2c6c;color:white;border-radius:4px;text-decoration:none;" '
                'href="{}">PDF</a>',
                url
            )
        return format_html(
            '<span style="color:gray;">Indisponível</span>'
        )

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