from django.apps import AppConfig


class ElementsConfig(AppConfig):
    name = 'elements'

    def ready(self):
        import elements.signals
