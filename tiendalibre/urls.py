from django.urls import path
from . import views

app_name = 'tiendalibre'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('catalogo/', views.CatalogoView.as_view(), name='catalogo'),
    path('categoria/<slug:slug>/', views.CategoriaView.as_view(), name='categoria'),
    path('home_1/', views.home_1, name='home_1'),
    path('acerca-de-mi/', views.acerca_de_mi, name='acerca-de-mi'),
    path('detalle-producto/<int:pk>/', views.DetalleProductoView.as_view(), name='detalle_producto'),
    path('producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
]