from django.apps import AppConfig


class CheckinAppConfig(AppConfig):

    name = "django_rest_demo.checkin"
    verbose_name = "Checkin"

    # def ready(self):
    #     try:
    #         import users.signals  # noqa F401
    #     except ImportError:
    #         pass
