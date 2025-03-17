# Generated by Django 4.2.1 on 2024-05-26 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=12)),
                ('nom_producto', models.CharField(max_length=30)),
                ('modelo', models.CharField(blank=True, max_length=20, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=200, null=True)),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('umbral_stock_bajo', models.IntegerField(default=10)),
                ('ubicacion', models.CharField(blank=True, max_length=200, null=True)),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maest_app.categoria')),
                ('id_marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maest_app.marca')),
            ],
        ),
        migrations.CreateModel(
            name='AlertaStockBajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alerta', models.DateTimeField(auto_now_add=True)),
                ('stock_actual', models.IntegerField()),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maest_app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoEtiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_etiqueta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maest_app.etiqueta')),
                ('id_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maest_app.producto')),
            ],
            options={
                'unique_together': {('id_prod', 'id_etiqueta')},
            },
        ),
    ]
