from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView

class TiendaTemplateView(TemplateView):
    template_name = 'tienda.html'

def home_1(request):
    return HttpResponse("<h1>Bienvenido a la tienda Libre</h1>")

def home(request):
    return render(request, 'home.html')