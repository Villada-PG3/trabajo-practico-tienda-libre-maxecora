from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto


class CatalogoViewsTests(TestCase):
    def test_home_displays_recent_products(self):
        producto = Producto.objects.create(
            nombre='Producto reciente',
            descripcion='Descripción de prueba',
            precio='12.50',
            stock=3,
        )

        response = self.client.get(reverse('tiendalibre:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, producto.nombre)
        self.assertIn(producto, response.context['productos_recientes'])

    def test_catalogo_lists_products_with_category(self):
        categoria = Categoria.objects.create(nombre='Accesorios')
        producto = Producto.objects.create(
            categoria=categoria,
            nombre='Producto de catálogo',
            descripcion='Descripción de prueba',
            precio='12.50',
            stock=3,
        )

        response = self.client.get(reverse('tiendalibre:catalogo'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo.html')
        self.assertContains(response, producto.nombre)
        self.assertIn(producto, response.context['productos'])
