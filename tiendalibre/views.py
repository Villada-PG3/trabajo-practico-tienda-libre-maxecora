from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class TiendaTemplateView(TemplateView):
    template_name = 'tienda.html'
