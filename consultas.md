1) Producto.objects.all() 
Devuelve un QuerySet con todos los productos.

2) Producto.objects.count()
Devuelve un número entero del total de productos.

3) Producto.objects.filter(precio__gt=1000)
Filtra productos con precio mayor a 1000, gt = greater than.

4) Producto.objects.filter(nombre__icontains='')
Filtra productos cuyo nombre contenga lo buscado, icontains = no distingue mayusculas.

5) Producto.objects.get(id=1)
Obtener un producto específico por ID.

6) Producto.objects.filter(stock__in=[])
Filtrar productos con stock en valores específicos.

7)  producto = Producto.objects.get(id=1)
    print(producto.categoria.nombre)  
Accede a la categoría relacionada al producto.

8)  categoria = Categoria.objects.get(nombre='Electrónica')
    print(categoria.productos.all())  
Accede a todos los productos de una categoría.

9) Producto.objects.exclude(stock=0)
Excluye productos sin stock (stock diferente de 0).

10) Producto.objects.filter(nombre__startswith='')
Filtra productos cuyo nombre comience con una letra x.
