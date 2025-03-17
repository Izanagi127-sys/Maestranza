# maest_app/tasks.py

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Producto, Informe
import pandas as pd
from django.utils.timezone import now
from django.core.files.storage import default_storage

@shared_task
def generar_informe_excel():
    productos = Producto.objects.all().values('nom_producto', 'precio', 'stock', 'ubicacion')
    df = pd.DataFrame(productos)
    timestamp = now().strftime('%Y%m%d_%H%M%S')
    filename = f'informe_{timestamp}.xlsx'
    filepath = default_storage.save(f'informes/{filename}', df.to_excel(index=False))
    Informe.objects.create(nombre_archivo=filename, archivo=filepath)
    return filepath
