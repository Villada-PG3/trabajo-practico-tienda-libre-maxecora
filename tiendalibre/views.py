from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView
from .models import Producto

class TiendaTemplateView(TemplateView):
    template_name = 'tienda.html'

def home_1(request):
    return HttpResponse("<h1>Bienvenido a la tienda Libre de Maximo Corallo Margosian</h1>")

def home(request):
    productos_destacados = [
        {"nombre": "Bombo", "precio": None, "stock": 10, "marca": "Firulete"},
        {"nombre": "Hilux", "precio": None, "stock": 0, "marca": "Totoya"},
        {"nombre": "Mouse", "precio": None, "stock": 2, "marca": "Genius"},
        {"nombre": "Teclado", "precio": None, "stock": 5, "marca": "Logitech"},
        {"nombre": "Play Station 3", "precio": None, "stock": 1, "marca": "Sony"},
        {"nombre": "Rodilleras", "precio": None, "stock": 0, "marca": "Nike"},
    ]

    contexto = {
        'productos': Producto.objects.all(), 
        'productos_destacados': productos_destacados,
        'titulo': 'Tienda Libre',
        'esta_logueado': True, #False muestra un mensaje que se necesita estar logueado
    }
    return render(request, 'home.html', contexto)

def acerca_de_mi(request):
    return render(request, 'acerca-de-mi.html')