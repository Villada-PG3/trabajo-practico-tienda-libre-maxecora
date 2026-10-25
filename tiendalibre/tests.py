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

    def test_catalogo_paginates_six_products_per_page(self):
        productos = [
            Producto.objects.create(
                nombre=f'Producto {numero:02}',
                descripcion='Descripción de prueba',
                precio='12.50',
                stock=3,
            )
            for numero in range(1, 9)
        ]

        primera_pagina = self.client.get(reverse('tiendalibre:catalogo'))
        segunda_pagina = self.client.get(
            reverse('tiendalibre:catalogo'),
            {'page': 2},
        )

        self.assertEqual(primera_pagina.status_code, 200)
        self.assertEqual(primera_pagina.context['productos'].count(), 6)
        self.assertEqual(primera_pagina.context['page_obj'].number, 1)
        self.assertTrue(primera_pagina.context['is_paginated'])
        self.assertContains(primera_pagina, '?page=2')
        self.assertEqual(segunda_pagina.status_code, 200)
        self.assertEqual(segunda_pagina.context['productos'].count(), 2)
        self.assertEqual(segunda_pagina.context['page_obj'].number, 2)
        for producto in productos[:6]:
            self.assertContains(primera_pagina, producto.nombre)
        for producto in productos[6:]:
            self.assertContains(segunda_pagina, producto.nombre)

    def test_detalle_producto_uses_detail_view(self):
        producto = Producto.objects.create(
            nombre='Producto detallado',
            descripcion='Descripción de prueba',
            precio='12.50',
            stock=3,
        )

        response = self.client.get(
            reverse('tiendalibre:detalle_producto', args=[producto.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detalle.html')
        self.assertEqual(response.context['producto'], producto)
        self.assertContains(response, producto.nombre)
