from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'marca', 'stock', 'mostrar_miniatura')
    readonly_fields = ('mostrar_imagen_detalle',)

    def mostrar_miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.imagen.url)
        return "No hay imagen"

    mostrar_miniatura.short_description = 'Miniatura'

    def mostrar_imagen_detalle(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.imagen.url)
        return "No hay imagen"

    mostrar_imagen_detalle.short_description = 'Previsualización de la imagen'

admin.site.register(Categoria)

