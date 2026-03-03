from django.urls import path
from . import views

urlpatterns = [
    path('os/<int:pk>/pdf/', views.gerar_pdf_os, name='gerar_pdf_os'),
]