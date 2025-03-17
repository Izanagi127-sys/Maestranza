from django.apps import AppConfig

class MaestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maest_app'

    def ready(self):
        import maest_app.signals
