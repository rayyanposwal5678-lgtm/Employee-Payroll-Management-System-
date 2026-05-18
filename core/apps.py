import os
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Start the background scheduler when Django starts.
        
        The RUN_MAIN check ensures the scheduler only starts once,
        not on the reloader process that Django's runserver uses.
        """
        if os.environ.get('RUN_MAIN') == 'true':
            from core import scheduler
            scheduler.start()

