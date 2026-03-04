from django.conf import settings

def empresa_info(request):
    return {
        'NOME_EMPRESA': settings.NOME_EMPRESA,
        'CNPJ': settings.CNPJ,
        'TELEFONE': settings.TELEFONE,
    }