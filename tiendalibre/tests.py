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
        self.assertEqual(len(primera_pagina.context['productos']), 6)
        self.assertEqual(primera_pagina.context['page_obj'].number, 1)
        self.assertTrue(primera_pagina.context['is_paginated'])
        self.assertContains(primera_pagina, '?page=2')
        self.assertEqual(segunda_pagina.status_code, 200)
        self.assertEqual(len(segunda_pagina.context['productos']), 2)
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

    def test_catalogo_search_matches_name_brand_and_description(self):
        matches = [
            Producto.objects.create(
                nombre='Balón especial',
                descripcion='Producto deportivo',
                marca='Marca genérica',
                stock=2,
            ),
            Producto.objects.create(
                nombre='Producto de prueba',
                descripcion='Producto deportivo',
                marca='Marca buscada',
                stock=2,
            ),
            Producto.objects.create(
                nombre='Producto adicional',
                descripcion='Texto de búsqueda',
                marca='Marca genérica',
                stock=2,
            ),
        ]
        Producto.objects.create(
            nombre='Producto no relacionado',
            descripcion='Otro texto',
            marca='Otra marca',
            stock=2,
        )

        for term in ('Balón', 'Marca buscada', 'búsqueda'):
            with self.subTest(term=term):
                response = self.client.get(
                    reverse('tiendalibre:catalogo'),
                    {'q': term},
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.context['productos']), 1)
        self.assertEqual(len(matches), 3)

    def test_category_page_filters_products_and_navbar_shows_category(self):
        categoria = Categoria.objects.create(nombre='Accesorios deportivos')
        producto = Producto.objects.create(
            categoria=categoria,
            nombre='Producto categorizado',
            descripcion='Descripción de prueba',
            stock=3,
        )
        Producto.objects.create(
            nombre='Producto sin categoría',
            descripcion='Descripción de prueba',
            stock=3,
        )

        response = self.client.get(
            reverse('tiendalibre:categoria', args=[categoria.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tiendalibre/categoria.html')
        self.assertEqual(response.context['categoria'], categoria)
        self.assertEqual(list(response.context['productos']), [producto])
        self.assertContains(response, categoria.nombre)
        self.assertContains(response, reverse('tiendalibre:categoria', args=[categoria.slug]))

    def test_category_slug_is_generated_uniquely(self):
        first = Categoria.objects.create(nombre='Ropa deportiva')
        second = Categoria.objects.create(nombre='Ropa-deportiva')

        self.assertEqual(first.slug, 'ropa-deportiva')
        self.assertEqual(second.slug, 'ropa-deportiva-2')
