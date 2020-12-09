from django.apps import AppConfig


class RegisterAndLoginConfig(AppConfig):
    name = 'register_and_login'

    def ready(self):
    	import register_and_login.signals
