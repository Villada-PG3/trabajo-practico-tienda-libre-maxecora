from django.contrib import admin

# Register your models here.
from .models import Producto
from .models import Categoria
admin.site.register(Producto)
admin.site.register(Categoria)