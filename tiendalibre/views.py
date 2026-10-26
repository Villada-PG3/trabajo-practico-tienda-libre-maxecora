from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q
from .models import Categoria, Producto

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
    paginate_by = 6

    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria').all()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query)
                | Q(marca__icontains=query)
                | Q(descripcion__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['is_paginated']:
            context['page_range'] = context['paginator'].get_elided_page_range(
                context['page_obj'].number
            )
        return context


class CategoriaView(ListView):
    model = Producto
    template_name = 'tiendalibre/categoria.html'
    context_object_name = 'productos'
    paginate_by = 6

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Producto.objects.filter(categoria=self.categoria).select_related('categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        if context['is_paginated']:
            context['page_range'] = context['paginator'].get_elided_page_range(
                context['page_obj'].number
            )
        return context


class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'detalle.html'
    context_object_name = 'producto'
    queryset = Producto.objects.select_related('categoria')

def home_1(request):
    return HttpResponse("<h1>Bienvenido a la tienda Libre de Maximo Corallo Margosian</h1>")

def acerca_de_mi(request):
    return render(request, 'acerca-de-mi.html')
