from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import dashboard.signels

    name = 'dashboard'
