from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import OrdemServico
from django.conf import settings
from weasyprint import HTML
from pathlib import Path

context = {
    "NOME_EMPRESA": settings.NOME_EMPRESA,
    "CNPJ": settings.CNPJ,
    "TELEFONE": settings.TELEFONE,
}

def gerar_pdf_os(request, pk):
    os_obj = get_object_or_404(OrdemServico, pk=pk)

    logo_horizontal_path = (
        Path(settings.BASE_DIR) / 'static' / 'img' / 'logo_horizontal.png'
    ).resolve().as_uri()

    logo_principal_path = (
        Path(settings.BASE_DIR) / 'static' / 'img' / 'logo_principal.png'
    ).resolve().as_uri()

    html_string = render_to_string(
        'ordens/pdf/ordem_servico.html',
        {
            'os': os_obj,
            'logo_horizontal_path': logo_horizontal_path,
            'logo_principal_path': logo_principal_path,
            'request': request,
            'context': context,
        }
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=os_{os_obj.numero_os}.pdf'

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')  
    ).write_pdf(response)

    return response