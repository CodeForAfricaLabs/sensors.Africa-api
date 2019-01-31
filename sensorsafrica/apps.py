from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'sensorsafrica.accounts'


class SensorsConfig(AppConfig):
    name = 'sensorsafrica.sensors'
    # This is to not conflict with feinstaub sensors app label
    label = 'sensorsafrica.sensors'
