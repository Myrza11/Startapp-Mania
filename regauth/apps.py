from django.apps import AppConfig
from django.db import transaction

class RegauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regauth'

    def ready(self):

        from .tasks import cleanup_inactive_users
        from .models import CustomUsers

        from threading import Thread

        # Define cleanup_users_thread as a standalone function
        @transaction.atomic
        def cleanup_users_thread():
            cleanup_inactive_users()

        # Start a new thread to run cleanup_users_thread
        t = Thread(target=cleanup_users_thread)
        t.daemon = True
        t.start()
