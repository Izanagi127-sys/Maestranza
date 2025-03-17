# maestranzas/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maestranzas.settings')
app = Celery('maestranzas')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# celery.py (añadir al final del archivo)
from celery.schedules import crontab

app.conf.beat_schedule = {
    'generar-informe-cada-hora': {
        'task': 'your_app_name.tasks.generar_informe_excel',
        'schedule': crontab(minute=0, hour='*'),  # Cada hora en el minuto 0
    },
}
