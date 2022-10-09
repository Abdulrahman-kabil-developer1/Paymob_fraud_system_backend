from django.apps import AppConfig


class FraudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fraud'
    #run method add_actions created in models.py after migrate done
    def ready(self):
        from fraud.models import add_actions
        from django.db.models.signals import post_migrate
        post_migrate.connect(add_actions,sender=self)

