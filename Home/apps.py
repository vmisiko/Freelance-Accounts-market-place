from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'Home'

    def ready(self):
        # import signal handlers
        import Home.signals