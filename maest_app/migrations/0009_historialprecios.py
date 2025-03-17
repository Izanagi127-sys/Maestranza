# Generated by Django 5.0.4 on 2024-06-15 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maest_app', '0008_alter_proveedor_modalidad_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialPrecios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precios', to='maest_app.producto')),
            ],
        ),
    ]
