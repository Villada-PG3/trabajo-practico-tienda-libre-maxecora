from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length= 100, unique=True)
    #slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['nombre']
# Create your models here.
    def __str__(self):
        return self.nombre
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