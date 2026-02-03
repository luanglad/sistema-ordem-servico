from django.contrib import admin
from clientes.models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'telefone', 'tipo', 'created_at',)
    search_fields = ('nome', 'documento', 'telefone')
    list_filter = ('tipo', 'created_at')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at',)