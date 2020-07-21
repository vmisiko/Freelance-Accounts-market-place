from django.apps import AppConfig


class UnlocksappConfig(AppConfig):
    name = 'UnlocksApp'

    def ready(self):
        #import signals handler
        import UnlocksApp.signals