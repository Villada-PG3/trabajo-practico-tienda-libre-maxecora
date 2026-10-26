from django.db import migrations, models
from django.utils.text import slugify


def populate_category_slugs(apps, schema_editor):
    categoria = apps.get_model('tiendalibre', 'Categoria')
    database = schema_editor.connection.alias
    used_slugs = set()

    for item in categoria.objects.using(database).order_by('pk'):
        slug_base = slugify(item.nombre)[:100] or 'categoria'
        slug = slug_base
        suffix = 2
        while slug in used_slugs:
            suffix_text = f'-{suffix}'
            slug = f'{slug_base[:100 - len(suffix_text)]}{suffix_text}'
            suffix += 1
        used_slugs.add(slug)
        categoria.objects.using(database).filter(pk=item.pk).update(slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ('tiendalibre', '0005_alter_producto_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
        migrations.RunPython(populate_category_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
