from django.contrib.auth.models import User
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

    def test_producto_crud_cycle(self):
        user = User.objects.create_user(username='editor', password='test-password')
        self.client.force_login(user)
        create_url = reverse('tiendalibre:producto_crear')
        create_response = self.client.post(
            create_url,
            {
                'nombre': 'Producto CRUD',
                'descripcion': 'Descripción de prueba',
                'precio': '25.50',
                'stock': 4,
                'marca': 'Marca CRUD',
                'activo': True,
            },
        )

        self.assertRedirects(create_response, reverse('tiendalibre:catalogo'))
        producto = Producto.objects.get(nombre='Producto CRUD')
        self.assertEqual(producto.creado_por, user)

        update_response = self.client.post(
            reverse('tiendalibre:producto_editar', args=[producto.pk]),
            {
                'nombre': 'Producto CRUD editado',
                'descripcion': 'Descripción actualizada',
                'precio': '30.00',
                'stock': 5,
                'marca': 'Marca CRUD',
                'activo': True,
            },
        )
        self.assertRedirects(update_response, reverse('tiendalibre:catalogo'))
        producto.refresh_from_db()
        self.assertEqual(producto.nombre, 'Producto CRUD editado')

        detail_response = self.client.get(
            reverse('tiendalibre:detalle_producto', args=[producto.pk])
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, producto.nombre)
        self.assertContains(detail_response, user.username)
        self.assertContains(detail_response, reverse('tiendalibre:producto_editar', args=[producto.pk]))
        self.assertContains(detail_response, reverse('tiendalibre:producto_eliminar', args=[producto.pk]))

        delete_url = reverse('tiendalibre:producto_eliminar', args=[producto.pk])
        confirmation_response = self.client.get(delete_url)
        self.assertEqual(confirmation_response.status_code, 200)
        self.assertTemplateUsed(
            confirmation_response,
            'tiendalibre/producto_confirm_delete.html',
        )
        self.assertContains(confirmation_response, 'Confirmar eliminación')
        self.assertTrue(Producto.objects.filter(pk=producto.pk).exists())

        delete_response = self.client.post(delete_url)
        self.assertRedirects(delete_response, reverse('tiendalibre:catalogo'))
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())

    def test_authentication_protects_crud_and_controls_user_actions(self):
        producto = Producto.objects.create(
            nombre='Producto protegido',
            descripcion='Descripción de prueba',
            stock=3,
        )
        create_url = reverse('tiendalibre:producto_crear')

        response = self.client.get(create_url)
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={create_url}',
        )
        login_page = self.client.get(reverse('login'))
        self.assertTemplateUsed(login_page, 'registration/login.html')

        detail_url = reverse('tiendalibre:detalle_producto', args=[producto.pk])
        detail_response = self.client.get(detail_url)
        self.assertNotContains(detail_response, reverse('tiendalibre:producto_editar', args=[producto.pk]))
        self.assertNotContains(detail_response, reverse('tiendalibre:producto_eliminar', args=[producto.pk]))
        catalog_response = self.client.get(reverse('tiendalibre:catalogo'))
        self.assertNotContains(catalog_response, create_url)

        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin-password',
        )
        login_response = self.client.post(
            reverse('login'),
            {'username': 'admin', 'password': 'admin-password', 'next': create_url},
        )
        self.assertRedirects(login_response, create_url)

        create_response = self.client.post(
            create_url,
            {
                'nombre': 'Producto creado por admin',
                'descripcion': 'Descripción de prueba',
                'stock': 2,
                'marca': 'Marca de prueba',
            },
        )
        self.assertRedirects(create_response, reverse('tiendalibre:catalogo'))
        self.assertTrue(Producto.objects.filter(nombre='Producto creado por admin').exists())

        authenticated_detail_response = self.client.get(detail_url)
        self.assertContains(
            authenticated_detail_response,
            reverse('tiendalibre:producto_editar', args=[producto.pk]),
        )
        self.assertContains(
            authenticated_detail_response,
            reverse('tiendalibre:producto_eliminar', args=[producto.pk]),
        )

        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, '/')
        logged_out_detail_response = self.client.get(detail_url)
        self.assertNotContains(
            logged_out_detail_response,
            reverse('tiendalibre:producto_editar', args=[producto.pk]),
        )
        self.assertNotContains(
            logged_out_detail_response,
            reverse('tiendalibre:producto_eliminar', args=[producto.pk]),
        )

    def test_registration_creates_user_and_links_to_login(self):
        registration_url = reverse('tiendalibre:registro')
        login_page = self.client.get(reverse('login'))
        self.assertContains(login_page, registration_url)

        response = self.client.post(
            registration_url,
            {
                'username': 'nuevo_usuario',
                'password1': 'A-strong-password-123!',
                'password2': 'A-strong-password-123!',
            },
        )

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

    def test_only_creator_or_superuser_can_edit_or_delete_product(self):
        creator = User.objects.create_user(username='creador', password='creator-password')
        otro_usuario = User.objects.create_user(username='otro', password='other-password')
        producto = Producto.objects.create(
            creado_por=creator,
            nombre='Producto de creador',
            descripcion='Descripción de prueba',
            stock=3,
        )
        edit_url = reverse('tiendalibre:producto_editar', args=[producto.pk])
        delete_url = reverse('tiendalibre:producto_eliminar', args=[producto.pk])
        detail_url = reverse('tiendalibre:detalle_producto', args=[producto.pk])

        self.client.force_login(otro_usuario)
        self.assertEqual(self.client.get(edit_url).status_code, 404)
        self.assertEqual(self.client.get(delete_url).status_code, 404)
        self.assertNotContains(self.client.get(detail_url), edit_url)
        self.assertNotContains(self.client.get(detail_url), delete_url)

        self.client.force_login(creator)
        self.assertEqual(self.client.get(edit_url).status_code, 200)
        self.assertEqual(self.client.get(delete_url).status_code, 200)

        admin = User.objects.create_superuser(
            username='administrador',
            email='admin@example.com',
            password='admin-password',
        )
        self.client.force_login(admin)
        self.assertEqual(self.client.get(edit_url).status_code, 200)
        self.assertEqual(self.client.get(delete_url).status_code, 200)

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
