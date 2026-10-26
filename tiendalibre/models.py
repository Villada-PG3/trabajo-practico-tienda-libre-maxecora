from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length= 100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['nombre']
# Create your models here.
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.nombre)[:100] or 'categoria'
            self.slug = slug_base
            suffix = 2
            while Categoria.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                suffix_text = f'-{suffix}'
                self.slug = f'{slug_base[:100 - len(suffix_text)]}{suffix_text}'
                suffix += 1
        super().save(*args, **kwargs)


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='productos',
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    marca = models.CharField(max_length=100, default='Marca Desconocida')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} - {self.marca} - ${self.precio} - Stock: {self.stock}'