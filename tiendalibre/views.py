from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.views.generic import ListView, TemplateView
from .models import Producto

class TiendaTemplateView(TemplateView):
    template_name = 'tienda.html'

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'productos_destacados': [
                {"nombre": "Bombo", "precio": None, "stock": 10, "marca": "Firulete"},
                {"nombre": "Hilux", "precio": None, "stock": 0, "marca": "Totoya"},
                {"nombre": "Mouse", "precio": None, "stock": 2, "marca": "Genius"},
                {"nombre": "Teclado", "precio": None, "stock": 5, "marca": "Logitech"},
                {"nombre": "Play Station 3", "precio": None, "stock": 1, "marca": "Sony"},
                {"nombre": "Rodilleras", "precio": None, "stock": 0, "marca": "Nike"},
            ],
            'productos_recientes': Producto.objects.select_related('categoria').order_by(
                '-fecha_creacion', '-id'
            )[:3],
            'titulo': 'Tienda Libre',
            'esta_logueado': True,
        })
        return context

class CatalogoView(ListView):
    model = Producto
    template_name = 'catalogo.html'
    context_object_name = 'productos'
    queryset = Producto.objects.select_related('categoria').all()

def home_1(request):
    return HttpResponse("<h1>Bienvenido a la tienda Libre de Maximo Corallo Margosian</h1>")

def acerca_de_mi(request):
    return render(request, 'acerca-de-mi.html')

def detalle_producto(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria'),
        pk=pk,
    )
    context = {'producto': producto,}
    return render(request, 'detalle.html', context)