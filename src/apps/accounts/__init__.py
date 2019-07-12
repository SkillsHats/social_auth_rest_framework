from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    name = 'apps.accounts'
    label = 'accounts'
    verbose_name = 'Account'

    def ready(self):
        import apps.accounts.signals

default_app_config = 'apps.accounts.AccountsAppConfig'