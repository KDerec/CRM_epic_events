import sys
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        if not "migrate" in sys.argv:
            from accounts.permissions import create_group_and_permission

            create_group_and_permission()
